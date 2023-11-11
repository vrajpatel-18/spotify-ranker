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
    }
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



document.querySelector('.options-add').addEventListener('click', function (e) {
    addAllSongs();
});

document.querySelector('.options-remove').addEventListener('click', function (e) {
    removeAllSongs();
});

function addAllSongs() {
    // add all songs
    let length = document.querySelector('.songs-container').querySelectorAll('.list-song').length;
    let songs = document.querySelector('.songs-container').querySelectorAll('.list-song');
    songs.forEach(function (song) {
        let htmlData = `
        <div class="list-song">
            <div class="list-song-img-container"><img src="../static/images/utopia.jpg" class="list-song-img"></div>
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
}

function removeAllSongs() {
    // remove all numberes
    let numbers = document.querySelector('.list-number-container').querySelectorAll('.list-number');
    numbers.forEach(function (number) {
        number.remove();
    });
    // remove all songs
    let songs = document.querySelector('.list-song-container').querySelectorAll('.list-song');
    songs.forEach(function (song) {
        let htmlData = `
        <div class="list-song">
            <div class="list-song-img-container"><img src="../static/images/utopia.jpg" class="list-song-img"></div>
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
}




// 12 characters or less: padding-left: 8%, font-size: 72px
// 13 characters: padding-left: 4%, font-size: 72px
// 14 characters: padding-left: 0, font-size: 72px
// 15 characters or more: padding-left: 0, font-size: 64px