/**
 * A simple replicable script that auto-detects Drive file URLs in a Form
 * response Spreadsheet and provides the associated filenames.
 * * * *
 * To use, copy into the script editor of a Form response Spreadsheet, then:
 * (1) Run manualUpdate() (and grant permissions to this script)
 * (2) Attach autoUpdate() to the "On Form Submit" event
 * Further instructions are available on the functions in question.
 * * * *
 * @author Luna Yee (yeec@carleton.edu), Carleton Digital Humanitiesh
 */

/**
 * MANUALLY RUN THIS FUNCTION
 * --------------------------
 * Run this function with the container spreadsheet open to manually update
 * filenames for all rows in the spreadsheet.
 * * * *
 * To run this function manually:
 * (1) From "Select function" dropdown menu above, choose "manualUpdate"
 * (2) Click "Run" (the play button to the left of the dropdown menu)
 */
function manualUpdate() {
	// Retrieve metadata
	var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
	// Update values
	update(sheet);
}

/**
 * ATTACH THIS FUNCTION TO THE "ON FORM SUBMIT" EVENT
 * --------------------------------------------------
 * This method will automatically update the container spreadsheet with
 * filenames whenever a form is submitted.
 * * * *
 * To attach this function to the "On form submit" event:
 * (1) Click the arrow icon in upper left, "Google Apps Script Dashboard"
 * (2) Right-click this script and choose "Triggers"
 * (3) Click "+ Add Trigger" in the bottom right
 * (4) For "Choose which function to run", choose "autoUpdate"
 * (5) For "Select event type", choose "On form submit"
 * (6) Review "Failure notification settings" and hit "Save"
 * WARNING: Run manualUpdate FIRST to grant permissions to this script
 * * * *
 * @param e Event details
 */
function autoUpdate(e) {
	// Retrieve metadata
	var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
	// Update the submission row
	var row = e.range.getRow();
	if (row > sheet.getLastRow()) throw "Row index out of bounds: " + row;
	updateRow(sheet, row);
}

// SUPPORTING METHODS

/**
 * Checks whether the value is a valid, accessible Drive URL.
 * @param value
 * @return true if usable Drive URL; false otherwise
 */
function isDriveFile(value) {
	if (value == null) return false;
	value = value.toString();
	// Check if Drive URL
	if (value.indexOf("https://drive.google.com/open?id=") === -1) return false;
	// Check if valid and accessible
	var driveId = value.slice(value.indexOf("=") + 1);
	try {
		var file = DriveApp.getFileById(driveId);
	} catch (err) {
		return false;
	}
	return true;
}

/**
 * Fetches the filename of a file by its Drive URL using DriveApp.
 * @param driveUrl URL of the Drive file
 * @return string filename of the Drive file
 */
function getFilename(driveUrl) {
	driveUrl = driveUrl.toString();
	var driveId = driveUrl.slice(driveUrl.indexOf("=") + 1);
	var file = DriveApp.getFileById(driveId);

	return file.getName();
}

/**
 * Updates a single row in the sheet with filenames of any Drive
 * files.
 * @param sheet Form response sheet of the Spreadsheet
 * @param row Row of the submission to update
 */
function updateRow(sheet, row) {
	// Retrieve sheet data
	var rows = sheet.getLastRow();
	var cols = sheet.getLastColumn();
	var headers = sheet.getRange(1, 1, 1, cols).getValues()[0];
	var activeRow = sheet.getRange(row, 1, 1, cols).getValues()[0];

	// Search through active row for drive files
	for (var col = 1; col <= cols; col++) {
		var value = activeRow[col - 1];
		if (isDriveFile(value)) {
			var rawFilename = getFilename(value);
			var filename = rawFilename.replace(/\s/g, "_");
			var activeHeader = headers[col - 1] + " (Filename)";
			// If there is no existing filename field for this header, add one
			if (headers.indexOf(activeHeader) == -1) {
				sheet.insertColumnAfter(col);
				headers.splice(col, 0, activeHeader);
				sheet.getRange(1, col + 1).setValue(activeHeader);
			}
			// Add filename
			var filenameIndex = headers.indexOf(activeHeader) + 1;
			sheet.getRange(row, filenameIndex).setValue(filename.length);
			sheet.getRange(row, filenameIndex + 1).setValue(filename);
		}
	}
}

/**
 * Updates all rows in the sheet with filenames of any Drive
 * files.
 * @param sheet Form response sheet of the Spreadsheet
 */
function update(sheet) {
	// Update every row
	var rows = sheet.getLastRow();
	if (rows > 1) {
		for (var i = 2; i <= rows; i++) {
			updateRow(sheet, i);
		}
	}
}
