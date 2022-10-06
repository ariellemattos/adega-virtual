$(document).ready(function () {
    const searchInput = document.getElementById('search_input');
    const searchButton = document.getElementById('search_place_button');
    var autocomplete;
    autocomplete = new google.maps.places.Autocomplete(searchInput, {
        types: ['geocode'],
        componentRestrictions: {
            country: "BR"
        }
    });

    searchInput.addEventListener("change", () => {
        searchButton.disabled = true;
    })
    
    google.maps.event.addListener(autocomplete, 'place_changed', function (ev) {
        var near_place = autocomplete.getPlace();

        searchButton.disabled = false;
        
        latitude_view = near_place.geometry.location.lat();
        longitude_view = near_place.geometry.location.lng();

        var coordenadas = {lat: latitude_view, lng: longitude_view};

        var mapa = new google.maps.Map(document.getElementById('mapa'), {
            zoom: 15,
            center: coordenadas 
          });

        var marker = new google.maps.Marker({
            position: coordenadas,
            map: mapa,
            title: 'Estou aqui'
          });

    });
   
});



