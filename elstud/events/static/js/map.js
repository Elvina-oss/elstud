ymaps.ready(init);

function init() {
    var map = new ymaps.Map("map", {
        center: [55.797676, 49.101264],
        zoom: 10
    });

    // Получение данных о событиях из Django представления
    fetch('/event_list/')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            var events = JSON.parse(data);

            // Проверка наличия событий
            if (events.length > 0) {
                // Создание меток на карте для каждого события
                for (var i = 0; i < events.length; i++) {
                    var event = events[i].fields;
                    var placemark = new ymaps.Placemark([event.location_lat, event.location_lng], {
                        balloonContent: 'Event time: ' + event.time
                    });
                    map.geoObjects.add(placemark);
                }
            } else {
                // В случае отсутствия событий, просто отображаем карту без меток
            }
        });
}