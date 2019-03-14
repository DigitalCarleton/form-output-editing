/**
 * Generates the properties that this script needs to run. MUST be run manually when
 * attaching to a new Form response Spreadsheet.
 * To run this function manually, click the "Select function" dropdown menu above,
 * choose genProperties, and hit "Run" (the play button to the left).
 */
function genProperties() {
  var defaultProperties = {
    "UPLOAD_FIELD": "Image Upload",
    "FILENAME_FIELD": "Filename"
  };
  var documentProperties = PropertiesService.getDocumentProperties();
  documentProperties.setProperties(defaultProperties);
}

/**
 *
 */
function setupSheet(sheet, documentProperties) {
  // Retrieve document properties
  var uploadField = documentProperties.getProperty("UPLOAD_FIELD");
  var filenameField = documentProperties.getProperty("FILENAME_FIELD");
  // Retrieve sheet metadata
  var rows = sheet.getLastRow();
  var cols = sheet.getLastColumn();
  // Retrieve the headers on the sheet
  var headers = sheet.getRange(1, 1, 1, cols).getValues()[0];
  
  // Find upload field index and save property
  var uploadIndex = headers.indexOf(uploadField) + 1;
  if (uploadIndex < 1) throw uploadField + "not found";
  documentProperties.setProperty("UPLOAD_INDEX", uploadIndex);
  
  // Find/create filename field index and save property
  var filenameIndex = headers.indexOf(filenameField) + 1;
  if (filenameIndex < 1) {
    // Generate filename column
    filenameIndex = cols + 1; // Next available column
    var headerCell = sheet.getRange(1, filenameIndex);
    headerCell.setValue(filenameField);
  }
  documentProperties.setProperty("FILENAME_INDEX", filenameIndex);
  
  // Update all current entries before the most recent (if any)
  for (var row = 2; row < rows; row++) {
    addFilename(row, sheet, uploadIndex, filenameIndex);
  }
}

/**
 * Fetches the filename of a file by its Drive URL using DriveApp.
 */
function getFilename(driveUrl) {
  driveUrl = driveUrl.toString();
  var idIndex = driveUrl.lastIndexOf("=") + 1;
  var driveId = driveUrl.slice(idIndex);
  var file = DriveApp.getFileById(driveId);
  var filename = file.getName();
  
  return filename;
}

/**
 * Retrieves the filename of a file submission, the URL of
 * which resides in the uploadIndex column, and inserts this
 * value in the filenameIndex column.
 */
function addFilename(row, sheet, uploadIndex, filenameIndex) {
  // Retrieve upload URL from sheet, and get filename
  var uploadCell = sheet.getRange(row, uploadIndex);
  var filename = getFilename(uploadCell.getValue());
  
  // Push filename to sheet
  var filenameCell = sheet.getRange(row, filenameIndex);
  filenameCell.setValue(filename);
}

/**
 *
 */
function onFormSubmit(e) {
  // Retrieve metadata
  var documentProperties = PropertiesService.getDocumentProperties();
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  // Initialize index properties if uninitialized
  if (!("UPLOAD_INDEX" in documentProperties.getKeys()) || !("FILENAME_INDEX" in documentProperties.getKeys())) {
    setupSheet(sheet, documentProperties);
  }
  var uploadIndex = documentProperties.getProperty("UPLOAD_INDEX");
  var filenameIndex = documentProperties.getProperty("FILENAME_INDEX");
  
  // Update the newest submission
  var activeRow = sheet.getLastRow();
  addFilename(activeRow, sheet, uploadIndex, filenameIndex);
}