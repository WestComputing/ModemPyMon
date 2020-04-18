const fs = require('fs');
const CITY_DATA_FILENAME = './city.list.json';

function calculate_range(latA, lonA, latB, lonB) {
    const deg2rad = deg => deg * Math.PI/180; // radians = degrees * pi/180
    const R = 3961; // Radius of the Earth in miles at 39 degrees, Haversine Formula

    // convert coordinates to radians
    const lat1 = deg2rad(latA);
    const lon1 = deg2rad(lonA);
    const lat2 = deg2rad(latB);
    const lon2 = deg2rad(lonB);

    const dLon = lon2 - lon1;
    const dLat = lat2 - lat1;
    const a = Math.pow(Math.sin(dLat/2),2) + Math.cos(lat1) * Math.cos(lat2) * Math.pow(Math.sin(dLon/2),2);
    const c = 2 * Math.atan2(Math.sqrt(a),Math.sqrt(1-a)); // great circle distance in radians
    const d = c * R;
    return Number(d.toFixed(2));
}

const myLat = 36;
const myLon = -79;
const myRanges = [];

const rawData = fs.readFileSync(CITY_DATA_FILENAME, 'utf8');
const cities = JSON.parse(rawData);

for (const city of cities) {
    const tuple = {
        id: city.id,
        name: city.name,
        lat: city.coord.lat,
        lon: city.coord.lon
    };
    tuple.range = calculate_range(myLat, myLon, city.coord.lat, city.coord.lon);
    myRanges.push(tuple);
}

myRanges.sort((a, b) => a.range - b.range);
console.log(myRanges.slice(0, 10));
