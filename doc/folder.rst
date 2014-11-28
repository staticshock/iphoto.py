Properties of folder records
============================

+-----------------------------------------+------------+--------------------------------------------+
| Property                                | Type       | Description                                |
+=========================================+============+============================================+
| `modelId`                               | int        | Internal primary key (not that useful.)    |
+-----------------------------------------+------------+--------------------------------------------+
| `uuid`                                  | str        | A unique key referenced by other tables    |
|                                         |            | (useful for  recognizing relationships.)   |
+-----------------------------------------+------------+--------------------------------------------+
| `folderType`                            | integer    | Ths is 1 for internal folders, 2 for       |
|                                         |            | regular album folders.                     |
+-----------------------------------------+------------+--------------------------------------------+
| `name`                                  | str        | If the album is named, the name is copied  |
|                                         |            | here, but for all other albums this is "". |
+-----------------------------------------+------------+--------------------------------------------+
| `parentFolderUuid`                      | str        | For events and other top level folders,    |
|                                         |            | this is a string representing some         |
|                                         |            | internal folder that serves as the parent. |
+-----------------------------------------+------------+--------------------------------------------+
| `parentFolder`                          | Folder[]   | The parent `Folder` record.                |
+-----------------------------------------+------------+--------------------------------------------+
| `childFolders`                          | Folder[]   | All the child `Folder` record.             |
+-----------------------------------------+------------+--------------------------------------------+
| `versions`                              | Versions[] | All the associated `Version` records.      |
+-----------------------------------------+------------+--------------------------------------------+
| `implicitAlbumUuid`                     | str        | Uuid of the associated `Album` record.     |
+-----------------------------------------+------------+--------------------------------------------+
| `album`                                 | Album      | The associated `Album` record.             |
+-----------------------------------------+------------+--------------------------------------------+
| `posterVersionUuid`                     | str        | Uuid of the `Version` record used as the   |
|                                         |            | "Key Photo" for the album.                 |
+-----------------------------------------+------------+--------------------------------------------+
| `masters`                               | Master[]   | All the associated `Master` records.       |
+-----------------------------------------+------------+--------------------------------------------+
| `automaticallyGenerateFullSizePreviews` | integer    | Unsure. For me, this is always 1 unless    |
|                                         |            | `folderType` is 1.                         |
+-----------------------------------------+------------+--------------------------------------------+
| `versionCount`                          | integer    | Number of photos in the folder.            |
+-----------------------------------------+------------+--------------------------------------------+
| `minImageTimeZoneName`                  | str        | Unsure. Presumably this sorts images by    |
|                                         |            | UTC offset, but my images are always GMT.  |
+-----------------------------------------+------------+--------------------------------------------+
| `maxImageTimeZoneName`                  | str        | Counterpart to `minImageTimeZoneName`.     |
+-----------------------------------------+------------+--------------------------------------------+
| `minImageDate`                          | datetime   | Min `imageDate` in folder.                 |
+-----------------------------------------+------------+--------------------------------------------+
| `maxImageDate`                          | datetime   | Max `imageDate` in folder.                 |
+-----------------------------------------+------------+--------------------------------------------+
| `folderPath`                            | str        | Unsure. Seems to have nothing in common    |
|                                         |            | with physical file system paths.           |
+-----------------------------------------+------------+--------------------------------------------+
| `createDate`                            | datetime   | Unsure.                                    |
+-----------------------------------------+------------+--------------------------------------------+
| `isExpanded`                            | integer    | 1 if the folder is expanded in the UI, 0   |
|                                         |            | otherwise.                                 |
+-----------------------------------------+------------+--------------------------------------------+
| `isHidden`                              | integer    | Unsure. If this is about hiding an album,  |
|                                         |            | I don't know how to access that feature    |
|                                         |            | from the UI.                               |
+-----------------------------------------+------------+--------------------------------------------+
| `isHiddenWhenEmpty`                     | integer    | Unsure. For me this value is 1 for the "My |
|                                         |            | Photo Stream" folder, but 0 for everything |
|                                         |            | else.                                      |
+-----------------------------------------+------------+--------------------------------------------+
| `isFavorite`                            | integer    | Unsure. This is always 0 for me, and I see |
|                                         |            | no way to mark an album as a "favorite"    |
|                                         |            | from the UI.                               |
+-----------------------------------------+------------+--------------------------------------------+
| `isInTrash`                             | integer    | 1 if the associated album has been         |
|                                         |            | discarded, 0 otherwise.                    |
+-----------------------------------------+------------+--------------------------------------------+
| `isMagic`                               | integer    | Identifies special folders. This seems to  |
|                                         |            | include everything with `folderType` = 1,  |
|                                         |            | but also "My Photo Stream".                |
+-----------------------------------------+------------+--------------------------------------------+
| `colorLabelIndex`                       | integer    | Unsure.                                    |
+-----------------------------------------+------------+--------------------------------------------+
| `sortAscending`                         | integer    | Unsure. This defaults to 1, but I don't    |
|                                         |            | know if 0 implies "descending" or "custom  |
|                                         |            | sorting".                                  |
+-----------------------------------------+------------+--------------------------------------------+
| `sortKeyPath`                           | str        | This defaults to the string "custom.kind"  |
|                                         |            | for most things, and "custom.default" for  |
|                                         |            | a couple of internal folders.              |
+-----------------------------------------+------------+--------------------------------------------+
