function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Contacts')
    .addItem('show Groups', 'showContactGroups')
    .addItem('add Contact', 'addContact')
    .addItem('test Contact', 'testContact')
    .addItem('saveIntoDriveStatic2', 'saveIntoDriveStatic2')
    .addItem('checkSimilarity', 'checkSimilarity')
    .addItem('setimportXML', 'setimportXML')
    .addToUi();
}

function showContactGroups() {
  var groups = ContactsApp.getContactGroups();
  var str = 'Groups\n';
  for (var g = 0; g < groups.length; g++) {
    str += '\n' + groups[g].getName()

  }

  showOutputBox(str, 'Your Contact Groups');
}


function addContact() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var cell = sheet.getActiveCell();
  var active_row = cell.getRow();
  var range = sheet.getDataRange();
  var exists = 0;
  const CNAME = 3;
  const CADDR = 4;
  const CTEL = 5;
  const CIMGSRC = 8;

  var first_name = range.getCell(active_row, 3).getValue();
  //    var last_name = range.getCell(active_row ,2).getValue();
  var email = ""; range.getCell(active_row, 3).getValue() + '@test.com'; // test email
  var last_name = "test";
  //    var email = "test@test.com";
  var gurl = range.getCell(active_row, 6).getValue();
  var tel = range.getCell(active_row, 5).getValue();
  var address = range.getCell(active_row, 4).getValue();
  var statusCell = range.getCell(active_row, 1);
  var contact;


  // This formats the date as Greenwich Mean Time in the format
  var formattedDate = Utilities.formatDate(new Date(), "GMT", "yy-MM");

  // check if group exists, create it otherwise
  if (mainGroup = ContactsApp.getContactGroup("import")) {
    // group exists
  }
  else {
    // create the group
    mainGroup = ContactsApp.createContactGroup("import");
    Logger.log("created group import");
  }

  var exists = 0;
  if (contact = ContactsApp.getContactsByPhone(tel)) {
    // phone number exists
    // check if name exists
    for (i = 0; i < contact.length; i++) {
      if (similarity(contact[i].getGivenName(), first_name) >= 0.7)
        exists++;
    }

  }

  // check if Name exists, create otherwise
  if (exists)  //Phone Number Exists
  {
    // contact exists
    Logger.log('Skipped existing Contact: ' + first_name + ' ' + last_name + ' | ' + (email.toString()) + ' already exists in ' + (mainGroup.getName()));
    showOutputBox('Skipped ' + first_name + ' last name ' + last_name + ' \ntel ' + tel, 'addcontact');

    return;
  } else {
    // create contact and add it to Group
    contact = ContactsApp.createContact(first_name, last_name, email);  // create contact
    Logger.log('Added Contact: ' + first_name + ' ' + last_name + ' | ' + (email.toString()) + ' added in ' + (mainGroup.getName()));
    mainGroup.addContact(contact);                                      // add contact to group
    statusCell.setValue(formattedDate);
    contact.addPhone(formattedDate, tel.toString());                    // add date label to tel nr
    contact.addUrl(formattedDate, gurl.toString());                    // add URL
    contact.addAddress(formattedDate, address.toString());                    // add address

    showOutputBox('Created ' + first_name + ' last name ' + last_name + ' \ntel ' + tel, 'addcontact');
    return contact;
  }
}

/******************************************************* */
function testContact() {
  /******************************************************* */
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = SpreadsheetApp.getActiveSheet();
  var cell = sheet.getActiveCell();
  var active_row = cell.getRow();
  var range = sheet.getDataRange();
  const CNAME = 3;
  const CADDR = 4;
  const CTEL = 5;
  const CIMGSRC = 8;

  var name = range.getCell(active_row, CNAME).getValue().toString().trim();
  var tel = range.getCell(active_row, CTEL).getValue();
  var addr = range.getCell(active_row, CADDR).getValue();
  var imgsrc = range.getCell(active_row, CIMGSRC).getValue();

  Logger.log('checking ' + name + ' ' + tel + ' ' + addr);// + ' ' + imgsrc);
//  ss.toast('checking ' + name + ' ' + tel, 'testContact');
  if (names=ContactsApp.getContactsByName(name).length)
    Logger.log(names+'x '+name+'s found');

  var contacts = ContactsApp.getContactsByPhone(tel);

  if (contacts.length > 0) {
    Logger.log(contacts.length + 'x tel found');

    for (i = 0; i < contacts.length; i++) {
      if (similarity(name, contacts[i].getGivenName()) > 0.7)
        Logger.log(name+'+phone MATCH');//+  contacts[i].getGivenName() +' MATCH *****');
      else
        Logger.log(name+' .. ' +contacts[i].getGivenName()+' ='+similarity(name, contacts[i].getGivenName() ) );

      Logger.log(contacts[i].getFullName()
        //        + ' id: ' + contacts[i].getId() + '\n'
       // + ' ' + contacts[i].getPhones()[0].getPhoneNumber().toString() 
        //       + '\n updated' + contacts[i].getLastUpdated()
        +' \nupdated ' + Utilities.formatDate(contacts[i].getLastUpdated(), "GMT", "yy-MM-dd")
      );
      if (contacts[i].getAddresses() > 0)
        Logger.log(contacts[0].getAddresses()[0].getAddress().toString());
    }
    ss.toast(
      contacts.length+' contacts found \n'
      + contacts[0].getFullName() //+ ' id: ' + contacts[0].getId().toString() + '\n'
      + contacts[0].getPhones()[0].getPhoneNumber().toString() +
      ' \nupdated ' + Utilities.formatDate(contacts[0].getLastUpdated(), "GMT", "yy-MM-dd")
    );

    return contacts[0];

  } else {
    ss.toast(name + ' with tel ' + tel+' is not in contacts','testContact');
    Logger.log('contact does not exist');
    return -1;
  }
}



function showOutputBox(str, title) {
  var html = HtmlService.createHtmlOutput('<pre>' + str + '</pre>')
    .setWidth(400)
    .setHeight(300);

  SpreadsheetApp.getUi()
    .showModalDialog(html, title);
}



function fdupSheetStatic(oldSheet) {
  const UL = 'A1';
  const LR = 'G350';
  var oldSheetName = oldSheet.getSheetName();
  var newSheetName = (new Date()).toLocaleDateString() + oldSheetName;
  var oldSs = oldSheet.getParent();
  var newSheet = oldSs.insertSheet(newSheetName);

  // create a new ss in the directory statics, if it does not exist
  // var newSs = SpreadsheetApp.create()

  Logger.log(newSheetName);

  //  var source.
  oldSheet.getRange(UL + ':' + LR).copyTo(newSheet.getRange(UL + ':' + LR), SpreadsheetApp.CopyPasteType.PASTE_VALUES, false);  // CHECK THIS
  oldSheet.getRange(UL + ':' + LR).copyTo(newSheet.getRange(UL + ':' + LR), SpreadsheetApp.CopyPasteType.PASTE_COLUMN_WIDTHS, false);
  oldSheet.getRange(UL + ':' + LR).copyTo(newSheet.getRange(UL + ':' + LR), SpreadsheetApp.CopyPasteType.PASTE_FORMAT, false);

  //Browser.msgBox('duplicated to static sheet');
  return newSheet;

}



function saveIntoDriveStatic2() {

  var oldSs = SpreadsheetApp.getActiveSpreadsheet();
  var oldSheet = SpreadsheetApp.getActiveSheet();
  var oldSheetName = oldSheet.getSheetName();

  folderId = '1tzbBQiRvNolmV36GKHUms7LXuFMGzToh';
  ssname = (new Date()).toLocaleDateString() + "booksusi";
  folder = DriveApp.getFolderById(folderId);

  newSheetName = (new Date()).toLocaleDateString() + oldSheetName;
  var newSs = createSpreadSheetInFolder(ssname, folder);

  // create "static" temp sheet
  var tempSheet = fdupSheetStatic(oldSheet);
  Logger.log("tempsheet created");

  Logger.log(oldSs.getName(), oldSheetName);
  Logger.log(newSs.getName(), newSheetName);

  var newSheet = tempSheet.copyTo(newSs);
  newSheet.setName(newSheetName);
  tempSheet.getParent().deleteSheet(tempSheet);

  Browser.msgBox('stored sheet to static spreadsheet');

  return newSheet;

}



function createSpreadSheetInFolder(name, folder) {

  var FileIterator = DriveApp.getFilesByName(name);
  while (FileIterator.hasNext()) {
    var file = FileIterator.next();
    if (file.getName() == name) {
      var ss = SpreadsheetApp.open(file);
      var id = file.getId();
      Logger.log("exists: ss");
      return ss;
    }
  }

  var ss = SpreadsheetApp.create(name);
  Logger.log("create: ss");
  var id = ss.getId();
  var file = DriveApp.getFileById(id);

  folder.addFile(file);

  return ss;

}


function checkSimilarity() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var cell = sheet.getActiveCell();
  var active_row = cell.getRow();
  var active_column = cell.getColumn();
  //  var range = sheet.getActiveRange();

  if (sheet.getRange(active_row, active_column).isBlank() ||
    sheet.getRange(active_row, active_column + 1).isBlank()) {
    Logger.log('cell NULL');
    return -1;
  }

  var str1 = sheet.getRange(active_row, active_column).getValue();
  var str2 = sheet.getRange(active_row, active_column + 1).getValue();
  Logger.log(str1 + ' ... ' + str2);
  similarity(str1, str2);
}

function similarity(s1, s2) {
  var longer = s1;
  var shorter = s2;
  if (s1.length < s2.length) {
    longer = s2;
    shorter = s1;
  }
  var longerLength = longer.length;
  if (longerLength == 0) {
    return 1.0;
  }
  var simpercentage = (longerLength - editDistance(longer, shorter)) / parseFloat(longerLength);
  /*  if (simpercentage >= 0.75)
      Logger.log('SIMILAR ' + simpercentage.toFixed(2) + '%');
    else
      Logger.log(simpercentage.toFixed(2) + '%');
  */
  return simpercentage.toFixed(2);
}

function editDistance(s1, s2) {
  s1 = s1.toLowerCase();
  s2 = s2.toLowerCase();

  var costs = new Array();
  for (var i = 0; i <= s1.length; i++) {
    var lastValue = i;
    for (var j = 0; j <= s2.length; j++) {
      if (i == 0)
        costs[j] = j;
      else {
        if (j > 0) {
          var newValue = costs[j - 1];
          if (s1.charAt(i - 1) != s2.charAt(j - 1))
            newValue = Math.min(Math.min(newValue, lastValue),
              costs[j]) + 1;
          costs[j - 1] = lastValue;
          lastValue = newValue;
        }
      }
    }
    if (i > 0)
      costs[s2.length] = lastValue;
  }
  return costs[s2.length];
}

function setimportXML(url, xpath, row, column) {

  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getActiveSheet();
  var cell = sheet.getActiveCell();
  ss.toast('setimportXML', 'function', 2);

  SpreadsheetApp.getActiveSheet.toString()
  //a6.setValue('=ImportXML("https://litecoin.miningpoolhub.com/index.php?page=api&action=getuserbalance&")');
  Logger.log('function setimportXML in ' + ss.getName() + '/' + sheet.getName() + '/' + cell.getA1Notation());
  Logger.log('url ' + url + ', xpath ' + xpath);
  return ('setimportxml output');

}


function addContactWithPhoto() {
  const familyName = 'Mustermann';
  const givenName = 'Max';
  const emailAddress = 'max@mustermann.com';
  const imageUrl = 'https://booksusi.com/files/1/53101/square.jpg';

  // 1. Create contact.
  const resource1 = { emailAddresses: [{ value: emailAddress }], names: [{ familyName: familyName, givenName: givenName }] }
  const resourceName = People.People.createContact(resource1).resourceName;
  
  // 2. Add cover photo to the created contact.
  const resource2 = { photoBytes: Utilities.base64Encode(UrlFetchApp.fetch(imageUrl).getContent()), personFields: "coverPhotos" };
  People.People.updateContactPhoto(resource2, resourceName);
}
