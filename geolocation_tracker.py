#!/usr/bin/env python3
"""
Geolocation Tracker
--------------------
Fetches geolocation data for an IP address (defaults to the caller's own
public IP) using the free ip-api.com service, and renders the result on
an interactive map (HTML file, built with Folium).

Usage:
    python geolocation_tracker.py                # locate your own public IP
    python geolocation_tracker.py 8.8.8.8         # locate a specific IP
    python geolocation_tracker.py 8.8.8.8 -o out.html
"""

import argparse
import sys
import requests
import folium


IP_API_URL = "http://ip-api.com/json/{ip}"
FIELDS = "status,message,country,regionName,city,zip,lat,lon,timezone,isp,org,query"


def get_public_ip() -> str:
    """Return the caller's own public IP address."""
    response = requests.get("https://api.ipify.org?format=json", timeout=10)
    response.raise_for_status()
    return response.json()["ip"]


def get_geolocation(ip: str | None = None) -> dict:
    """
    Fetch geolocation data for the given IP address.
    If no IP is given, looks up the caller's own public IP.
    """
    target = ip if ip else ""
    url = IP_API_URL.format(ip=target) + f"?fields={FIELDS}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "success":
        raise ValueError(f"Geolocation lookup failed: {data.get('message', 'unknown error')}")

    return data


def build_map(data: dict, output_path: str = "map.html") -> str:
    """Render the geolocation result on an interactive Folium map."""
    lat, lon = data["lat"], data["lon"]

    m = folium.Map(location=[lat, lon], zoom_start=10, tiles="OpenStreetMap")

    popup_html = f"""
    <b>IP:</b> {data.get('query')}<br>
    <b>City:</b> {data.get('city')}<br>
    <b>Region:</b> {data.get('regionName')}<br>
    <b>Country:</b> {data.get('country')}<br>
    <b>ISP:</b> {data.get('isp')}<br>
    <b>Timezone:</b> {data.get('timezone')}
    """

    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"{data.get('city')}, {data.get('country')}",
        icon=folium.Icon(color="red", icon="map-marker", prefix="fa"),
    ).add_to(m)

    m.save(output_path)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Fetch IP geolocation and display it on a map.")
    parser.add_argument("ip", nargs="?", default=None, help="IP address to look up (defaults to your own public IP)")
    parser.add_argument("-o", "--output", default="map.html", help="Output HTML map file (default: map.html)")
    args = parser.parse_args()

    try:
        print("Looking up geolocation data...")
        data = get_geolocation(args.ip)

        print("\nResult:")
        print(f"  IP:       {data.get('query')}")
        print(f"  City:     {data.get('city')}")
        print(f"  Region:   {data.get('regionName')}")
        print(f"  Country:  {data.get('country')}")
        print(f"  Lat/Lon:  {data.get('lat')}, {data.get('lon')}")
        print(f"  ISP:      {data.get('isp')}")
        print(f"  Timezone: {data.get('timezone')}")

        output_file = build_map(data, args.output)
        print(f"\nMap saved to: {output_file}")
        print("Open this file in a browser to view the location.")

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
