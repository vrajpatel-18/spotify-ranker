document.getElementById("searchButton").addEventListener('click', search);
document.addEventListener('keydown', function(event) {
    if (event.keyCode === 13) {
        search();
    }
});

let lastSearch = "";
let lastTerm = "";
let currTerm = "artist";
let searchTerm, searchType = "";
function search() {
    let searchValue = document.getElementById("search").value;
    if (searchValue != "" && (searchValue != lastSearch || currTerm != lastTerm)) {
        lastSearch = searchValue;
        lastTerm = currTerm;
        searchTerm = searchValue;
        searchType = currTerm;
        console.log(searchValue, searchType)
        fillResults();
    }
}


let searchOptions = document.querySelectorAll('.search-type');
searchOptions.forEach(function (option) {
    option = option.querySelector('.search-type-inner');
    option.addEventListener('click', function (e) {
        let name = option.innerHTML;
        if (name.toLowerCase() != currTerm) { // user changed options
            currTerm = name.toLowerCase();
            clearResults();
            search();
        }
        if (name == "Playlist") name = 'a playlist';
        else name = 'an ' + name.toLowerCase();
        document.getElementById("search").placeholder = `Search for ${name}`;
        searchOptions.forEach(function (option) {
            option = option.querySelector('.search-type-inner');
            option.classList.remove('active');
        });
        option.classList.add('active');
    });
});

function getData(search, type, callback) {
    $.ajax({
        type: 'POST',
        url: `/${type}`,
        data: { 'search': search },
        success: function (data) {
            data = JSON.parse(data);
            callback(data);
        }
    });
}

function clearResults() {
    let results = document.querySelectorAll('.home-results-item');
    results.forEach(function (result) {
        result.remove();
    });
}

function fillResults() {
    clearResults();
    getData(searchTerm, searchType, function (data) {
        if ('artists' in data) {
            let resultContainer = document.querySelector('.home-results');
            data['artists'].forEach(function (artist) {
                let htmlData = `
                <div id="${artist['id']}" class="home-results-item">
                    <img class="home-results-item-img" src="${artist['img']}">
                    <div class="home-results-item-text">
                        <h2 class="home-results-item-text-title">${artist['name']}</h2>
                        <div style="display: flex;">
                            <h6 class="home-results-item-text-desc1" style="margin-right: 25px; margin-left: 2px;">Artist</h6>
                            <h6 class="home-results-item-text-desc2"></h6>
                        </div>
                    </div>
                </div>
                `;
                resultContainer.insertAdjacentHTML('beforeend', htmlData);
            });
        } else if ('albums' in data) {
            let resultContainer = document.querySelector('.home-results');
            data['albums'].forEach(function (album) {
                let artists = album['artists'].join(', ');
                let htmlData = `
                <div id="${album['id']}" class="home-results-item">
                    <img class="home-results-item-img" src="${album['img']}">
                    <div class="home-results-item-text">
                        <h2 class="home-results-item-text-title">${album['name']}</h2>
                        <div style="display: flex;">
                            <h6 class="home-results-item-text-desc1" style="margin-right: 25px; margin-left: 2px;">${album['year']}</h6>
                            <h6 class="home-results-item-text-desc2">${artists}</h6>
                        </div>
                    </div>
                </div>
                `;
                resultContainer.insertAdjacentHTML('beforeend', htmlData);
            });
        }
    });
}