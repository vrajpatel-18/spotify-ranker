// ON LOAD
let currTerm = "album";
let loggedIn = false;

// Check if user is logged in
if (sessionStorage.getItem('loggedIn') != 'true') {
    function getUserInfo(callback) {
        $.ajax({
            type: 'GET',
            url: `/user-info`,
            success: function (data) {
                if (JSON.stringify(data) !== '{}') {
                    console.log(data);
                    callback(data);
                } else {
                    console.log("data not found");
                }
            }
        });
    }
    getUserInfo(function (data) {
        console.log("logged in");
        loggedIn = true;
        let accountEl = document.querySelector('.account');
        accountEl.querySelector('.account-text').innerHTML = data['display_name'];
        accountEl.querySelector('.account-icon').src = data['images'][1]['url'];
        sessionStorage.setItem('loggedIn', 'true');
        sessionStorage.setItem('accountName', data['display_name']);
        sessionStorage.setItem('accountImage', data['images'][1]['url']);
        sessionStorage.setItem('accountID', data['id']);
    });
} else {
    console.log("logged in");
    loggedIn = true;
    let accountEl = document.querySelector('.account');
    accountEl.querySelector('.account-text').innerHTML = sessionStorage.getItem('accountName');
    accountEl.querySelector('.account-icon').src = sessionStorage.getItem('accountImage');
}





document.getElementById("searchButton").addEventListener('click', search);
document.addEventListener('keydown', function (event) {
    if (event.keyCode === 13) {
        search();
    }
});

let lastSearch = "";
let lastTerm = "";
let searchTerm, searchType = "";

function search() {
    let searchValue = document.getElementById("search").value;
    let type = document.querySelector('.active').innerHTML;
    if (((type != "Playlist" && searchValue != "") || type == "Playlist") && (searchValue != lastSearch || currTerm != lastTerm)) {
        insertLoading();
        removeNoResults();
        lastSearch = searchValue;
        lastTerm = currTerm;
        searchTerm = searchValue;
        searchType = currTerm;
        fillResults();
    }
}


let searchOptions = document.querySelectorAll('.search-type');
searchOptions.forEach(function (option) {
    option.addEventListener('click', function (e) {
        let name = option.innerHTML;
        document.getElementById("search").placeholder = `Search for ${name.toLowerCase()}`;
        searchOptions.forEach(function (option) {
            option.classList.remove('active');
        });
        option.classList.add('active');
        if (name.toLowerCase() != currTerm) { // user changed options
            currTerm = name.toLowerCase();
            clearResults();
            search();
        }
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
    removeLoading();
    getData(searchTerm, searchType, function (data) {
        removeLoading();
        if ('artists' in data) {
            let resultContainer = document.querySelector('.home-results');
            data['artists'].forEach(function (artist) {
                let htmlData = `
                <a href="/artist/${artist['id']}"><div id="${artist['id']}" class="home-results-item">
                    <img class="home-results-item-img" src="${artist['img']}">
                    <div class="home-results-item-text">
                        <h2 class="home-results-item-text-title">${artist['name']}</h2>
                        <div style="display: flex;">
                            <h6 class="home-results-item-text-desc1" style="margin-right: 25px; margin-left: 2px;">Artist</h6>
                            <h6 class="home-results-item-text-desc2"></h6>
                        </div>
                    </div>
                </div></a>
                `;
                resultContainer.insertAdjacentHTML('beforeend', htmlData);
            });
        } else if ('albums' in data) {
            let resultContainer = document.querySelector('.home-results');
            data['albums'].forEach(function (album) {
                let artists = album['artists'].join(', ');
                let htmlData = `
                <a href="/album/${album['id']}"><div id="${album['id']}" class="home-results-item">
                    <img class="home-results-item-img" src="${album['img']}">
                    <div class="home-results-item-text">
                        <h2 class="home-results-item-text-title">${album['name']}</h2>
                        <div style="display: flex;">
                            <h6 class="home-results-item-text-desc1" style="margin-right: 25px; margin-left: 2px;">${album['year']}</h6>
                            <h6 class="home-results-item-text-desc2">${artists}</h6>
                        </div>
                    </div>
                </div></a>
                `;
                resultContainer.insertAdjacentHTML('beforeend', htmlData);
            });
        } else if ('playlists' in data) {
            if (data['playlists'].length == 0) {
                removeLoading();
                insertNoResults();
            } else {
                let resultContainer = document.querySelector('.home-results');
                data['playlists'].forEach(function (playlist) {
                    let htmlData = `
                <a href="/playlist/${playlist['id']}"><div id="${playlist['id']}" class="home-results-item">
                    <img class="home-results-item-img" src="${playlist['img']}">
                    <div class="home-results-item-text">
                        <h2 class="home-results-item-text-title">${playlist['name']}</h2>
                        <div style="display: flex;">
                            <h6 class="home-results-item-text-desc1" style="margin-right: 25px; margin-left: 2px;">Playlist</h6>
                            <h6 class="home-results-item-text-desc2">${playlist['owner']}</h6>
                        </div>
                    </div>
                </div></a>
                `;
                    resultContainer.insertAdjacentHTML('beforeend', htmlData);
                });
            }
        } else {
            removeLoading();
            insertNoResults();
        }
    });
}


function insertLoading() {
    let resultsBody = document.querySelector('.home-results');
    let htmlData = `
        <div class="spinner">
            <div class="loader">Loading...</div>
            <h2>Loading Results</h2>
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
    let resultsBody = document.querySelector('.home-results');
    let htmlData = `
        <div class="no-results">
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