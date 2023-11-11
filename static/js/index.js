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