const wsUrl = "ws://" + window.location.host + "/ws";
const responseTypes = {"start": startWs,
    "changePartner": changePartner,
    "changeColor": changeColor,
    "disconnectPartner": disconnectPartner,
    "online": updateOnline,
    "message": newMessage}
let ws = null;

function setText(idEl, text) {
    let el = document.getElementById(idEl);
    el.innerText = text;
}

function startWs(uid) {
    setText("uid", uid);
}

function changePartner(pid) {
    setText("pid", pid);
    newMessage("New partner: " + pid);
}

function changeColor(color) {
    let colorEl = document.getElementById("colorNumber");
    newMessage("Partner changed your color #" + colorEl.innerText + " --> " + color);

    colorEl.innerText = color;

    let colorDiv = document.getElementById("color");
    colorDiv.style.backgroundColor = color;
}

function disconnectPartner(data) {
    let pid = document.getElementById("pid");
    pid.innerText = "Empty";
    setText("pid", "Empty");
    newMessage(data);
}

function updateOnline(count) {
    setText("onlineNumber", count)
}

function newMessage(message) {
    let events = document.getElementById("events");
    let newEvent = document.createElement("li");
    newEvent.innerText = message;
    events.appendChild(newEvent);
}

function buttonClick(event) {
    ws.send(this.dataset.t);
    console.log("button was pressed;")
    console.log(this.dataset.t);
    event.preventDefault();
}

// WS

function onOpen(event) {
    newMessage("You was connected.");
    event.preventDefault();
}

function onMessage(event) {
    let response = JSON.parse(event.data);

    if (!(response.type in responseTypes)) {
        console.error("Wrong type of response");
        return;
    }

    responseTypes[response.type](response.data);
    event.preventDefault();
}

function onClose(event) {
    console.log("WS was closed");
    console.log(event.data);

    newMessage("Sorry, but connection failed.")
    event.preventDefault();
}

function connect() {
    ws = new WebSocket(wsUrl);

    ws.onopen = onOpen;
    ws.onmessage = onMessage;
    ws.onclose = onClose;
}


connect();
let button = document.getElementById("nextPartner");
button.onclick = buttonClick;
button = document.getElementById("nextColor");
button.onclick = buttonClick;
