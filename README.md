# Singapore MRT Fare Calculator

![](https://journey.smrt.com.sg/static/journey/img/network_map_2025_January.png)

## Introduction
This project helps you calculate the shortest route between two MRT stations in Singapore and supports multiple MRT lines, including interchanges.

## How It Works
1. Parses station names from text files under `config/` directory
2. Constructs an adjacency list (graph) from each line.
3. Finds the shortest path using BFS (ideal for unweighted graphs like MRT maps).

## Get Started
Clone this repository
```
git clone https://github.com/yourusername/sg-mrt-route-finder.git
cd sg-mrt-route-finder
```

run `main.py` file
```
python3 main.py
```

## Configuration
- Can add or remove lines just by creating or deleting the text files in `config/`
- Text files in this directory must store corresponding MRT stations in ascending order of station code

```
.
├── config/
│   ├── EW.txt            # East-West Line stations
│   ├── NS.txt            # North-South Line stations
│   ├── CC.txt            # Circle Line stations
│   ├── NE.txt            # North-East Line stations
│   └── ...               # More lines if added
├── display_stations.py   
├── api_request.py        
├── main.py               
└── README.md             
```

## References
- [Wikipedia – Mass Rapid Transit (Singapore)](https://en.wikipedia.org/wiki/Mass_Rapid_Transit_(Singapore))
- [LTA Official MRT System Map](https://www.lta.gov.sg/content/ltagov/en/map.html)
- [OpenStreetMap Singapore Rail Data](https://www.openstreetmap.org/)
- [Singapore MRT Station Codes and Data](https://www.transitlink.com.sg/)
- [OpenRouteService API](https://openrouteservice.org)
- [For image in this file](https://journey.smrt.com.sg/static/journey/img/network_map_2025_January.png)
