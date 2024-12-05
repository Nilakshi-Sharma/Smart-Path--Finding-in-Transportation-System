import folium
import requests
from flask import Flask, render_template, request
from folium import PolyLine
import openrouteservice

app = Flask(__name__, template_folder='template')

def format_duration(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

@app.route('/', methods=['POST', 'GET'])
def get_map():
    map_html = None
    formatted_duration = "" 
    if request.method == 'POST':
        lat1 = float(request.form['lat1'])
        lng1 = float(request.form['lng1'])
        lat2 = float(request.form['lat2'])
        lng2 = float(request.form['lng2'])

        # Set a default vehicle type (e.g., "driving-car")
        vehicle_type = 'driving-car'

        # Request traffic data (optional: only if needed for future use)
        url = f"https://data.traffic.hereapi.com/v7/flow?locationReferencing=shape&in=bbox:{lng1},{lat1},{lng2},{lat2}&apiKey=ZhY92oQpAlyZoyMaBp9mI3vFedz_kR9mq0H3M3HhEZY"
        response = requests.get(url)
        traffic_data = response.json()

        # Create a map centered at the average of the input coordinates
        m = folium.Map(location=[(lat1 + lat2) / 2, (lng1 + lng2) / 2], zoom_start=14)

        client = openrouteservice.Client(key='5b3ce3597851110001cf6248cc5863ac80a4414e8c34f637a1220b04')  # Replace with your OpenRouteService API key
        coords = [[lng1, lat1], [lng2, lat2]]

        # Find the shortest path using OpenRouteService
        route = client.directions(coordinates=coords, profile=vehicle_type, format='geojson')
        duration = route['features'][0]['properties']['segments'][0]['duration']  # Get the duration in seconds

        # Add the shortest path to the map
        folium.GeoJson(route, name='Shortest Path').add_to(m)

        # Add start and end markers to the map
        folium.Marker([lat1, lng1], popup='Start', icon=folium.Icon(color='green', icon='play')).add_to(m)
        folium.Marker([lat2, lng2], popup='End', icon=folium.Icon(color='red', icon='stop')).add_to(m)

        map_html = m._repr_html_()
        formatted_duration = format_duration(duration)
    return render_template('index.html', map_html=map_html, duration=formatted_duration)

if __name__ == '__main__':
    app.run(debug=True)
