Properties of master records
============================

Some of these map to database columns, while others map to foreign key
relationships.

+------------------------+-------------+-----------------------------------------------------------+
| Property               | Type        | Description                                               |
+========================+=============+===========================================================+
| `modelId`              | int         | Internal primary key (not that useful.)                   |
+------------------------+-------------+-----------------------------------------------------------+
| `uuid`                 | str         | A unique key referenced by other tables (useful for       |
|                        |             | recognizing relationships.)                               |
+------------------------+-------------+-----------------------------------------------------------+
| `name`                 | str         | The name of the photo (defaults to filename without       |
|                        |             | extension.)                                               |
+------------------------+-------------+-----------------------------------------------------------+
| `projectUuid`          | str         | Uuid of the `Folder` record, which indirectly associates  |
|                        |             | this record with an event album.                          |
+------------------------+-------------+-----------------------------------------------------------+
| `folder`               | Folder      | `Folder` record, which indirectly associates this record  |
|                        |             | with an event album.                                      |
+------------------------+-------------+-----------------------------------------------------------+
| `importGroupUuid`      | str         | Uuid of the associated `ImportGroup` record (not that     |
|                        |             | useful.)                                                  |
+------------------------+-------------+-----------------------------------------------------------+
| `importGroup`          | ImportGroup | The associated `ImportGroup` record (not that useful.)    |
+------------------------+-------------+-----------------------------------------------------------+
| `fileVolumeUuid`       | str         | I haven't looked into the specifics of how this is used,  |
|                        |             | but it looks like it might be useful.                     |
+------------------------+-------------+-----------------------------------------------------------+
| `alternateMasterUuid`  | str         | Unsure.                                                   |
+------------------------+-------------+-----------------------------------------------------------+
| `originalVersionUuid`  | str         | The `uuid` of the v0 record.                              |
+------------------------+-------------+-----------------------------------------------------------+
| `originalVersionName`  | str         | The `name` of the v0 record (not that useful; no idea why |
|                        |             | this is separate from name.)                              |
+------------------------+-------------+-----------------------------------------------------------+
| `originalVersion`      | Version     | The v0 record.                                            |
+------------------------+-------------+-----------------------------------------------------------+
| `versions`             | Version[]   | All the associated `Version` records.                     |
+------------------------+-------------+-----------------------------------------------------------+
| `fileName`             | str         | The file name of the originally imported image.           |
+------------------------+-------------+-----------------------------------------------------------+
| `type`                 | str         | A string representing the file type. Can be               |
|                        |             | "IMGT", "VIDT", and probably others.                      |
+------------------------+-------------+-----------------------------------------------------------+
| `subtype`              | str         | A string representing the file type a bit more precisely. |
|                        |             | Can be "JPGST", "VIDST", and maybe others.                |
+------------------------+-------------+-----------------------------------------------------------+
| `fileIsReference`      | int         | Probably related to `fileVolumeUuid`.                     |
+------------------------+-------------+-----------------------------------------------------------+
| `isExternallyEditable` | int         | Unsure.                                                   |
+------------------------+-------------+-----------------------------------------------------------+
| `isTrulyRaw`           | int         | Unsure.                                                   |
+------------------------+-------------+-----------------------------------------------------------+
| `isMissing`            | int         | Unsure.                                                   |
+------------------------+-------------+-----------------------------------------------------------+
| `hasAttachments`       | int         | Unsure.                                                   |
+------------------------+-------------+-----------------------------------------------------------+
| `hasNotes`             | int         | Unsure.                                                   |
+------------------------+-------------+-----------------------------------------------------------+
| `hasFocusPoints`       | int         | Unsure.                                                   |
+------------------------+-------------+-----------------------------------------------------------+
| `imagePath`            | str         | Path to master image relative to `$IPHOTO_ROOT/Masters/`  |
+------------------------+-------------+-----------------------------------------------------------+
| `fileSize`             | int         | Size of master image in bytes.                            |
+------------------------+-------------+-----------------------------------------------------------+
| `pixelFormat`          | int         | Unsure.                                                   |
+------------------------+-------------+-----------------------------------------------------------+
| `duration`             | float       | Unsure.                                                   |
+------------------------+-------------+-----------------------------------------------------------+
| `imageDate`            | datetime    | Extracted from the image's Exif info, though I'm not sure |
|                        |             | which header it corresponds to.                           |
+------------------------+-------------+-----------------------------------------------------------+
| `fileCreationDate`     | datetime    | Not sure where this originates.                           |
+------------------------+-------------+-----------------------------------------------------------+
| `fileModificationDate` | datetime    | Not sure where this originates, but it's shown as         |
|                        |             | "modified time" in the UI.                                |
+------------------------+-------------+-----------------------------------------------------------+
| `streamAssetId`        | str         | Unsure.                                                   |
+------------------------+-------------+-----------------------------------------------------------+
| `streamSourceUuid`     | str         | Unsure.                                                   |
+------------------------+-------------+-----------------------------------------------------------+
| `burstUuid`            | str         | Unsure.                                                   |
+------------------------+-------------+-----------------------------------------------------------+
| `imageHash`            | str         | Unsure.                                                   |
+------------------------+-------------+-----------------------------------------------------------+
| `originalFileName`     | str         | Not sure when this would ever differ from `fileName`      |
+------------------------+-------------+-----------------------------------------------------------+
| `originalFileSize`     | int         | Not sure when this would ever differ from `fileSize`      |
+------------------------+-------------+-----------------------------------------------------------+
| `imageFormat`          | int         | A number (e.g. 1246774599) representing the format type.  |
|                        |             | I can't find an authoritative listing of these numbers,   |
|                        |             | but some others are listed here:                          |
|                        |             | https://github.com/dphenderson/iPhoto2web                 |
+------------------------+-------------+-----------------------------------------------------------+
| `importedBy`           | int         | Unsure.                                                   |
+------------------------+-------------+-----------------------------------------------------------+
| `createDate`           | datetime    | Original time of import.                                  |
+------------------------+-------------+-----------------------------------------------------------+
| `isInTrash`            | int         | 1 if the image has been trashed via the UI, 0 otherwise.  |
+------------------------+-------------+-----------------------------------------------------------+
| `faceDetectionState`   | int         | Unsure.                                                   |
+------------------------+-------------+-----------------------------------------------------------+
| `colorSpaceName`       | str         | Unsure. Extracted from the Exif headers, I assume.        |
+------------------------+-------------+-----------------------------------------------------------+
| `colorSpaceDefinition` | bytes       | Unsure.                                                   |
+------------------------+-------------+-----------------------------------------------------------+
| `fileAliasData`        | bytes       | Unsure.                                                   |
+------------------------+-------------+-----------------------------------------------------------+
