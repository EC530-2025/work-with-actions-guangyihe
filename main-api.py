import os
import json
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)

# JSON file paths for data storage
HOUSES_FILE = 'houses.json'
ROOMS_FILE = 'rooms.json'
DEVICES_FILE = 'devices.json'

def load_data(file_path):
    """Load data from a JSON file. If the file does not exist, create an empty list."""
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)
        return []
    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except Exception:
            data = []
    return data

def save_data(file_path, data):
    """Save data to a specified JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/house/add', methods=['POST'])
def add_house():
    """Add a new house. Required fields: name, lat, lon, addr, floors, size. A unique uid is generated automatically."""
    data = request.get_json()
    required = ['name', 'lat', 'lon', 'addr', 'floors', 'size']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400

    houses = load_data(HOUSES_FILE)
    uid = str(uuid.uuid4())
    new_house = {
        'uid': uid,
        'name': data['name'],
        'lat': data['lat'],
        'lon': data['lon'],
        'addr': data['addr'],
        'floors': data['floors'],
        'size': data['size']
    }
    houses.append(new_house)
    save_data(HOUSES_FILE, houses)
    return jsonify({'message': 'House added successfully', 'uid': uid})

@app.route('/house/remove', methods=['POST'])
def remove_house():
    """Remove a house by uid. Deleting a house also removes all associated rooms and devices."""
    data = request.get_json()
    if 'uid' not in data:
        return jsonify({'error': 'uid is required'}), 400

    uid = data['uid']
    houses = load_data(HOUSES_FILE)
    new_houses = [house for house in houses if house['uid'] != uid]
    if len(new_houses) == len(houses):
        return jsonify({'error': 'House not found'}), 404
    save_data(HOUSES_FILE, new_houses)

    # Remove all rooms associated with the house
    rooms = load_data(ROOMS_FILE)
    removed_rooms = [room for room in rooms if room['belong_to_house'] == uid]
    rooms = [room for room in rooms if room['belong_to_house'] != uid]
    save_data(ROOMS_FILE, rooms)

    # Remove all devices in deleted rooms
    devices = load_data(DEVICES_FILE)
    for room in removed_rooms:
        devices = [device for device in devices if device['belong_to_room'] != room['name']]
    save_data(DEVICES_FILE, devices)
    return jsonify({'message': 'House and its associated rooms and devices removed successfully'})

@app.route('/house/update', methods=['POST'])
def update_house():
    """Update house information. The uid must be provided and cannot be changed. Optional fields: name, lat, lon, addr, floors, size."""
    data = request.get_json()
    if 'uid' not in data:
        return jsonify({'error': 'uid is required'}), 400

    uid = data['uid']
    houses = load_data(HOUSES_FILE)
    for house in houses:
        if house['uid'] == uid:
            for field in ['name', 'lat', 'lon', 'addr', 'floors', 'size']:
                if field in data:
                    house[field] = data[field]
            save_data(HOUSES_FILE, houses)
            return jsonify({'message': 'House updated successfully'})
    return jsonify({'error': 'House not found'}), 404

@app.route('/house/query', methods=['GET'])
def query_house():
    """Query houses by any combination of name, lat, lon, addr, uid. If no parameters are provided, return all houses."""
    args = request.args
    houses = load_data(HOUSES_FILE)
    result = []
    for house in houses:
        match = True
        for field in ['name', 'lat', 'lon', 'addr', 'uid']:
            if field in args and str(house.get(field)) != args.get(field):
                match = False
                break
        if match:
            result.append(house)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
