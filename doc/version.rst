Properties of version records
=============================

Since version records use the master record as their template, a lot of the
properties overlap content.

+-----------------------------------+-------------------+------------------------------------------+
| Property                          | Type              | Description                              |
+===================================+===================+==========================================+
| `modelId`                         | int               | Internal primary key (not that useful.)  |
+-----------------------------------+-------------------+------------------------------------------+
| `uuid`                            | str               | A unique key referenced by other tables  |
|                                   |                   | (useful for recognizing relationships.)  |
+-----------------------------------+-------------------+------------------------------------------+
| `name`                            | str               | The name of the photo (defaults to       |
|                                   |                   | filename without extension.)             |
+-----------------------------------+-------------------+------------------------------------------+
| `fileName`                        | str               | The file name of the originally imported |
|                                   |                   | image.                                   |
+-----------------------------------+-------------------+------------------------------------------+
| `versionNumber`                   | int               | Distinguishes v1 from v0.                |
+-----------------------------------+-------------------+------------------------------------------+
| `stackUuid`                       | str               | Unsure.                                  |
+-----------------------------------+-------------------+------------------------------------------+
| `masterUuid`                      | str               | Uuid of the associated `Master` record.  |
+-----------------------------------+-------------------+------------------------------------------+
| `masterId`                        | int               | Id of the associated `Master` record.    |
+-----------------------------------+-------------------+------------------------------------------+
| `rawMasterUuid`                   | str               | Unsure. Always NULL in my library.       |
+-----------------------------------+-------------------+------------------------------------------+
| `nonRawMasterUuid`                | str               | Unsure. Always same as `masterUuid` for  |
|                                   |                   | me.                                      |
+-----------------------------------+-------------------+------------------------------------------+
| `master`                          | Master            | The associated `Master` record.          |
+-----------------------------------+-------------------+------------------------------------------+
| `projectUuid`                     | str               | Uuid of the associated `Folder` record.  |
+-----------------------------------+-------------------+------------------------------------------+
| `folder`                          | Folder            | The associated `Folder` record.          |
+-----------------------------------+-------------------+------------------------------------------+
| `imageTimeZoneName`               | str               | Unsure. Always "GMT" in my library.      |
+-----------------------------------+-------------------+------------------------------------------+
| `imageDate`                       | datetime          | Extracted from the image's Exif info,    |
|                                   |                   | though I'm not sure which header it      |
|                                   |                   | corresponds to.                          |
+-----------------------------------+-------------------+------------------------------------------+
| `mainRating`                      | int               | Presumably the rating value assigned via |
|                                   |                   | the UI (1-5, or 0 if not assigned.)      |
+-----------------------------------+-------------------+------------------------------------------+
| `isHidden`                        | int               | 1 if photo is hidden via the UI, 0       |
|                                   |                   | otherwise.                               |
+-----------------------------------+-------------------+------------------------------------------+
| `isFlagged`                       | int               | 1 if photo is flagged via the UI, 0      |
|                                   |                   | otherwise.                               |
+-----------------------------------+-------------------+------------------------------------------+
| `isOriginal`                      | int               | Unsure.                                  |
+-----------------------------------+-------------------+------------------------------------------+
| `isEditable`                      | int               | Unsure.                                  |
+-----------------------------------+-------------------+------------------------------------------+
| `colorLabelIndex`                 | int               | Unsure.                                  |
+-----------------------------------+-------------------+------------------------------------------+
| `masterHeight`                    | int               | Height of master image in pixels.        |
+-----------------------------------+-------------------+------------------------------------------+
| `masterWidth`                     | int               | Width of master image in pixels.         |
+-----------------------------------+-------------------+------------------------------------------+
| `processedHeight`                 | int               | Height of the photo represented by the   |
|                                   |                   | current version (e.g. after cropping,    |
|                                   |                   | rotating, etc.)                          |
+-----------------------------------+-------------------+------------------------------------------+
| `processedWidth`                  | int               | Width of the photo represent by the      |
|                                   |                   | current version.                         |
+-----------------------------------+-------------------+------------------------------------------+
| `rotation`                        | int               | Degrees the photo has been rotated. One  |
|                                   |                   | of: 0, 90, 180, 270.                     |
+-----------------------------------+-------------------+------------------------------------------+
| `hasAdjustments`                  | int               | 1 if the photo has been adjusted, 0      |
|                                   |                   | otherwise.                               |
+-----------------------------------+-------------------+------------------------------------------+
| `hasEnabledAdjustments`           | int               | Unsure. Set to 1 once the photo has been |
|                                   |                   | adjusted, and possible set back to 0 if  |
|                                   |                   | the "Revert to original" button is used? |
+-----------------------------------+-------------------+------------------------------------------+
| `imageAdjustments`                | ImageAdjustment[] | A collection of `ImageAdjustment`        |
|                                   |                   | records.                                 |
+-----------------------------------+-------------------+------------------------------------------+
| `hasNotes`                        | int               | Unsure. Probably corresponds to the      |
|                                   |                   | "description" field in the UI?           |
+-----------------------------------+-------------------+------------------------------------------+
| `createDate`                      | datetime          | Original time of import.                 |
+-----------------------------------+-------------------+------------------------------------------+
| `exportImageChangeDate`           | datetime          | Unsure. Only v1 has a value for this.    |
+-----------------------------------+-------------------+------------------------------------------+
| `exportMetadataChangeDate`        | datetime          | Unsure. Only v1 has a value for this.    |
+-----------------------------------+-------------------+------------------------------------------+
| `isInTrash`                       | int               | 1 if the image has been trashed via the  |
|                                   |                   | UI, 0 otherwise.                         |
+-----------------------------------+-------------------+------------------------------------------+
| `thumbnailGroup`                  | str               | Unsure.                                  |
+-----------------------------------+-------------------+------------------------------------------+
| `overridePlaceId`                 | int               | Unsure. Presumably this is for a         |
|                                   |                   | UI-specified place for photos that       |
|                                   |                   | include geolocation Exif data.           |
+-----------------------------------+-------------------+------------------------------------------+
| `exifLatitude`                    | float             | Unsure.                                  |
+-----------------------------------+-------------------+------------------------------------------+
| `exifLongitude`                   | float             | Unsure.                                  |
+-----------------------------------+-------------------+------------------------------------------+
| `renderVersion`                   | int               | Unsure.                                  |
+-----------------------------------+-------------------+------------------------------------------+
| `adjSeqNum`                       | int               | Unsure.                                  |
+-----------------------------------+-------------------+------------------------------------------+
| `supportedStatus`                 | int               | Unsure.                                  |
+-----------------------------------+-------------------+------------------------------------------+
| `videoInPoint`                    | str               | Unsure. Always NULL in my library.       |
+-----------------------------------+-------------------+------------------------------------------+
| `videoOutPoint`                   | str               | Unsure. Always NULL in my library.       |
+-----------------------------------+-------------------+------------------------------------------+
| `videoPosterFramePoint`           | str               | Unsure.                                  |
+-----------------------------------+-------------------+------------------------------------------+
| `showInLibrary`                   | int               | This is 1 for v1 and 0 for v0.           |
+-----------------------------------+-------------------+------------------------------------------+
| `editState`                       | int               | Unsure. Seems to be NULL for v0, and     |
|                                   |                   | either 0 or 4 for v1 in my library.      |
+-----------------------------------+-------------------+------------------------------------------+
| `contentVersion`                  | int               | Unsure. In my library, this is always    |
|                                   |                   | NULL for v0, and 0 for v1.               |
+-----------------------------------+-------------------+------------------------------------------+
| `propertiesVersion`               | int               | Unsure. In my library, this is always    |
|                                   |                   | NULL for v0, and 0 for v1.               |
+-----------------------------------+-------------------+------------------------------------------+
| `rawVersion`                      | str               | Unsure. Always NULL in my library.       |
+-----------------------------------+-------------------+------------------------------------------+
| `faceDetectionIsFromPreview`      | int               | Unsure. Always 0 in my library.          |
+-----------------------------------+-------------------+------------------------------------------+
| `faceDetectionRotationFromMaster` | int               | Unsure.                                  |
+-----------------------------------+-------------------+------------------------------------------+
| `editListData`                    | bytes             | Unsure. Always NULL in my library. Based |
|                                   |                   | on the datatype, I'd guess that this is  |
|                                   |                   | a keyed archive.                         |
+-----------------------------------+-------------------+------------------------------------------+
| `hasKeywords`                     | int               | Unsure. Probably implies that `Keyword`  |
|                                   |                   | records are available for this uuid,     |
|                                   |                   | though the relationship isn't currently  |
|                                   |                   | auto-generated.                          |
+-----------------------------------+-------------------+------------------------------------------+
