iPhoto.py
=========

Command line utilities for managing an iPhoto library.

**Warning:** not tested with any version of iPhoto aside from my own, which is
currently v9.5.1. Use at your own risk.

Currently requires python 3.4. Not for any serious reason, but it's the only
version I've tested with.

Installation
------------

.. code-block:: bash

    pip install iphoto

Command line usage
------------------

**Warning:** ``exec`` is a dangerous, potentially destructive command that directly
operates on your iPhoto database. Backup your library before proceeding.

**Warning:** If you run ``exec`` and concurrently make changes via iPhoto, the
results are not predictable. The least you can expect is some lag between an
action in iPhoto and an observable change on the command line, but also be
aware of the potential for data loss, since the application could operate from
a stale cache of recent changes. *iPhoto has no reasonable expectation that
other applications are using its database.*

The ``exec`` command relies on some knowledge of the iPhoto object model,
which is described in its own section below.

.. code-block:: bash

    # If you don't specify any specific actions, the `exec` script defaults to
    # `print(master)`:
    $ iphoto exec
    The Badlands / DSC_0240
    ... snip ...
    Unnamed event (10/30/2014) / 20141030_150848

    # Unless you specify the `--commit` flag, everything is executed in
    # "dry-run" mode. For instance, this lists the photos that would be
    # modified by the `--reset-time` action:
    $ iphoto exec --reset-time

    # Different filters are available for constraining which photos `exec`
    # applies to. For instance, this resets the v1 time to match the master
    # time for photos in the Mayhem album:
    $ iphoto exec --album='Mayhem' --reset-time --commit

    # This subtracts an hour from flagged photos in the Mayhem album:
    $ iphoto exec --album='Mayhem' --flagged --offset-time='-3600' --commit

    # You can specify a generic python script which executes in the context of
    # a single photo. For instance, this unflags everything from events
    # containing photos from 10/14/2014:
    $ iphoto exec --event='2014-10-14' --commit 'v1.isFlagged = 0'

    # This prints the name and image path for every photo from the event of
    # 10/14/2014:
    $ iphoto exec --event '2014-10-14' \
           'print("%s\t%s" % (master.name, master.imagePath))'

    # This prints the file sizes of all flagged photos:
    $ iphoto exec --flagged 'print(master.fileSize)'

Object model
------------

iPhoto doesn't apply any image adjustments to the originally imported "master"
image. Instead, it keeps a copy of each image's Exif data in a SQLite database.
In fact, it actually keeps three copies--the master, v0, and v1 records, and
all of them are created on import. The properties you see in the UI all come
from the v1 record. I recommend that you stick to the same approach: edit v1,
and, if necessary, revert it by copying properties from v0 or from master.

When you export photos out of iPhoto, the properties from v1 are automatically
applied to the exported photos.

Album types
~~~~~~~~~~~

There are three types of album records:

1. **Events:** exactly what you'd think if you've used the UI. Each photo is
   associated with exactly one event album, which is referenced by master and
   version records via ``projectUuid``.
2. **Smart albums:** custom-made albums with dynamic, query-defined contents.
   The query is hidden away inside of a keyed archive, which is itself stored
   in the album's binary plist file. *This album type is currently unsupported
   by iphoto.py because I haven't found or written a parser for the keyed
   archive format. It's technically similar to bplist parser, but more
   complicated.*
3. **Regular albums:** custom-made albums with a static, user-curated image
   list. The v1 uuids of the included images are listed in the album's binary
   plist file.

See also
~~~~~~~~

* `Properties of album records <doc/album.rst>`_.
* `Properties of folder records <doc/folder.rst>`_.
* `Properties of master records <doc/master.rst>`_.
* `Properties of version records <doc/version.rst>`_.
