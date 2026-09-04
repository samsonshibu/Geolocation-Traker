# 🌍 Geolocation Tracker

Fetch geolocation data for any IP address and display it on an interactive map.

Uses [ip-api.com](https://ip-api.com/) for IP → location lookups and
[Folium](https://python-visualization.github.io/folium/) (built on Leaflet.js)
to render the result as an interactive HTML map.

## Features

- Look up your own public IP or any target IP address
- Retrieves city, region, country, ISP, timezone, and coordinates
- Generates an interactive HTML map with a marker and popup info
- Simple CLI — no API key required

## Demo

```
$ python geolocation_tracker.py 8.8.8.8

Looking up geolocation data...

Result:
  IP:       8.8.8.8
  City:     Mountain View
  Region:   California
  Country:  United States
  Lat/Lon:  37.4056, -122.0775
  ISP:      Google LLC
  Timezone: America/Los_Angeles

Map saved to: map.html
Open this file in a browser to view the location.
```

## Installation

```bash
git clone https://github.com/<your-username>/geolocation-tracker.git
cd geolocation-tracker
pip install -r requirements.txt
```

## Usage

Locate your own public IP:

```bash
python geolocation_tracker.py
```

Locate a specific IP address:

```bash
python geolocation_tracker.py 8.8.8.8
```

Choose a custom output file:

```bash
python geolocation_tracker.py 8.8.8.8 -o mymap.html
```

Then open the generated `.html` file in any browser to see the pinned location.

## How it works

1. `get_public_ip()` — if no IP is supplied, fetches your own public IP via `api.ipify.org`.
2. `get_geolocation()` — queries `ip-api.com` for location data on the target IP.
3. `build_map()` — plots the coordinates on a Folium/Leaflet map with a popup showing
   city, region, country, ISP, and timezone, and saves it as a standalone HTML file.

## Notes & limitations

- IP geolocation is approximate — it typically reflects the ISP's registered
  location, not the device's exact physical address.
- [ip-api.com](https://ip-api.com/docs/legal) free tier allows 45 requests/minute
  and is for non-commercial use. For production use, consider a paid provider
  (ipinfo.io, MaxMind, ipstack, etc.) and add an API key.
- Requires an internet connection to reach the geolocation API.

## License

MIT — feel free to use and modify.
