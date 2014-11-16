#!/usr/bin/env python
import os
import click
import re
import datetime
from locale import setlocale, LC_TIME
from .library import IPhotoLibrary

setlocale(LC_TIME, '')

default_iphoto_root = os.path.expanduser("~/Pictures/iPhoto Library.photolibrary")


@click.group()
@click.option(
    "--root", default=default_iphoto_root, envvar="IPHOTO_ROOT",
    type=click.Path(exists=True, file_okay=False))
@click.option("--show-queries", is_flag=True, help="Show raw SQL queries.")
@click.pass_context
def cli(ctx, root, show_queries):
    lib = ctx.obj['lib'] = IPhotoLibrary(root)
    if show_queries:
        lib.db_engine.echo = True


def date_from_string(date_str, date_format="%Y-%m-%d"):
    return datetime.datetime.strptime(date_str.strip(), date_format).date()


def offset_from_string(offset_str):
    """Turn --offset-time value into a timedelta."""
    match = re.match(r"^\s*([+-]?)(\d+)\s*", offset_str.strip())
    negative = match.group(1) == "-"
    seconds = int(match.group(2))
    return datetime.timedelta(seconds=(-seconds if negative else seconds))


@cli.command(name="exec")
@click.option("--album", 'album_name', metavar="NAME", help="Execute for every image in matched album.")
@click.option(
    "--event", 'event_date', metavar="DATE", type=date_from_string,
    help="Execute for every image in matched event. Format: %Y-%m-%d. For instance, 2014-10-14.")
@click.option(
    "--flagged", 'flagged_only', is_flag=True, help="Execute for every flagged image.")
@click.option("--reset-time", is_flag=True, help="Reset the image's v1 time to match the master time.")
@click.option(
    "--offset-time", metavar="[+|-]SECONDS", type=offset_from_string,
    help="Add or subtract from the current v1 time.")
@click.option(
    "--commit", 'should_commit', is_flag=True,
    help="Commit to the database. Omitting this flag results in a dry-run.")
@click.argument("script", default="")
@click.pass_context
def exec_(ctx, album_name, event_date, flagged_only, reset_time, offset_time, should_commit, script):
    """
    Run a script for every matched photo.
    """
    lib = ctx.obj['lib']

    for ver in iter_versions(lib, album_name, event_date, flagged_only):
        exec_locals = {
            'v0': next(v0 for v0 in ver.master.version_collection if v0.versionNumber == 0),
            'v1': ver,
            'master': ver.master,
            'date': datetime.date,
            'timedelta': datetime.timedelta,
        }
        for cur_script in iter_scripts(reset_time, offset_time, script):
            exec(cur_script, None, exec_locals)
        for obj, attr_name, old_value, new_value in lib.flush_attr_changes():
            click.echo("  %s.%s: %s -> %s" % (obj, attr_name, old_value, new_value))

    changes = list(lib.get_attr_changes())
    if changes and should_commit:
        click.echo("Committing")
        lib.commit()


def iter_versions(lib, album_name, event_date, flagged_only):
    seen_versions = set()
    albums = lib.get_albums(album_name=album_name, event_date=event_date)
    for album in albums:
        for version in lib.get_photos_in_album(album):
            if version.modelId in seen_versions:
                continue
            seen_versions.add(version.modelId)
            if flagged_only and not version.isFlagged:
                continue
            yield version


def iter_scripts(reset_time, offset_time, generic_script):
    if reset_time:
        yield "v1.imageDate = master.imageDate\n"
    if offset_time:
        yield "v1.imageDate += %s\n" % repr(offset_time)
    if generic_script:
        yield generic_script
    if not reset_time and not offset_time and not generic_script:
        yield "print(master)\n"


def main():
    # Ignore sqlalchemy's datetime truncation warnings
    import warnings
    from sqlalchemy.exc import SAWarning, OperationalError
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=SAWarning)
        try:
            cli(obj={})
        except OperationalError as ex:
            if "database is locked" in str(ex.orig):
                click.echo("Database is locked... maybe other programs are using it?")
            else:
                raise


if __name__ == '__main__':
    main()
