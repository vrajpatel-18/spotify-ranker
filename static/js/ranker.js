let totalSongs;
let loggedIn;
let userId;
// Check if user is logged in
function getUserInfo(callback) {
    $.ajax({
        type: 'GET',
        url: `/user-info`,
        success: function (data) {
            if (JSON.stringify(data) !== '{}') {
                loggedIn = true;
                callback(data);
            } else {
                loggedIn = false;
            }
        }
    });
}
function getUserInfoPromise() {
    return new Promise((resolve, reject) => {
        getUserInfo(data => {
            if (JSON.stringify(data) !== '{}') {
                let accountEl = document.querySelector('.account');
                userId = data['id'];
                accountEl.querySelector('.account-text').innerHTML = data['display_name'];
                accountEl.querySelector('.account-icon').src = data['images'][1]['url'];
                resolve(data);
            } else {
                reject('No user data found');
            }
        });
    });
}


let originalSongs;
let cards = document.querySelector('.songs-container');
let songList = new Sortable(cards, {
    group: 'shared',
    draggable: '.list-song',
    animation: 200,
    ghostClass: 'hidden',
    dragClass: 'active',
    forceFallback: true,
    onAdd: function (evt) { // when song moves from right to left
        removeNumber();
        addSongToOriginal(evt.item);
        assignDoubleClick();
    },
    onEnd: function (evt) {

    },
});

let list = document.querySelector('.list-song-container');
let rankList = new Sortable(list, {
    group: 'shared',
    draggable: '.list-song',
    animation: 200,
    ghostClass: 'hidden',
    dragClass: 'active',
    forceFallback: true,
    onAdd: function (evt) { // when song moves from left to right
        addNumber();
        removeSongFromOriginal(evt.item);

    },
    onEnd: function (evt) {

    },
});


function addNumber() {
    let numbers = document.querySelectorAll('.list-number-text');
    if (numbers.length != 0) {
        let lastNumber;
        numbers.forEach(function (number) {
            lastNumber = Number(number.innerHTML);
        });
        let htmlData = `
            <div class="list-number">
                <h3 class="list-number-text">${lastNumber + 1}</h3>
            </div>
        `;
        document.querySelector('.list-number-container').insertAdjacentHTML('beforeend', htmlData);
    } else {
        let htmlData = `
            <div class="list-number">
                <h3 class="list-number-text">1</h3>
            </div>
        `;
        document.querySelector('.list-number-container').insertAdjacentHTML('beforeend', htmlData);

    }
}

function removeNumber() {
    let numbers = document.querySelectorAll('.list-number');
    let lastNumber;
    numbers.forEach(function (number) {
        lastNumber = Number(number.querySelector('.list-number-text').innerHTML);
    });
    numbers.forEach(function (number) {
        if (Number(number.querySelector('.list-number-text').innerHTML) === lastNumber) {
            number.remove();
        }
    });
}



document.querySelector('.options-add').addEventListener('click', addAllSongs);

document.querySelector('.options-remove').addEventListener('click', removeAllSongs);

function addAllSongs() {
    // add all songs
    let length = document.querySelector('.songs-container').querySelectorAll('.list-song').length;
    let songs = document.querySelector('.songs-container').querySelectorAll('.list-song');
    songs.forEach(function (song) {
        let htmlData = `
        <div id="${song.id}" class="${song.classList}">
            <div class="list-song-img-container"><img src="${song.querySelector(".list-song-img").src}" class="list-song-img"></div>
            <div class="list-song-info" id="${song.querySelector(".list-song-info").id}">
                <h3 class="list-song-title">${song.querySelector(".list-song-title").innerHTML}</h3>
                <h4 class="list-song-break">|</h4>
                <h6 class="list-song-artist">${song.querySelector(".list-song-artist").innerHTML}</h4>
            </div>
            <div class="list-song-lines-container"><img src="../static/images/lines.png" class="list-song-lines"></div>
        </div>
        `;
        document.querySelector('.list-song-container').insertAdjacentHTML('beforeend', htmlData);
        song.remove();
        removeSongFromOriginal(song);
    });
    // add all numbers
    for (let i = 1; i <= length; i++) {
        addNumber();
    }
}

function removeAllSongs() {
    // remove all numbers
    let numbers = document.querySelector('.list-number-container').querySelectorAll('.list-number');
    numbers.forEach(function (number) {
        number.remove();
    });
    // remove all songs
    let songs = document.querySelector('.list-song-container').querySelectorAll('.list-song');
    songs.forEach(function (song) {
        let htmlData = `
        <div id="${song.id}" class="${song.classList}">
            <div class="list-song-img-container"><img src="${song.querySelector(".list-song-img").src}" class="list-song-img"></div>
            <div class="list-song-info" id="${song.querySelector(".list-song-info").id}">
                <h3 class="list-song-title">${song.querySelector(".list-song-title").innerHTML}</h3>
                <h4 class="list-song-break">|</h4>
                <h6 class="list-song-artist">${song.querySelector(".list-song-artist").innerHTML}</h4>
            </div>
            <div class="list-song-lines-container"><img src="../static/images/lines.png" class="list-song-lines"></div>
        </div>
        `;
        document.querySelector('.songs-container').insertAdjacentHTML('beforeend', htmlData);
        song.remove();
        addSongToOriginal(song);
    });
    assignDoubleClick();
}

document.querySelector(".search-bar").addEventListener("input", function () {
    updateSearch();
})

function updateSearch() {
    let search = document.querySelector(".search-bar").value;
    let items = document.querySelector('.songs-container');
    while (items.firstChild) items.removeChild(items.firstChild);
    let newSongs = [];
    originalSongs.forEach(function (song) {
        let songInfo = song.classList.value.replace('list-song ', '') + " " + song.querySelector('.list-song-title').innerHTML + " " + song.querySelector('.list-song-artist').innerHTML;
        if (searchType == 'artist') songInfo = songInfo.replace(document.querySelector('.list-title').innerHTML, '');
        else if (searchType == 'album') {
            let artist = song.querySelector('.list-song-artist');
            if (artist) {
                artist = artist.innerHTML;
                let index = artist.indexOf(',');
                if (index != -1) artist = artist.substring(0, index);
                songInfo = songInfo.replace(artist, '');
            }
        }
        songInfo = songInfo.replace(',', '').replace('.', '').replace('(', '').replace(')', '').replace("'", '');
        if (songInfo.toLowerCase().includes(search.toLowerCase())) {
            newSongs.push(song);
        }
    });
    newSongs.forEach(function (song) {
        document.querySelector('.songs-container').appendChild(song);
    });
    assignDoubleClick();
}

function clearSearch() {
    document.querySelector(".search-bar").value = "";
    let items = document.querySelector('.songs-container');
    while (items.firstChild) items.removeChild(items.firstChild);
    originalSongs.forEach(function (song) {
        document.querySelector('.songs-container').appendChild(song);
    });
    assignDoubleClick();
}

function removeSongFromOriginal(songEl) {
    let newSongs = [];
    if (originalSongs) {
        originalSongs.forEach(function (song) {
            if (songEl.id != song.id) {
                newSongs.push(song);
            }
        });
        originalSongs = newSongs;
    }
}

function addSongToOriginal(songEl) {
    originalSongs.forEach(function (song) {
        if (songEl.id == song.id) {
            return;
        }
    });
    originalSongs.push(songEl);
}

function doubleClick(song) {
    $(song).off("dblclick");
    $(song).on("dblclick", function () {
        let htmlData = `
            <div id="${song.id}" class="${song.classList}">
                <div class="list-song-img-container"><img src="${$(song).find(".list-song-img").attr("src")}" class="list-song-img"></div>
                <div class="list-song-info" id="${$(song).find(".list-song-info").id}">
                    <h3 class="list-song-title">${$(song).find(".list-song-title").html()}</h3>
                    <h4 class="list-song-break">|</h4>
                    <h6 class="list-song-artist">${$(song).find(".list-song-artist").html()}</h4>
                </div>
                <div class="list-song-lines-container"><img src="../static/images/lines.png" class="list-song-lines"></div>
            </div>
        `;
        $('.list-song-container').append(htmlData);
        $(song).remove();
        addNumber();
        let el = document.createElement("div");
        el.id = song.id;
        removeSongFromOriginal(el);
    });
}


function assignDoubleClick() {
    let songs = $('.songs-container').find('.list-song');
    for (let i = 0; i < songs.length; i++) {
        doubleClick(songs[i]);
    }
}

function getData(search, type, callback) {
    insertLoading();
    $.ajax({
        type: 'POST',
        url: `/${type}-songs`,
        data: { 'search': search },
        success: function (data) {
            data = JSON.parse(data);
            callback(data);
        }
    });
}



function buildSongs() {
    return new Promise((resolve, reject) => {
        document.querySelector('.songs-container').innerHTML = '';
        getData(searchID, searchType, function (data) {
            removeLoading();
            if (data['songs'].length == 0) {
                insertNoResults();
            } else {
                if (searchType == 'album') {
                    data['songs'].forEach(function (song) {
                        song['album'] = "";
                    });
                }
                let resultContainer = document.querySelector('.songs-container');
                data['songs'].forEach(function (song) {
                    let artists = song['artists'].join(', ');
                    let songType = song['type'] ? `id=${song['type']}` : '';
                    let htmlData = `
                <div id="${song['id']}" class="list-song ${song['album']}">
                    <div class="list-song-img-container"><img src="${song['img']}" class="list-song-img"></div>
                    <div class="list-song-info"${songType}>
                        <h3 class="list-song-title">${song['name']}</h3>
                        <h4 class="list-song-break">|</h4>
                        <h6 class="list-song-artist">${artists}</h4>
                    </div>
                    <div class="list-song-lines-container"><img src="../static/images/lines.png" class="list-song-lines"></div>
                </div>
                `;
                    resultContainer.insertAdjacentHTML('beforeend', htmlData);
                });
                assignDoubleClick();
                document.querySelector('.search-bar').classList.remove('hidden');
                originalSongs = Array.from(document.querySelector('.songs-container').querySelectorAll('.list-song'));
                totalSongs = originalSongs.length;
            }
            resolve();
        });
    });
}



// 12 characters or less: padding-left: 8%, font-size: 72px
// 13 characters: padding-left: 4%, font-size: 72px
// 14 characters: padding-left: 0, font-size: 72px
// 15 characters or more: padding-left: 0, font-size: 64px





// ON READY
let searchID = document.querySelector('.list-title').id;
let searchType = document.querySelector('.ranker-body').id;
let title = document.querySelector('.list-title').innerHTML.trim();
if (title.length > 14) {
    let fontSize = 72;
    for (let i = 14; i < title.length; i++) {
        fontSize -= 1.1;
    }
    document.querySelector('.list-title').style.fontSize = `${fontSize}px`;
}



function insertLoading() {
    let resultsBody = document.querySelector('.songs-container');
    let htmlData = `
        <div class="spinner ranker">
            <div class="loader">Loading...</div>
            <h2>Loading Songs</h2>
        </div>
    `;
    resultsBody.insertAdjacentHTML('beforeend', htmlData);
}

function removeLoading() {
    let loading = document.querySelector('.spinner');
    if (loading) {
        loading.remove();
    }
}

function insertNoResults() {
    let resultsBody = document.querySelector('.songs-container');
    let htmlData = `
        <div class="no-results ranker">
            <h2>No Results Found</h2>
        </div>
    `;
    resultsBody.insertAdjacentHTML('beforeend', htmlData);
}

function removeNoResults() {
    let noResults = document.querySelector('.no-results');
    if (noResults) {
        noResults.remove();
    }
}



function saveData(savedata, callback) {
    $.ajax({
        type: 'POST',
        url: `/save-list`,
        contentType: 'application/json',
        data: JSON.stringify(savedata),
        dataType: 'json',
        success: function (data) {
            callback(data);
        }
    });
}

document.querySelector('.list-options-save').addEventListener('click', saveList);
function saveList() {
    if (loggedIn) {
        clearSearch();
        let unrankedSongs = Array.from(document.querySelector('.songs-container').querySelectorAll('.list-song'));
        let rankedSongs = Array.from(document.querySelector('.list-song-container').querySelectorAll('.list-song'));
        let unrankedArr = [];
        let rankedArr = [];
        unrankedSongs.forEach(function (song) {
            unrankedArr.push(song.id);
        });
        rankedSongs.forEach(function (song) {
            rankedArr.push(song.id);
        });
        let data = {
            'unranked': unrankedArr,
            'ranked': rankedArr,
            'type': searchType,
            'id': searchID,
            'user_id': userId,
            'num_unranked': unrankedArr.length,
            'rank_date': new Date().toISOString().slice(0, 10),
            'name': title,
        }
        saveData(data, function (data) {
            if (data['status'] == 'success') {
                showPopup("List saved!");
            } else {
                showPopup("Error saving list!");
            }
        });
    } else {
        showPopup("You must be logged in to save a list!");
    }
}


function loadData(userId, rankingId, callback) {
    $.ajax({
        type: 'POST',
        url: `/load-list`,
        data: { 'user_id': userId, 'ranking_id': rankingId },
        success: function (data) {
            callback(data);
        }
    });
}

document.querySelector('.list-options-load').addEventListener('click', loadList);
function loadList(popup = true) {
    if (loggedIn) {
        clearSearch();
        removeNumber();
        loadData(userId, searchID, function (data) {
            if (data['status'] == 'success') {
                let unranked = data['unranked'];
                let ranked = data['ranked'];
                let unrankedArr = [];
                let rankedArr = [];
                unranked.forEach(function (song) {
                    unrankedArr.push(document.getElementById(song));
                });
                ranked.forEach(function (song) {
                    rankedArr.push(document.getElementById(song));
                });
                unrankedArr.forEach(function (song) {
                    document.querySelector('.songs-container').appendChild(song);
                    addSongToOriginal(song);
                });
                rankedArr.forEach(function (song) {
                    document.querySelector('.list-song-container').appendChild(song);
                    removeSongFromOriginal(song);
                    while (Array.from(document.querySelectorAll('.list-number')).length <= rankedArr.length) addNumber();
                });
                assignDoubleClick();
                removeNumber();
                if (popup) showPopup("List loaded!");
                else showPopup("List loaded automatically.");
            } else {
                if (popup) showPopup("No list found.");
            }
        });
    } else {
        if (popup) showPopup("You must be logged in to load a list.");
    }
}

function showPopup(text) {
    document.querySelector('.list-options-popup').classList.remove('hidden');
    document.querySelector('.popup-inner').innerHTML = text;
    setTimeout(function () {
        document.querySelector('.list-options-popup').classList.add('hidden');
    }, 2000);
}










async function start() {
    try {
        await Promise.all([buildSongs(), getUserInfoPromise()]);
        loadList(false);
    } catch (error) {
        console.error('An error occurred:', error);
    }
}

start();