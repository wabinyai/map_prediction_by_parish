// Function to handle the geolocation request
function getUserLocation(map, callback) {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                // Get user's latitude and longitude
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                // Update the map view to the user's location
                map.setView([latitude, longitude], 10);

                // Call the callback function with the user's location
                callback(latitude, longitude);
            },
            (error) => {
                console.error("Error getting user's location:", error.message);
            }
        );
    } else {
        console.error("Geolocation is not available in this browser.");
    }
}

// Initialize the map
var map = L.map("map-container").setView([0, 0], 10);

// Load the OpenStreetMap tiles
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

// Create a GeoSearch control
const search = new GeoSearch.GeoSearchControl({
    provider: new GeoSearch.OpenStreetMapProvider(),
    autoComplete: true,
    autoCompleteDelay: 100,
    style: 'bar',
    showMarker: true,
});

// Add the GeoSearch control to the map
map.addControl(search);

// function to get search results
// function searchEventHandler(result) {
//     console.log(result.location);
//   }
function searchEventHandler(result) {
    const latitude = result.location.lat;
    const longitude = result.location.lng;
    // Call a function to fetch PM2.5 data and draw boundaries on the map
    console.log("here now....")
    console.log(result.raw)
    console.log(latitude, longitude)
    fetchAndRenderMap(latitude, longitude, map);
}
  map.on('geosearch/showlocation', searchEventHandler);

// Fetch and render map data from the server based on user's location
getUserLocation(map, function (latitude, longitude) {
    fetchAndRenderMap(latitude, longitude, map);
});

// Attach an event listener for map movements
map.on("moveend", function () {
    const center = map.getCenter();
    const bounds = {
        latitude: center.lat,
        longitude: center.lng,
    };
    fetchAndRenderMap(bounds.latitude, bounds.longitude, map);
});

// Center the map at the user's location and fetch data from the server
getUserLocation(map);

function loadFeatures(features, map) {
    var customColors = ["green", "yellow", "orange", "red", "purple", "maroon"];

    var colorScale = d3.scaleThreshold().domain([12.1, 35.5, 55.5, 150.5, 250.4, 500]).range(customColors);

    L.geoJSON(features, {
        style: function (feature) {
            var pm = feature.properties.pm2_5;
            var color = colorScale(pm);

            return {
                fillColor: color,
                fillOpacity: 0.5,
                color: "black",
                weight: 1,
            };
        },
        onEachFeature: function (feature, layer) {
            layer.bindPopup(`Parish: ${feature.properties.parish}\nPM2.5 AQI: ${feature.properties.pm2_5}`);

            layer.on({
                mouseover: function (e) {
                    var layer = e.target;
                    layer.openPopup();
                },
                mouseout: function (e) {
                    var layer = e.target;
                    layer.closePopup();
                },
            });
        },
    }).addTo(map);
}

// Function to fetch and render map data in chunks
function fetchAndRenderMap(latitude, longitude, map) {
    // Make a fetch request to the /geo endpoint with latitude and longitude parameters
    fetch(`/geo?latitude=${latitude}&longitude=${longitude}`)
        .then((response) => response.json())
        .then((data) => {
            // Data is now a JSON object containing the PM2.5 value
            var pm2_5 = data.pm2_5;

            // You can use the PM2.5 value as needed
            console.log("PM2.5 Value:", pm2_5);

            // Optionally, you can update the map or perform other actions based on the PM2.5 value.
            // For example, you might want to display it on the map or take some action if it exceeds a threshold.

        })
        .catch((error) => {
            console.error("Error fetching PM2.5 data:", error);
        });
}


