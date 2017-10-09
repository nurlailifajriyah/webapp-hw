var req

var button = document.getElementById("Btn");
var content = document.getElementById("content");

function getFortune() {
   if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange = handleResponse;
    req.open("GET", "http://garrod.isri.cmu.edu/webapps/fortune/", true);
    req.send();
}

button.addEventListener("click", getFortune);

function handleResponse() {
    if (req.readyState != 4 || req.status != 200) {
        return;
    }

    // Removes the old to-do list items



    // Parses the response to get a list of JavaScript objects for
    // the items.
    var items = JSON.parse(req.responseText);
    content.innerHTML = items['fortune'];


}

