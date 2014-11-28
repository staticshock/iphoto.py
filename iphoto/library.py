#!/usr/bin/env python3
import os
import builtins
import plistlib
from datetime import datetime, timedelta
from sqlalchemy import \
    types, event, create_engine, Table, Column, Integer, String, ForeignKey
from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.orm.attributes import instance_state
from sqlalchemy.ext.automap import automap_base


class IPhotoPaths(object):
    """Path helper"""

    def __init__(self, root=None):
        self.root = root or os.path.expanduser("~/Pictures/iPhoto Library.photolibrary")
        self.database = os.path.join(self.root, "Database")
        self.albums = os.path.join(self.database, "Albums")
        self.masters = os.path.join(self.root, "Masters")

    @property
    def library_db_path(self):
        return os.path.join(self.database, "Library.apdb")

    def album_plist_path(self, albumUuid):
        return os.path.join(self.albums, albumUuid + ".apalbum")

    def master_file_path(self, relPath):
        return os.path.join(self.masters, relPath)


class IPhotoDateTimeType(types.TypeDecorator):
    """
    iPhoto stores timestamps as the number of seconds since midnight of
    Jan 1st, 2001. Some columns always store it as an int (second precision),
    others are always floats (microsecond precision), and yet others are a mix.

    The iPhoto-originating timestamps are probably always floats. The mixed
    columns likely represent data originating elsewhere but eventually updated
    via iPhoto for individual records.
    """
    impl = types.Integer
    epoch = datetime(2001, 1, 1, 0, 0, 0)

    def process_bind_param(self, value, dialect):
        if value is not None:
            total_seconds = (value - self.epoch).total_seconds()
            if not value.microsecond:
                total_seconds = int(total_seconds)
            return total_seconds

    def process_result_value(self, value, dialect):
        if value is not None:
            return self.epoch + timedelta(seconds=value)


@event.listens_for(Table, "column_reflect")
def inject_custom_datetime_type(inspector, table, column_info):
    if isinstance(column_info['type'], types.DateTime):
        column_info['type'] = IPhotoDateTimeType()


def table_name_to_class_name(cls, tbl_name, tbl):
    # Strip the first two letters of the table names (the "RK" prefix.)
    return tbl_name[2:]


Base = automap_base()
class_names = ('Master', 'Version', 'ImageAdjustment', 'Album', 'Folder', 'ImportGroup')
uuid_foreign_keys = (
    ('Master', 'importGroupUuid', 'ImportGroup'),
    # "project" and "folder" seem to be interchangeable terminology in the
    # schema, but they're consistenty mapped to "folder" here, since that's the
    # table name.
    ('Master', 'projectUuid', 'Folder'),
    ('Master', 'originalVersionUuid', 'Version'),
    ('Version', 'masterUuid', 'Master'),
    ('Version', 'projectUuid', 'Folder'),
    ('ImageAdjustment', 'versionUuid', 'Version'),
    ('Album', 'folderUuid', 'Folder'),
    ('Folder', 'parentFolderUuid', 'Folder'),
    ('Folder', 'implicitAlbumUuid', 'Album'),
)

# Tables with uuid primary keys
for name in class_names:
    props = dict(
        __tablename__='RK' + name,
        # Pretend like modelId is not the primary key. Other tables rarely
        # actually reference it by modelId, anyway.
        modelId=Column(Integer),
        # Pretend like uuid is the primary key. None of the foreign keys are
        # set up for this, so those will have to get faked out as well.
        uuid=Column(String, primary_key=True),
    )
    # Fake out foreign keys referencing the uuids
    for fk_side_table, col_name, pk_side_table in uuid_foreign_keys:
        if fk_side_table == name:
            props[col_name] = Column(String, ForeignKey('RK%s.uuid' % pk_side_table))
    builtins.__dict__[name] = type(name, (Base,), props)


def is_event(album):
    return album.albumSubclass == 1


def is_smart_album(album):
    return album.albumSubclass == 2


def album_repr(self):
    # if it's an event, call it an "unnamed event from date X" if name is missing
    if self.name:
        return self.name
    if is_event(self):
        start = self.folder.minImageDate.date().strftime("%x")
        end = self.folder.maxImageDate.date().strftime("%x")
        if start != end:
            return "Unnamed event (%s to %s)" % (start, end)
        else:
            return "Unnamed event (%s)" % start
    else:
        # non-events are pretty damn unlikely to be unnamed
        return self.uuid


Album.__repr__ = album_repr
Master.__repr__ = lambda self: "{r.folder.album} / {r.name}".format(r=self)
Version.__repr__ = lambda self: "{r.folder.album} / {r.name} / v{r.versionNumber}".format(r=self)


# Override some default relationship names.
# Format: (local_table_class, local_column_name, one_to_many_name, many_to_one_name)
_rel_names = (
    (Master, "originalVersionUuid", "originalVersion", None),
    (Folder, "parentFolderUuid", "parentFolder", "childFolders"),
)


def name_for_scalar_relationship(base, local_cls, referred_cls, constraint):
    local_col = constraint.columns[0]
    #referred_col = list(local_col.foreign_keys)[0].column
    #print("%s.%s -> %s.%s" % (local_col.table.key, local_col.key, referred_col.table.key, referred_col.key))
    for tbl_cls, col_name, one_to_many_name, _ in _rel_names:
        if (tbl_cls, col_name) == (local_cls, local_col.key):
            return one_to_many_name
    else:
        name = referred_cls.__name__
        return name[0].lower() + name[1:]


def name_for_collection_relationship(base, local_cls, referred_cls, constraint):
    local_col = constraint.columns[0]
    for tbl_cls, col_name, _, many_to_one_name in _rel_names:
        if (tbl_cls, col_name) == (local_cls, local_col.key) and many_to_one_name:
            return many_to_one_name
    else:
        name = referred_cls.__name__
        return name[0].lower() + name[1:] + "s"


def accumulate_db_changes(session, accumulator):
    """Keep track of flushed changes in accumulator"""
    @event.listens_for(session, 'before_flush')
    def receive_before_flush(session, flush_context, instances):
        for obj in session.dirty:
            state = instance_state(obj)
            for attr_name, old_value in state.committed_state.items():
                history = state.get_history(attr_name, True)
                if history.has_changes():
                    new_value = history.added[0]
                    accumulator.append((obj, attr_name, old_value, new_value))


class IPhotoLibrary(object):
    """
    An interface to the iPhoto library as a whole. Serves as an interface to
    the SQLite dbs, property lists, and the master image files.
    """
    def __init__(self, root=None):
        self.paths = IPhotoPaths(root)
        self.db_engine = create_engine("sqlite:///" + self.paths.library_db_path)
        # This makes all table-based entities available via Base.classes.*
        Base.prepare(
            self.db_engine,
            reflect=True,
            classname_for_table=table_name_to_class_name,
            name_for_scalar_relationship=name_for_scalar_relationship,
            name_for_collection_relationship=name_for_collection_relationship
        )
        self.db_session = Session(self.db_engine)
        self._attr_changes = []
        accumulate_db_changes(self.db_session, self._attr_changes)

    def album_query(
            self, album_name=None, event_date=None, prefer_events=True,
            filter=None, filter_by=None):
        """
        Create a generic album query.

        :param album_name: Match album name exactly.
        :param event_date: Match events containing photos from a specific date.
        :param prefer_events: Use most of the provided criteria to match
                              events, but expand the search to non-events
                              matching `album_name`.
        :param filter: Attach additional filter criteria.
        :param filter_by: Attach additional filter criteria via dictionary.
        """
        query = self.db_session.query(Album)

        # Pre-fetch folder, masters, and versions
        query = query.options(
            joinedload(Album.folder)
                .joinedload(Folder.versions)
                .joinedload(Version.master)
                .joinedload(Master.versions))

        if album_name is not None:
            query = query.filter(Album.name == album_name)

        if event_date is not None:
            event_datetime = datetime.combine(event_date, datetime.min.time())
            query = query.join(Album.folder).filter(and_(
                Album.albumSubclass == 1,
                Folder.minImageDate <= event_datetime + timedelta(days=1),
                Folder.maxImageDate >= event_datetime))

        if filter:
            query = query.filter(filter)

        combined_filter_by = dict(isMagic=0, isInTrash=0)
        if prefer_events and not album_name:
            combined_filter_by['albumSubclass'] = 1

        combined_filter_by.update(filter_by or {})
        query = query.filter_by(**combined_filter_by)

        return query.filter(
            Album.folderUuid != 'LibraryFolder',
            ~and_(
                Album.folderUuid == 'TopLevelAlbums',
                Album.albumSubclass == 1
            )
        )

    def get_albums(self, **kwargs):
        query = self.album_query(**kwargs)
        return query.all()

    def get_event_albums(self, filter_by=None, **kwargs):
        kwargs.update(filter_by=dict(filter_by or {}, albumSubclass=1))
        return self.get_albums(**kwargs)

    def get_smart_albums(self, filter_by=None, **kwargs):
        kwargs.update(filter_by=dict(filter_by or {}, albumSubclass=2))
        return self.get_albums(**kwargs)

    def get_regular_albums(self, filter_by=None, **kwargs):
        kwargs.update(filter_by=dict(filter_by or {}, albumSubclass=3))
        return self.get_albums(**kwargs)

    def version_query(self, filter_by=None):
        query = self.db_session.query(Version)

        combined_filter_by = dict(versionNumber=1, isInTrash=0)
        combined_filter_by.update(filter_by or {})
        return query.filter_by(**combined_filter_by)

    def get_flagged_photos(self, filter_by=None, **kwargs):
        kwargs.update(filter_by=dict(filter_by or {}, isFlagged=1))
        query = self.version_query(**kwargs)
        return query.all()

    def get_photos_in_album(self, album):
        """Returns Version records in album."""
        if is_event(album):
            # Events: the photo list is stored in SQLite.
            return (ver for ver in album.folder.versions if ver.versionNumber == 1)
        elif is_smart_album(album):
            # Smart albums: the photo list generated dynamically from a
            # query stored in the album's plist under the key 'UserQueryInfo'.
            # Sadly, it's stored as a keyed archive, not a property list, so
            # plistlib can't actually parse it.
            return tuple()
        else:
            # Regular albums: the photo list is stored as an array of uuids in
            # the album's property list.
            plist_path = self.paths.album_plist_path(album.uuid)
            with open(plist_path, "rb") as plist_stream:
                plist = plistlib.load(plist_stream)
            query = self.uuid_query(Version, plist['versionUuids'])
            return query.all()

    def uuid_query(self, table_cls, uuids):
        return self.db_session.query(table_cls).filter(table_cls.uuid.in_(uuids))

    def master_query(self, filter_by=None):
        query = self.db_session.query(Master)

        combined_filter_by = dict(isInTrash=0)
        combined_filter_by.update(filter_by or {})
        return query.filter_by(**combined_filter_by)

    def get_trashed_photos(self, filter_by=None, **kwargs):
        kwargs.update(filter_by=dict(filter_by or {}, isInTrash=1))
        query = self.master_query(**kwargs)
        return query.all()

    def get_attr_changes(self):
        """Flushes and returns the accumulated list of attr changes."""
        self.db_session.flush()
        return self._attr_changes

    def flush_attr_changes(self):
        """Flushes and returns only the most recent batch of attr changes."""
        ix_start = len(self._attr_changes)
        self.db_session.flush()
        return self._attr_changes[ix_start:]

    def commit(self):
        self.db_session.commit()
