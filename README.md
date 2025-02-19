# Smart Home System API (Semi-Finished Example)

This project is a sample backend service based on **Python Flask**, demonstrating basic RESTful APIs and parameter validation for **Houses**, **Rooms**, **Devices**, **Users**, and **House-User relationships** in a smart home system.

> **Note**:  
> This project only shows route design and basic parameter validation. It does not implement any actual data storage (like a database) or complex business logic. It can serve as a learning reference or a basic project scaffold.

## Table of Contents

1. [Features](#features)  
2. [Requirements](#requirements)  
3. [Installation & Running](#installation--running)  
4. [API Endpoints](#api-endpoints)  
   1. [House Endpoints](#house-endpoints)  
   2. [Room Endpoints](#room-endpoints)  
   3. [Device Endpoints](#device-endpoints)  
   4. [Users Endpoints](#users-endpoints)  
   5. [House-User Relationship Endpoints](#house-user-relationship-endpoints)  
5. [Example Requests](#example-requests)  
6. [Future Improvements](#future-improvements)

---

## Features

- **House**: Add, remove, update, and query operations.  
- **Room**: Add, remove, update, and query operations.  
- **Device**: Add, remove, update, and query operations.  
- **User**: Add, remove, update, and query operations.  
- **House-User Relationships**: Create and manage user-house relationships (e.g., permissions), including add, remove, update, and query.

**Key Point**: The main goal of this project is to demonstrate **Flask**-based RESTful API route design and basic parameter validation. It does not include database handling or complex business logic.

---

## Requirements

- Python 3.x
- Flask >= 1.0 (or an equivalent version)

You can specify other dependencies in a `requirements.txt` file as needed.

---

## Installation & Running

1. **Clone or download this repository**  
   ```bash
   git clone <YOUR_REPOSITORY_URL>
   cd your_project_directory
   ```

2. **Create and activate a virtual environment (optional)**  
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux or macOS
   .\venv\Scripts\activate    # Windows
   ```

3. **Install dependencies**  
   ```bash
   pip install flask
   ```
   If there is a `requirements.txt` file, you can use:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the project**  
   ```bash
   python app.py
   ```
   By default, the server listens on port `5000`.

5. **Test the endpoints**  
   - You can use Postman, cURL, or any other tool to make API requests.  
   - Default URL: `http://localhost:5000/`

---

## API Endpoints

Below are brief descriptions of each module's routes, request methods, and required parameters. **Note: This is only for demonstration. There is no data storage or real logic implemented.**

### House Endpoints

#### 1. `/house/add`
- **Method**: `POST`
- **Required Fields** (JSON Body):  
  - `name`  
  - `lat`  
  - `lon`  
  - `addr`  
  - `uid`  
  - `floors`  
  - `size`
- **Purpose**: Add a new House.  
- **Sample Response**:  
  ```json
  {
    "message": "House added successfully"
  }
  ```

#### 2. `/house/remove`
- **Method**: `POST`
- **Required Fields**:  
  - `uid`
- **Purpose**: Delete a House by `uid`.  
- **Sample Response**:  
  ```json
  {
    "message": "House with uid=<UID> removed"
  }
  ```

#### 3. `/house/update`
- **Method**: `POST`
- **Required Fields**:  
  - `uid` (cannot be changed)
- **Optional Fields**:  
  - `name`, `lat`, `lon`, `addr`, `floors`, `size`
- **Purpose**: Update a House’s mutable fields.  
- **Sample Response**:  
  ```json
  {
    "message": "House with uid=<UID> updated"
  }
  ```

#### 4. `/house/query`
- **Method**: `POST` or `GET`
- **Optional Fields**:  
  - `name`, `lat`, `lon`, `addr`, `uid`
- **Purpose**: Query Houses by given fields, or all if no fields are provided.  
- **Sample Response**:  
  ```json
  {
    "message": "House query result",
    "query_params": {
      "name": "...",
      "uid": "...",
      "...": "..."
    }
  }
  ```

---

## Example Requests

Below are some basic examples using `cURL` (with `POST` shown here as an example):

1. **Add House**  
   ```bash
   curl -X POST -H "Content-Type: application/json" \
   -d '{"name":"MyHouse","lat":10,"lon":20,"addr":"Some address","uid":"house_123","floors":2,"size":120}' \
   http://localhost:5000/house/add
   ```

2. **Remove Room**  
   ```bash
   curl -X POST -H "Content-Type: application/json" \
   -d '{"name":"LivingRoom","belong_to_house":"house_123"}' \
   http://localhost:5000/room/remove
   ```

3. **Query Device (GET)**  
   ```bash
   curl -X GET "http://localhost:5000/device/query?name=Light1&belong_to_room=room_456"
   ```

---

## Future Improvements

1. **Data Persistence**: Integrate MySQL, PostgreSQL, MongoDB, or other databases, and implement actual CRUD logic.  
2. **Stricter Parameter Validation**: Use `pydantic` or `marshmallow` for more advanced validation and automatic documentation generation.  
3. **Authentication & Authorization**: Add user authentication (e.g., token-based or OAuth2) and permission control for house-user relationships.  
4. **Modular Design**: Use Flask Blueprints to separate Houses, Rooms, Devices, Users, etc. into distinct modules for better maintainability and scalability.  
5. **Additional Business Logic**: For instance, data collection from devices, automatic control, scene linkage, and other core smart home features.

---

**Thank you for using this sample project!**  
If you have any questions or suggestions, feel free to reach out and discuss.

