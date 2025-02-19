from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

################################
#   1. House-related API
################################

# 1.1 House - Add
#     Required parameters: name, lat, lon, addr, uid, floors, size
@app.route('/house/add', methods=['POST'])
def add_house():
    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "No JSON provided"}), 400)

    required_params = ["name", "lat", "lon", "addr", "uid", "floors", "size"]
    for p in required_params:
        if p not in data:
            return make_response(jsonify({"error": f"Missing required parameter: {p}"}), 400)

    # Parameter validation
    if not isinstance(data["name"], str) or not data["name"].strip():
        return make_response(jsonify({"error": "Invalid 'name': must be a non-empty string"}), 400)

    if not isinstance(data["addr"], str) or not data["addr"].strip():
        return make_response(jsonify({"error": "Invalid 'addr': must be a non-empty string"}), 400)

    if not isinstance(data["uid"], str) or not data["uid"].strip():
        return make_response(jsonify({"error": "Invalid 'uid': must be a non-empty string"}), 400)

    try:
        lat = float(data["lat"])
        lon = float(data["lon"])
    except ValueError:
        return make_response(jsonify({"error": "Invalid 'lat' or 'lon': must be valid floating-point numbers"}), 400)

    if not (-90 <= lat <= 90):
        return make_response(jsonify({"error": "Invalid 'lat': must be between -90 and 90"}), 400)

    if not (-180 <= lon <= 180):
        return make_response(jsonify({"error": "Invalid 'lon': must be between -180 and 180"}), 400)

    try:
        floors = int(data["floors"])
        size = int(data["size"])
    except ValueError:
        return make_response(jsonify({"error": "Invalid 'floors' or 'size': must be integers"}), 400)

    if floors <= 0:
        return make_response(jsonify({"error": "Invalid 'floors': must be a positive integer"}), 400)

    if size <= 0:
        return make_response(jsonify({"error": "Invalid 'size': must be a positive integer"}), 400)

    # TODO: Actual addition logic

    return make_response(jsonify({"message": "House added successfully"}), 200)


# 1.2 House - Remove
#     Required parameter: uid
@app.route('/house/remove', methods=['POST'])  # Alternatively, use DELETE
def remove_house():
    data = request.get_json(silent=True)
    if not data or 'uid' not in data:
        return make_response(jsonify({"error": "uid is required"}), 400)

    # TODO: Actual deletion logic

    return make_response(jsonify({"message": f"House with uid={data['uid']} removed"}), 200)


# 1.3 House - Update
#     Required parameter: uid (cannot be changed)
#     Optional parameters: name, lat, lon, addr, floors, size
@app.route('/house/update', methods=['POST'])  # Alternatively, use PUT
def update_house():
    data = request.get_json(silent=True)
    if not data or 'uid' not in data:
        return make_response(jsonify({"error": "uid is required"}), 400)

    # uid is immutable, just demonstrating retrieving uid, other fields are optional
    house_uid = data['uid']

    # TODO: Find the house by house_uid and update it accordingly
    # Here, you can check data.get('name') / data.get('lat') etc.

    return make_response(jsonify({"message": f"House with uid={house_uid} updated"}), 200)


# 1.4 House - Query
#     Accepts 0 or more parameters: name, lat, lon, addr, uid
@app.route('/house/query', methods=['POST', 'GET'])
def query_house():
    # If it's a GET request, parameters are usually in the query string.
    # If it's a POST request, parameters are usually in the request body.
    # Here, we unify by fetching from the JSON body
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
    else:
        # For GET requests, retrieve parameters from request.args
        data = {
            'name': request.args.get('name'),
            'lat': request.args.get('lat'),
            'lon': request.args.get('lon'),
            'addr': request.args.get('addr'),
            'uid': request.args.get('uid')
        }
    
    # data may have some fields missing or set to None
    # TODO: Implement filtering logic based on input fields
    
    return make_response(jsonify({
        "message": "House query result",
        "query_params": data
    }), 200)


################################
#   2. Room-related API
################################

# 2.1 Room - Add
#     Required parameters: name, belong_to_house, size, floor
@app.route('/room/add', methods=['POST'])
def add_room():
    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "No JSON provided"}), 400)

    required_params = ["name", "belong_to_house", "size", "floor"]
    for p in required_params:
        if p not in data:
            return make_response(jsonify({"error": f"Missing required parameter: {p}"}), 400)

    # TODO: Check if the name already exists in the same house
    # TODO: Actual addition logic

    return make_response(jsonify({"message": "Room added successfully"}), 200)


# 2.2 Room - Remove
#     Required parameters: name, belong_to_house
@app.route('/room/remove', methods=['POST'])  # Alternatively, use DELETE
def remove_room():
    data = request.get_json(silent=True)
    if not data or 'name' not in data or 'belong_to_house' not in data:
        return make_response(jsonify({"error": "name and belong_to_house are required"}), 400)

    # TODO: Actual deletion logic

    return make_response(jsonify({"message": f"Room {data['name']} removed from house {data['belong_to_house']}"}), 200)


# 2.3 Room - Update
#     Required parameters: name, belong_to_house
#     Optional parameters: size, floor
@app.route('/room/update', methods=['POST'])  # Alternatively, use PUT
def update_room():
    data = request.get_json(silent=True)
    if not data or 'name' not in data or 'belong_to_house' not in data:
        return make_response(jsonify({"error": "name and belong_to_house are required"}), 400)

    # TODO: Locate the room by name and belong_to_house, then update it
    # Can update: size, floor

    return make_response(jsonify({"message": f"Room {data['name']} updated"}), 200)


if __name__ == '__main__':
    # Enable debug mode for testing
    app.run(debug=True, host='0.0.0.0', port=5000)
