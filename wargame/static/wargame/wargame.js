function checkWins() {
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4) return;
        updateHome(xhr);
    }
    let name_input = document.getElementById("check-wins-input");
    if (name_input == null) {
        return;
    }
    let player_name = name_input.value;
    xhr.open("GET", `/get-wins/${player_name}`, true);
    xhr.send();
}

function updateHome(xhr) {
    if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText);
        updateWins(response);
        return;
    }
    if (xhr.status === 0) {
        displayError("Cannot connect to server");
        return;
    }
    if (!xhr.getResponseHeader('content-type') === 'application/json') {
        displayError(`Received status = ${xhr.status}`);
        return;
    }
    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error);
        return;
    }
    displayError(response);
}

function displayError(message) {
    console.log(message);
}

function updateWins(response) {
    let div = document.getElementById("wins-div")
    if (div == null) {
        displayError("Can't find wins-div");
        return;
    }
    if (response.player_exists === "true") {
        div.innerHTML = `Player ${response.player_name} has ${response.wins} wins`;
    } else {
        div.innerHTML = `Player named ${response.player_name} does not exist!`;
    }   
}

function getGame(p1Name, p2Name) {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState !== 4) return
        displayGamePage(xhr)
    }

    xhr.open("POST", `/play-game/${p1Name}/${p2Name}`, true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhr.send(`csrfmiddlewaretoken=${getCSRFToken()}`)
}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}

function displayGamePage(xhr) {
    if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText);
        displayGame(response);
        return;
    }
    if (xhr.status === 0) {
        displayError("Cannot connect to server");
        return;
    }
    if (!xhr.getResponseHeader('content-type') === 'application/json') {
        displayError(`Received status = ${xhr.status}`);
        return;
    }
    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error);
        return;
    }
    displayError(response);
}