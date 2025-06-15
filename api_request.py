import requests

api_key = "5b3ce3597851110001cf624812782a91d0ba4c469745e9af84f34936"

def get_coordinates(station_name: str) -> list:
    url = "https://api.openrouteservice.org/geocode/search"
    coords: list = []
    params = {
            "api_key": api_key,
            "text": f"{station_name} MRT, Singapore",
            "boundary.country": "SG"  # limit results to Singapore
            }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['features']:
            coords = data['features'][0]['geometry']['coordinates']
            #print(f"Coordinates of {station_name}: {coords}")
        else:
            print("No results found.")
    else:
        print("Error:", response.status_code)
        print(type(response.status_code))
        print(response.text)

    return coords

def calc_distance_mrt(start: str, end: str):

    distance: float = 0
    duration: float = 0

    start_cor: list = get_coordinates(start)
    end_cor: list = get_coordinates(end)
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {
            'Authorization': api_key,
            'Content-Type': 'application/json'
    }
    body = {
            "coordinates": [start_cor, end_cor]
    }
    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        distance = data['routes'][0]['summary']['distance']/1000 # m -> km
        duration = data['routes'][0]['summary']['duration']/60 # s -> min
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

    return (distance, duration)

# example usage
if __name__ == '__main__':
    distance, duration = calc_distance_mrt("City Hall", "Bugis")
    print(f"Distance: {distance:.2f}km")
    print(f"Duration: {duration:.2f}min")

