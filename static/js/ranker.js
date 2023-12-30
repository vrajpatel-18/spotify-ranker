// Check if user is logged in
if (sessionStorage.getItem('loggedIn') != 'true') {
    function getUserInfo(callback) {
        $.ajax({
            type: 'GET',
            url: `/user-info`,
            success: function (data) {
                if (JSON.stringify(data) !== '{}') {
                    callback(data);
                } else {
                    console.log("data not found");
                }
            }
        });
    }
    getUserInfo(function (data) {
        console.log("logged in");
        let accountEl = document.querySelector('.account');
        accountEl.querySelector('.account-text').innerHTML = data['display_name'];
        accountEl.querySelector('.account-icon').src = data['images'][1]['url'];
        sessionStorage.setItem('loggedIn', 'true');
        sessionStorage.setItem('accountName', data['display_name']);
        sessionStorage.setItem('accountImage', data['images'][1]['url']);
    });
} else {
    let accountEl = document.querySelector('.account');
    accountEl.querySelector('.account-text').innerHTML = sessionStorage.getItem('accountName');
    accountEl.querySelector('.account-icon').src = sessionStorage.getItem('accountImage');
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
        updateData();
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
        updateData();
    },
    onEnd: function (evt) {
        updateData();
    },
});


function addNumber() {
    let numbers = document.querySelectorAll('.list-number-text');
    if (numbers.length != 0) {
        let lastNumber;
        numbers.forEach(function(number) {
            lastNumber = Number(number.innerHTML);
        });
        let htmlData = `
            <div class="list-number">
                <h3 class="list-number-text">${lastNumber+1}</h3>
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
            <div class="list-song-info">
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
    updateData();
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
            <div class="list-song-info">
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
    updateData();
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
                console.log(typeof artist);
                songInfo = songInfo.replace(artist, '');
            }
        }
        songInfo = songInfo.replace(',', '').replace('.', '').replace('(', '').replace(')', '').replace("'", '');
        console.log(songInfo);
        if (songInfo.toLowerCase().includes(search.toLowerCase())) {
            newSongs.push(song);
        }
    });
    newSongs.forEach(function (song) {
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
        sessionStorage.setItem('originalSongs', JSON.stringify(originalSongs.map(element => element.outerHTML)));
    }
}

function addSongToOriginal(songEl) {
    originalSongs.push(songEl);
}

function doubleClick(song) {
    $(song).off("dblclick");
    $(song).on("dblclick", function () {
        let htmlData = `
            <div id="${song.id}" class="${song.classList}">
                <div class="list-song-img-container"><img src="${$(song).find(".list-song-img").attr("src")}" class="list-song-img"></div>
                <div class="list-song-info">
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


function updateData() {
    console.log("update data");
    sessionStorage.setItem('leftHTML', document.querySelector('.songs-container').innerHTML);
    sessionStorage.setItem('rightNumsHTML', document.querySelector('.list-number-container').innerHTML);
    sessionStorage.setItem('rightSongsHTML', document.querySelector('.list-song-container').innerHTML);
    if (originalSongs) {
        sessionStorage.setItem('originalSongs', JSON.stringify(originalSongs.map(element => element.outerHTML)));
    }
}


function getData(search, type, callback) {
    updateData();
    console.log('loading...');
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
    document.querySelector('.songs-container').innerHTML = '';
    getData(searchID, searchType, function (data) {
        removeLoading();
        if (data['songs'].length == 0) {
            console.log('no songs');
            insertNoResults();
            updateData();
        } else {
            if (searchType == 'album') {
                data['songs'].forEach(function (song) {
                    song['album'] = "";
                });
            }
            let resultContainer = document.querySelector('.songs-container');
            data['songs'].forEach(function (song) {
                let artists = song['artists'].join(', ');
                let htmlData = `
                <div id="${song['id']}" class="list-song ${song['album']}">
                    <div class="list-song-img-container"><img src="${song['img']}" class="list-song-img"></div>
                    <div class="list-song-info">
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
            console.log('done');
            document.querySelector('.search-bar').classList.remove('hidden');
            originalSongs = Array.from(document.querySelector('.songs-container').querySelectorAll('.list-song'));
            sessionStorage.setItem('originalSongs', JSON.stringify(originalSongs));
            updateData();
        }
    });
}



// 12 characters or less: padding-left: 8%, font-size: 72px
// 13 characters: padding-left: 4%, font-size: 72px
// 14 characters: padding-left: 0, font-size: 72px
// 15 characters or more: padding-left: 0, font-size: 64px





// ON READY
let searchID = sessionStorage.getItem('id');
let searchType = sessionStorage.getItem('type');
let name = sessionStorage.getItem('name');
if (name.length > 14) {
    let fontSize = 72;
    for (let i = 14; i <  name.length; i++) {
        fontSize -= 1.1;
    }
    document.querySelector('.list-title').style.fontSize = `${fontSize}px`;
}
document.querySelector('.list-title').innerHTML = sessionStorage.getItem('name');
if (sessionStorage.getItem("changed") == 'true') {
    sessionStorage.setItem("changed", 'false');
    buildSongs();
} else {
    if (sessionStorage.getItem('leftHTML') != 'null') {
        document.querySelector('.songs-container').innerHTML = sessionStorage.getItem('leftHTML');
        document.querySelector('.list-number-container').innerHTML = sessionStorage.getItem('rightNumsHTML');
        document.querySelector('.list-song-container').innerHTML = sessionStorage.getItem('rightSongsHTML');
    } else {
        removeAllSongs();
    }
    document.querySelector('.search-bar').classList.remove('hidden');
    originalSongs = JSON.parse(sessionStorage.getItem("originalSongs")).map(htmlString => new DOMParser().parseFromString(htmlString, 'text/html').body.firstChild);
    assignDoubleClick();
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