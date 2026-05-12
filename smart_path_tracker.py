import math
import os
import webbrowser
import random
import networkx as nx
import folium
from folium.plugins import AntPath
def build_demo_graph():
    G = nx.Graph()
    locations = {
        "Taxila Cantt": (33.7456, 72.7873),
        "Taxila Museum": (33.7470, 72.7810),
        "Taxila Main Bazaar": (33.7505, 72.7990),
        "Taxila Railway Station": (33.7469, 72.7905),
        "UET Taxila": (33.7680, 72.8230),
        "Khanpur Road": (33.7582, 72.8050),
        "Mohra Moradu": (33.7395, 72.7765),
        "Sirkap Ruins": (33.7492, 72.7851),
        "Dharmarajika Stupa": (33.7441, 72.7834),
        "Wah Cantt": (33.7700, 72.7500)
    }
    edges = [
        ("Taxila Cantt", "Taxila Museum"),
        ("Taxila Cantt", "Taxila Railway Station"),
        ("Taxila Railway Station", "Taxila Main Bazaar"),
        ("Taxila Main Bazaar", "Khanpur Road"),
        ("Khanpur Road", "UET Taxila"),
        ("Taxila Museum", "Sirkap Ruins"),
        ("Sirkap Ruins", "Dharmarajika Stupa"),
        ("Dharmarajika Stupa", "Mohra Moradu"),
        ("Taxila Cantt", "Taxila Main Bazaar"),
        ("Taxila Main Bazaar", "Wah Cantt"),
        ("Wah Cantt", "UET Taxila")
    ]
    for a, b in edges:
        G.add_edge(a, b, weight=math.dist(locations[a], locations[b]))
    return G, locations
def bfs_route(G, start, end):
    return nx.shortest_path(G, start, end)
def dfs_route(G, start, end):
    stack = [(start, [start])]
    visited = set()
    while stack:
        node, path = stack.pop()
        if node == end:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in G.neighbors(node):
                stack.append((neighbor, path + [neighbor]))
    return None
def all_paths_backtracking(G, start, end, path=None, paths=None):
    if path is None:
        path = [start]
    if paths is None:
        paths = []
    if start == end:
        paths.append(path)
        return paths
    for neighbor in G.neighbors(start):
        if neighbor not in path:
            all_paths_backtracking(G, neighbor, end, path + [neighbor], paths)
    return paths
def linear_regression_predict(distance, traffic):
    traffic_weight = {"low": 1, "medium": 1.5, "high": 2}
    m = 2.8
    c = 4
    return (m * distance * traffic_weight[traffic]) + c
vehicle_icons = {
    "car": "car",
    "bus": "bus",
    "cycle": "bicycle",
    "walk": "user"
}
traffic_colors = {
    "low": "green",
    "medium": "orange",
    "high": "red"
}
def simulate_traffic():
    return random.choice(["low", "medium", "high"])
def visualize_route(route, locations, vehicle, traffic):
    m = folium.Map(location=locations[route[0]], zoom_start=14)
    route_color = traffic_colors[traffic]
    tourist_places = {
        "Taxila Museum",
        "Sirkap Ruins",
        "Dharmarajika Stupa",
        "Mohra Moradu"
    }
    for loc, coord in locations.items():
        if loc == route[0]:
            icon = folium.Icon(color="green", icon=vehicle_icons[vehicle], prefix="fa")
        elif loc == route[-1]:
            icon = folium.Icon(color="red", icon="flag", prefix="fa")
        elif loc in tourist_places:
            icon = folium.Icon(color="purple", icon="landmark", prefix="fa")
        elif loc in route:
            icon = folium.Icon(color="blue", icon="road", prefix="fa")
        else:
            icon = folium.Icon(color="gray", icon="info-sign")
        folium.Marker(coord, popup=loc, tooltip=loc, icon=icon).add_to(m)
    AntPath(
        locations=[locations[n] for n in route],
        color=route_color,
        weight=6,
        delay=800
    ).add_to(m)
    file = "taxila_ai_smart_route.html"
    m.save(file)
    webbrowser.open("file://" + os.path.abspath(file))
def main():
    print("=== SMART PATH: OFFLINE AI ROUTE TRACKING SYSTEM ===")
    G, locations = build_demo_graph()
    print("\nAvailable locations:")
    for l in locations:
        print("-", l)
    start = input("\nEnter start location: ").strip()
    end = input("Enter destination: ").strip()
    if start not in locations or end not in locations:
        print("Invalid location.")
        return
    print("\nChoose Algorithm:")
    print("1. BFS (Shortest Path)")
    print("2. DFS (Deep Search)")
    print("3. Backtracking (All Paths Best)")
    algo = input("Enter choice: ").strip()
    print("\nChoose vehicle: car | bus | cycle | walk")
    vehicle = input("Vehicle: ").strip().lower()
    if vehicle not in vehicle_icons:
        print("Invalid vehicle.")
        return
    traffic = simulate_traffic()
    print(f"\nLive Traffic Status: {traffic.upper()}")
    if algo == "1":
        route = bfs_route(G, start, end)
        algo_name = "BFS"
    elif algo == "2":
        route = dfs_route(G, start, end)
        algo_name = "DFS"
    elif algo == "3":
        all_routes = all_paths_backtracking(G, start, end)
        route = min(all_routes, key=len)
        algo_name = "Backtracking"
    else:
        print("Invalid algorithm.")
        return
    distance = sum(
        G[route[i]][route[i + 1]]["weight"]
        for i in range(len(route) - 1)
    )
    time = linear_regression_predict(distance, traffic)
    print("\n=== ROUTE DETAILS ===")
    print("Algorithm Used:", algo_name)
    print("Route:", " -> ".join(route))
    print(f"Distance: {distance:.2f} km")
    print(f"AI Predicted Time: {time:.2f} minutes")
    visualize_route(route, locations, vehicle, traffic)
if __name__ == "__main__":
    main()

