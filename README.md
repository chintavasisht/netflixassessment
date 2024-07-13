# Summary

#### This project contains the following python scripts in the scripts folder

- root_report.py -> This generates a report of total folders and files at the root.
- recursive_report.py -> This generates a report of child objects (recursively) for each top-level folder under the source folder id. Additionally it also generates total nested folders for the source folder.
- copy_contents.py -> This copies all contents of the source to a target folder.

**Additional information**
- Utils folder contains authentication function as well as a source config file for the scripts.
- All of the tasks make use of a OAuth 2.0 based login workflow. 