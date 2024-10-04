from http.client import HTTPException
import requests

API_KEY = 'd25fe013c17545d48a5d4a6659c0d1ff'


def create_city(name):
    response = requests.get(
        f"https://api.geoapify.com/v1/geocode/search?text={name}&limit=1&type=city&apiKey={API_KEY}"
    )
    if response.status_code == 200:
        data = response.json().get('features')[0]['properties']
        long = data.get("lon")
        lat = data.get("lat")
        print(f'lat = {lat}, long = {long}')
        return "Город успешно добавлен в базу данных"
    else:
        raise HTTPException(status_code=404, detail="City not found")


create_city('Moscow')

data = {
    'type': 'FeatureCollection',
    'features': [
        {
        'type': 'Feature',
        'properties': {
            'datasource': {
                    'sourcename': 'openstreetmap', 'attribution': '© OpenStreetMap contributors', 'license': 'Open Database License', 'url': 'https://www.openstreetmap.org/copyright'
                    }, 
       'name': 'Moscow',
       'country': 'Russia', 
       'country_code': 'ru', 
       'lon': 37.6174782,
       'lat': 55.7505412,
       'result_type': 'city', 'formatted': 'Moscow, Russia', 'address_line1': 'Moscow', 'address_line2': 'Russia', 'category': 'populated_place', 'timezone': {'name': 'Europe/Moscow', 'offset_STD': '+03:00', 'offset_STD_seconds': 10800, 'offset_DST': '+03:00', 'offset_DST_seconds': 10800, 'abbreviation_STD': 'MSK', 'abbreviation_DST': 'MSK'}, 'plus_code': '9G7VQJ28+6X', 'plus_code_short': '28+6X Moscow, Russia', 'rank': {'importance': 0.8908193282833463, 'popularity': 9.885307004745208, 'confidence': 1, 'confidence_city_level': 1, 'match_type': 'full_match'}, 'place_id': '51197f918609cf4240597a26eabb11e04b40f00101f901fdfc260000000000c002089203064d6f73636f77'}, 'geometry': {'type': 'Point', 'coordinates': [37.6174782, 55.7505412]}, 'bbox': [37.290502, 55.4913076, 37.9674277, 55.9577717]}], 'query': {'text': 'Moscow', 'parsed': {'city': 'moscow', 'expected_type': 'unknown'}}}
