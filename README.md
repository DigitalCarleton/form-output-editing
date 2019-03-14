# Form Output Editing - Carleton DHA

Form Output Editing is a project by the Digital Humanities Associates at Carleton College intended to 
make Google Forms outputs easier to use, particularly in conjunction with other digital tools.

## filename-append/

Filename Append is a prototype Google Apps Script that makes the name of files uploaded via the File
Upload response type available in the response Spreadsheet. Currently must be copied and pasted into
a Script attached to the Spreadsheet collecting responses to the Form.

For more, see the README in `filename-append/`.

**NOTE**: This project may well be later deprecated in favor of a Spreadsheets Add-on with the same functionality.

## form-output-editor/

Form Output Editor contains a primary Python script and its supporting frameworks, which allow the
user to generate edited versions of the outputs of a Form. This currently includes: managing field names,
removing unwanted fields, and managing filenames of uploaded files.

For more, see the README in `form-output-editor/`.

**NOTE**: Currently only available for Python3.
