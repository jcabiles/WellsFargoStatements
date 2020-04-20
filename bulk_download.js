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
