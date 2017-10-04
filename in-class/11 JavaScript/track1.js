var myList = document.getElementById("todolist");
var text = document.getElementById("textfield");
var myBtn = document.getElementById("addBtn");


function addItem(){
    var newList = document.createElement("li");
    newList.innerHTML = text.value;
    myList.appendChild(newList);
}

myBtn.addEventListener("click", addItem);