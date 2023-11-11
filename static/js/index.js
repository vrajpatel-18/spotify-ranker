document.getElementById("searchButton").addEventListener('click', search);
document.getElementById("search").addEventListener('keydown', function(event) {
    if (event.keyCode === 13) {
        search();
    }
});

function search() {
    let searchValue = document.getElementById("search").value;
    if (searchValue != "") {

    }
}


let searchOptions = document.querySelectorAll('.search-type');
searchOptions.forEach(function (option) {
    option = option.querySelector('.search-type-inner');
    option.addEventListener('click', function (e) {
        searchOptions.forEach(function (option) {
            option = option.querySelector('.search-type-inner');
            option.classList.remove('active');
        });
        option.classList.add('active');
    });
});