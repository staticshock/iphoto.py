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

**Warning:** `exec` is a dangerous, potentially destructive command that directly
operates on your iPhoto database. Backup your library before proceeding.

**Warning:** If you run `exec` and concurrently make changes via iPhoto, the
results are not predictable. The least you can expect is some lag between an
action in iPhoto and an observable change on the command line, but also be
aware of the potential for data loss, since the application could operate from
a stale cache of recent changes. *iPhoto has no reasonable expectation that
other applications are using its database.*

The `exec` command relies on some knowledge of the iPhoto object model,
which is described in its own section lower down.

.. code-block:: bash

    # List photos with timestamps that differ from master (this is a dry-run
    # operation, since --commit is not specified)
    $ iphoto exec --reset-time

    # Reset photos in the Mayhem album to master time
    $ iphoto exec --album='Mayhem' --reset-time --commit

    # Subtract an hour from flagged photos in the Mayhem album
    $ iphoto exec --album='Mayhem' --flagged --offset-time='-3600' --commit

    # Unflag all photos from events containing photos from 10/14/2014
    $ iphoto exec --event='2014-10-14' --commit 'v1.isFlagged = 0'

    # Print the name and image path for every photo from the event of 10/14/2014
    $ iphoto exec --event '2014-10-14' \
           'print("%s\t%s" % (master.name, master.imagePath))'

    # Print the file sizes of all flagged photos
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
