# Singapore MRT Fare Calculator

<img src="https://github.com/thihahtoozin/sg-mrt-fare-calculator/blob/master/images/system_map.jpg" width="600"/>

## Introduction
This project helps you calculate the shortest route between two MRT stations in Singapore and supports multiple MRT lines, including interchanges.

## Features
- Display Paths
- Estimate Arrival Time

## How It Works
1. Parses station names from text files under `config/` directory
2. Constructs an adjacency list (graph) from each line.
3. Finds the shortest path using BFS (ideal for unweighted graphs like MRT maps).

## Get Started
Clone this repository
```
git clone https://github.com/thihahtoozin/sg-mrt-fare-calculator.git
cd sg-mrt-route-finder
```

Install dependencies
```
pip install -r requirements.txt
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
- [Breadth First Search Algorithm Visualization](https://youtu.be/xlVX7dXLS64?si=KpHjRDwCiMgL1ZGV)
- [Breadth First Search Algorithm Lecture](https://youtu.be/pcKY4hjDrxk?si=Ip5uAggWFCaN9NMl)
- [Graph Theory](https://youtu.be/oDqjPvD54Ss?si=23dTyeoDfkiujbp9)

