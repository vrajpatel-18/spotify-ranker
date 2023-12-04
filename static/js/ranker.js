// import { Sortable, AutoScroll } from 'sortablejs';

// Sortable.mount(new AutoScroll());





let cards = document.querySelector('.songs-container');
let sortable2 = new Sortable(cards, {
    group: 'shared',
    animation: 200,
    ghostClass: 'hidden',
    dragClass: 'active',
    forceFallback: true,
    onAdd: function (evt) { // when song moves from right to left
        removeNumber();
        assignDoubleClick();
    },
    onEnd: function (evt) {
        updateData();
    },
});

let list = document.querySelector('.list-song-container');
let sortable = new Sortable(list, {
    group: 'shared',
    animation: 200,
    ghostClass: 'hidden',
    dragClass: 'active',
    forceFallback: true,
    onAdd: function (evt) { // when song moves from left to right
        addNumber();
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
    });
    assignDoubleClick();
    updateData();
}

function moveRight(song) {
    song.addEventListener('dblclick', function (e) {
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
        addNumber();
        updateData();
    });
}

function assignDoubleClick() {
    let songs = document.querySelector('.songs-container').querySelectorAll('.list-song');
    songs.forEach(moveRight);
}


function updateData() {
    sessionStorage.setItem('leftHTML', document.querySelector('.songs-container').innerHTML);
    sessionStorage.setItem('rightNumsHTML', document.querySelector('.list-number-container').innerHTML);
    sessionStorage.setItem('rightSongsHTML', document.querySelector('.list-song-container').innerHTML);
}


// function getData(search, type, callback) {
//     $.ajax({
//         type: 'POST',
//         url: `/${type}-songs`,
//         data: { 'search': search },
//         success: function (data) {
//             data = JSON.parse(data);
//             callback(data);
//         }
//     });
// }


function getData(search, type, callback) {
    $.ajax({
        type: 'POST',
        url: `/test`,
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
        sessionStorage.setItem('originalLeftHTML', resultContainer.innerHTML);
        assignDoubleClick();
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
        document.querySelector('.songs-container').innerHTML = sessionStorage.getItem('originalLeftHTML');
    }
    assignDoubleClick();
}
