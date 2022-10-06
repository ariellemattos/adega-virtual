var searchInput = 'search_input';

$(document).ready(function () {
    var autocomplete;
    autocomplete = new google.maps.places.Autocomplete((document.getElementById(searchInput)), {
    types: ['geocode'],
    componentRestrictions: {
        country: "BR"
    }
    });
    
    google.maps.event.addListener(autocomplete, 'place_changed', function () {
        var near_place = autocomplete.getPlace();
        
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
            title: 'Meu marcador'
          });

    });
   
});



