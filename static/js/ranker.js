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
        console.log(2);
    }
});

let list = document.querySelector('.list-song-container');
let sortable = new Sortable(list, {
    group: 'shared',
    animation: 200,
    ghostClass: 'hidden',
    dragClass: 'active',
    forceFallback: true,
    onMove: function (evt) {
        console.log(3);
    },
    onAdd: function (evt) { // when song moves from left to right
        console.log(4);
    }
});




// 12 characters or less: padding-left: 8%, font-size: 72px
// 13 characters: padding-left: 4%, font-size: 72px
// 14 characters: padding-left: 0, font-size: 72px
// 15 characters or more: padding-left: 0, font-size: 64px