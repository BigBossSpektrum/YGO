function updateSearchResults() {
    var form = document.getElementById("search-form");
    var formData = new FormData(form);

    var url = new URL(window.location.href);
    url.search = new URLSearchParams(formData).toString();

    console.log("URL generada:", url.toString()); // Depuración: Verifica la URL generada

    fetch(url, {
        method: 'GET',
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById("results").innerHTML = data;
    })
    .catch(error => console.error("Error al obtener resultados:", error));
}
