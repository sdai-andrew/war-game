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
        if (xhr.readyState !== 4) return;
        displayGamePage(xhr);
    }

    xhr.open("POST", `/play-game/${p1Name}/${p2Name}`, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(`csrfmiddlewaretoken=${getCSRFToken()}`);
}

function getCSRFToken() {
    let cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length);
        }
    }
    return "unknown";
}

function displayGamePage(xhr) {
    if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText);
        displayGame(response.moves);
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

function displayGame(moves) {
    const intervalID = setInterval(displayMove, 1000);
    let index = 0;
    function displayMove() {
        if (index >= moves.length) {
            clearInterval(intervalID);
            return;
        }
        let move = moves[i];
        let headerDiv = document.getElementById("header-div");
        let p2DeckDiv = document.getElementById("player-2-deck-div");
        let p2PlayDiv = document.getElementById("player-2-play-div");
        let p1DeckDiv = document.getElementById("player-1-deck-div");
        let p1PlayDiv = document.getElementById("player-1-play-div");
        headerDiv.innerHTML = move.status;
        if (move.p1numcards >= 1) {
            p1DeckDiv.style.backgroundColor = "Gray";
            p1DeckDiv.innerHTML = move.p1numcards;
        } else if (move.p1numcards === 0) {
            // make deck transparent to mimic empty deck
            p1DeckDiv.style.backgroundColor = "rgba(255, 255, 255, 0)";
            p1DeckDiv.style.borderColor = "rgba(255, 255, 255, 0)";
            p1DeckDiv.innerHTML = ``;
        }
        if (move.p1numcards >= 1) {
            p2DeckDiv.style.backgroundColor = "Gray";
            p2DeckDiv.innerHTML = move.p2numcards;
        } else if (move.p1numcards === 0) {
            // make deck transparent to mimic empty deck
            p2DeckDiv.style.backgroundColor = "rgba(255, 255, 255, 0)";
            p2DeckDiv.style.borderColor = "rgba(255, 255, 255, 0)";
            p2DeckDiv.innerHTML = ``;
        }
        let oneCard = move.p1card;
        let twoCard = move.p2card;
        if (oneCard.isfaceup === "True") {
            p1PlayDiv.innerHTML = `${oneCard.value} of ${oneCard.suit}`;
            p1PlayDiv.style.backgroundColor = "White";
        } else if (oneCard.isfaceup === "False") {
            p1PlayDiv.innerHTML = ``;
            p1PlayDiv.style.backgroundColor = "Gray";
        }
        if (twoCard.isfaceup === "True") {
            p2PlayDiv.innerHTML = `${twoCard.value} of ${twoCard.suit}`;
            p2PlayDiv.style.backgroundColor = "White";
        } else if (oneCard.isfaceup === "False") {
            p2PlayDiv.innerHTML = ``;
            p2PlayDiv.style.backgroundColor = "Gray";
        }
    }
}