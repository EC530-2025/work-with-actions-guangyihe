from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

################################
#   1. House 相关 API
################################

# 1.1 House - Add
#     需要参数: name, lat, lon, addr, uid, floors, size
@app.route('/house/add', methods=['POST'])
def add_house():
    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "No JSON provided"}), 400)

    required_params = ["name", "lat", "lon", "addr", "uid", "floors", "size"]
    for p in required_params:
        if p not in data:
            return make_response(jsonify({"error": f"Missing required parameter: {p}"}), 400)

    # TODO: 这里可进行进一步的参数校验（类型、数值范围等等）
    # TODO: 实际的添加逻辑

    return make_response(jsonify({"message": "House added successfully"}), 200)


# 1.2 House - Remove
#     需要参数: uid
@app.route('/house/remove', methods=['POST'])  # 或者使用 DELETE
def remove_house():
    data = request.get_json(silent=True)
    if not data or 'uid' not in data:
        return make_response(jsonify({"error": "uid is required"}), 400)

    # TODO: 实际的删除逻辑

    return make_response(jsonify({"message": f"House with uid={data['uid']} removed"}), 200)


# 1.3 House - Update
#     必须参数: uid (不能改)
#     可选参数: name, lat, lon, addr, floors, size
@app.route('/house/update', methods=['POST'])  # 或者使用 PUT
def update_house():
    data = request.get_json(silent=True)
    if not data or 'uid' not in data:
        return make_response(jsonify({"error": "uid is required"}), 400)

    # uid 不可变，这里仅演示获取 uid，其他字段可选
    house_uid = data['uid']

    # TODO: 根据 house_uid 查找 house，再进行更新
    # 在这里可检查 data.get('name') / data.get('lat') 等

    return make_response(jsonify({"message": f"House with uid={house_uid} updated"}), 200)


# 1.4 House - Query
#     可传入 0 个或多个: name, lat, lon, addr, uid
@app.route('/house/query', methods=['POST', 'GET'])
def query_house():
    # 如果是 GET，一般是在 query string 中；如果是 POST，一般在 body 中。
    # 这里只做示例，统一从 json body 中获取
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
    else:
        # GET 请求中，可从 request.args 获取参数
        data = {
            'name': request.args.get('name'),
            'lat': request.args.get('lat'),
            'lon': request.args.get('lon'),
            'addr': request.args.get('addr'),
            'uid': request.args.get('uid')
        }
    # data 可能部分字段是 None 或者没有传
    # TODO: 根据传入字段进行筛选逻辑
    
    return make_response(jsonify({
        "message": "House query result",
        "query_params": data
    }), 200)


################################
#   2. Room 相关 API
################################

# 2.1 Room - Add
#     需要参数: name, belong_to_house, size, floor
@app.route('/room/add', methods=['POST'])
def add_room():
    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "No JSON provided"}), 400)

    required_params = ["name", "belong_to_house", "size", "floor"]
    for p in required_params:
        if p not in data:
            return make_response(jsonify({"error": f"Missing required parameter: {p}"}), 400)

    # TODO: 检查在同一个 house 中 name 是否已经存在
    # TODO: 实际的添加逻辑

    return make_response(jsonify({"message": "Room added successfully"}), 200)


# 2.2 Room - Remove
#     需要参数: name, belong_to_house
@app.route('/room/remove', methods=['POST'])  # 或者使用 DELETE
def remove_room():
    data = request.get_json(silent=True)
    if not data or 'name' not in data or 'belong_to_house' not in data:
        return make_response(jsonify({"error": "name and belong_to_house are required"}), 400)

    # TODO: 实际的删除逻辑

    return make_response(jsonify({"message": f"Room {data['name']} removed from house {data['belong_to_house']}"}), 200)


# 2.3 Room - Update
#     必须参数: name, belong_to_house
#     可选参数: size, floor
@app.route('/room/update', methods=['POST'])  # 或者使用 PUT
def update_room():
    data = request.get_json(silent=True)
    if not data or 'name' not in data or 'belong_to_house' not in data:
        return make_response(jsonify({"error": "name and belong_to_house are required"}), 400)

    # TODO: 根据 name 和 belong_to_house 定位到具体 room，再进行更新
    # 可更新: size, floor

    return make_response(jsonify({"message": f"Room {data['name']} updated"}), 200)


# 2.4 Room - Query
#     要求传入 name 和 belong_to_house (题目说的: query 要求传入 name 和 belong_to_house)
@app.route('/room/query', methods=['POST', 'GET'])
def query_room():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
    else:
        data = {
            'name': request.args.get('name'),
            'belong_to_house': request.args.get('belong_to_house')
        }

    if 'name' not in data or 'belong_to_house' not in data or not data['name'] or not data['belong_to_house']:
        return make_response(jsonify({"error": "name and belong_to_house are required"}), 400)

    # TODO: 实际的查询逻辑

    return make_response(jsonify({
        "message": "Room query result",
        "query_params": data
    }), 200)


################################
#   3. Device 相关 API
################################

# 3.1 Device - Add
#     需要参数: name, belong_to_room, type
@app.route('/device/add', methods=['POST'])
def add_device():
    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "No JSON provided"}), 400)

    required_params = ["name", "belong_to_room", "type"]
    for p in required_params:
        if p not in data:
            return make_response(jsonify({"error": f"Missing required parameter: {p}"}), 400)

    # TODO: 实际的添加逻辑

    return make_response(jsonify({"message": "Device added successfully"}), 200)


# 3.2 Device - Remove
#     需要参数: name, belong_to_room
@app.route('/device/remove', methods=['POST'])  # 或者使用 DELETE
def remove_device():
    data = request.get_json(silent=True)
    if not data or 'name' not in data or 'belong_to_room' not in data:
        return make_response(jsonify({"error": "name and belong_to_room are required"}), 400)

    # TODO: 实际的删除逻辑

    return make_response(jsonify({"message": f"Device {data['name']} removed from room {data['belong_to_room']}"}), 200)


# 3.3 Device - Update
#     必须参数: name, belong_to_room
#     可选参数: type
@app.route('/device/update', methods=['POST'])  # 或者使用 PUT
def update_device():
    data = request.get_json(silent=True)
    if not data or 'name' not in data or 'belong_to_room' not in data:
        return make_response(jsonify({"error": "name and belong_to_room are required"}), 400)

    # TODO: 根据 name 和 belong_to_room 查找并更新
    # 可更新: type

    return make_response(jsonify({"message": f"Device {data['name']} updated"}), 200)


# 3.4 Device - Query
#     可根据自身需求灵活设计，这里简单示例
@app.route('/device/query', methods=['POST', 'GET'])
def query_device():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
    else:
        data = {
            'name': request.args.get('name'),
            'belong_to_room': request.args.get('belong_to_room'),
            'type': request.args.get('type')
        }
    # TODO: 实际的查询逻辑

    return make_response(jsonify({
        "message": "Device query result",
        "query_params": data
    }), 200)


################################
#   4. Users 相关 API
################################

# 假设用户信息至少包含: user_id (唯一标识), name, 等等
# 仅示例

# 4.1 Users - Add
@app.route('/users/add', methods=['POST'])
def add_user():
    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "No JSON provided"}), 400)

    if 'user_id' not in data or 'name' not in data:
        return make_response(jsonify({"error": "user_id and name are required"}), 400)

    # TODO: 实际的添加逻辑

    return make_response(jsonify({"message": "User added successfully"}), 200)


# 4.2 Users - Remove
@app.route('/users/remove', methods=['POST'])  # 或者 DELETE
def remove_user():
    data = request.get_json(silent=True)
    if not data or 'user_id' not in data:
        return make_response(jsonify({"error": "user_id is required"}), 400)

    # TODO: 实际的删除逻辑

    return make_response(jsonify({"message": f"User with user_id={data['user_id']} removed"}), 200)


# 4.3 Users - Update
@app.route('/users/update', methods=['POST'])  # 或者 PUT
def update_user():
    data = request.get_json(silent=True)
    if not data or 'user_id' not in data:
        return make_response(jsonify({"error": "user_id is required"}), 400)

    # user_id 不可修改，可更新 name 等其他字段

    return make_response(jsonify({"message": f"User with user_id={data['user_id']} updated"}), 200)


# 4.4 Users - Query
@app.route('/users/query', methods=['POST', 'GET'])
def query_user():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
    else:
        data = {
            'user_id': request.args.get('user_id'),
            'name': request.args.get('name'),
        }
    # TODO: 根据 user_id、name 等筛选

    return make_response(jsonify({
        "message": "User query result",
        "query_params": data
    }), 200)


################################
#   5. House 与 User 的对应关系
################################
# 假设有这样的需求：
#   - 为了建立某个 user 可以访问某个 house 的关系，需要一个 house_user 表或类似存储
#   - 我们只写对应关系的增删改查接口，示例：

@app.route('/house-user/add', methods=['POST'])
def add_house_user_relationship():
    data = request.get_json(silent=True)
    if not data or 'user_id' not in data or 'house_uid' not in data:
        return make_response(jsonify({"error": "user_id and house_uid are required"}), 400)

    # TODO: 建立 user 与 house 的对应关系

    return make_response(jsonify({"message": "Relationship between user and house added"}), 200)


@app.route('/house-user/remove', methods=['POST'])  # 或者 DELETE
def remove_house_user_relationship():
    data = request.get_json(silent=True)
    if not data or 'user_id' not in data or 'house_uid' not in data:
        return make_response(jsonify({"error": "user_id and house_uid are required"}), 400)

    # TODO: 移除 user 与 house 的对应关系

    return make_response(jsonify({"message": "Relationship between user and house removed"}), 200)


@app.route('/house-user/update', methods=['POST'])  # 或者 PUT
def update_house_user_relationship():
    data = request.get_json(silent=True)
    if not data or 'user_id' not in data or 'house_uid' not in data:
        return make_response(jsonify({"error": "user_id and house_uid are required"}), 400)

    # TODO: 更新 user 与 house 的对应关系 (如果需要存储更多属性，比如权限等级等)

    return make_response(jsonify({"message": "Relationship between user and house updated"}), 200)


@app.route('/house-user/query', methods=['POST', 'GET'])
def query_house_user_relationship():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
    else:
        data = {
            'user_id': request.args.get('user_id'),
            'house_uid': request.args.get('house_uid'),
        }

    # TODO: 根据 user_id、house_uid 等进行查询

    return make_response(jsonify({
        "message": "Query house-user relationships",
        "query_params": data
    }), 200)


if __name__ == '__main__':
    # debug 模式便于测试
    app.run(debug=True, host='0.0.0.0', port=5000)
