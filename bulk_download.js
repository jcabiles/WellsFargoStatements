/**
 * This script is based on the following thread: https://gist.github.com/binary1230/7cfa0524d0fae7c320e3b15fc1f4f64c
 *
 * To use it, follow these steps:
 * 1) In Chrome browser, navigate to your Wells Fargo Statement Viewer and pull up the set of PDFs you want to view
 * 2) Press F12 to open the developer tools and click the tab at the bottom that says 'Console'
 * 3) In the developer console, paste the code that is shown under "Create the functions" section.  Then press ENTER.
 * 4) Select the calendar year for which you want to download statements
 * 5) Type this command in the developer console: openAll(lastResponse);
 * 6) Press ENTER.  You'll know you were successful when a bunch of browser tabs open up.
 *      Note: make sure that AdBlock allows you to open these tabs
 * 7) Download the PDF files.  It might make later steps easier if you follow this naming convention: "yyyy-mm.pdf" 
 * 8) Repeat steps 4-6 as needed
 *
 */
 

/* Create functions to facilitate bulk downloads */
function parseWFData(str) {
  str = str.substr(24);
  str = str.substr(0, str.length - 24);
  str = str.replace(/\\"/g, '"');
  return JSON.parse(str);
}

var lastResponse = "";
var lastXHR;
function handleResponse(xhr) {
  if (xhr.responseURL.indexOf('edocs/documents/statement/list') !== -1) {
    lastXHR = xhr;
    lastResponse = parseWFData(xhr.responseText);
  }
}

var xopen = XMLHttpRequest.prototype.open;
XMLHttpRequest.prototype.open = function() {
    this.addEventListener("readystatechange", function(event){
      var xhr = event.target;
      if (xhr.readyState === 4) { handleResponse(xhr); }
    });
    xopen.apply(this, arguments);
}

function extractWFUrls(json) {
    return json.statementsDisclosuresInfo.statements.map(data => data.url);
}

function openAll(payload) {
    var urls = extractWFUrls(payload);
    urls.forEach(function(url){ window.open(url); });
};


/* Make sure to run this script once you finish */
