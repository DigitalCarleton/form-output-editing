# Filename Append

This subproject focuses on making the filename available in the results Spreadsheet when
choosing to include a File Upload option on a Form.

Natively, Forms will populate a File Upload field with links to the uploaded files. While
this may be useful online, it is limiting when trying to work with Form outputs offline,
especially when attempting to attribute files to submitters. This issue grows in relevance
as the number of submissions grows.

The provided script, `FilenameAppend.gs`, will retrieve these filenames and append them in
a new field.

## How to Use

### Step 1: Open a new Google form with option to "upload file" enabled

![upload-enabled-google-form](./screenshots/form_example.png?raw=true "Form example")

### Step 1: Link a Google Sheet to the form

![how-to-link-form](./screenshots/link_form_sheet.png?raw=true "Linking example")

![sheet-before-script](./screenshots/sheet_before_script.png?raw=true "Sheet before script is ran")

### Step 2: Attach the Script (Copy-Paste) into Sheet's Script Editor

![sheet-script-editor](./screenshots/sheet_script_editor.png?raw=true "How to get to script editor in Sheet")

![sheet-editor-pasted](./screenshots/sheet_editor_pasted.png?raw=true "Script editor after code is pasted")

### Step 2b: make sure to SAVE editor after script has been copied over (step 3 will be greyed out otherwise)

![save-script-editor](./screenshots/save_script.png?raw=true "Save editor")

### Step 3: Run manualUpdate function (Google will ask to enable permission for the first run)

![run-manual-update](./screenshots/run_manual_update.png?raw=true "Run manual update")

#### Check result (note: there should be a new column titled "Upload file here (Filename)". Title will follow "<image_name>-<author>.<file_extension> format).

![sheet-after-script-is-ran](./screenshots/sheet_after_script.png?raw=true "Sheet after manualUpdate is ran")

## Auto update on submission

To enable auto update, bind autoUpdate function to "On form submit" trigger

### Step 1: Navigate to Triggers panel

![navigate-to-triggers-top-left](./screenshots/script_trigger.png?raw=true "Navigating to Trigger function")

### Step 2: Add Trigger (bottom right corner)

![add-trigger-bottom-right-blue-button](./screenshots/add_trigger.png?raw=true "Adding new trigger")

### Step 3: Configure trigger to fire manualUpdate "On form submit"

![add-trigger-bottom-right-blue-button](./screenshots/add_trigger.png?raw=true "Adding new trigger")
![trigger-configuration-for-manualUpdate-onFormSubmit](./screenshots/trigger_setting.png?raw=true "Trigger configuration to fire function "On form submit")

## Known Issues

-

## Changelog

Versions are listed most recent to least recent.

### Version 0.0.1:
