# Smart Home API

This project provides a RESTful API for managing smart home systems, including houses, rooms, and devices. The API is built using Flask and stores data in local JSON files.

## Features
- **House Management**: Add, remove, update, and query houses.
- **Room Management**: Add, remove, update, and query rooms within a house.
- **Device Management**: Add, remove, update, and query devices within a room.
- **Data Persistence**: Uses JSON files for local data storage.

## Requirements
- Python 3.x
- Flask

You can install Flask using:
```bash
pip install flask
```

## API Endpoints

### House Endpoints
- **Add House**
  - `POST /house/add`
  - Required fields: `name`, `lat`, `lon`, `addr`, `floors`, `size`
  - Returns: `uid` (Unique Identifier)

- **Remove House**
  - `POST /house/remove`
  - Required field: `uid`
  - Deletes the house and its associated rooms and devices.

- **Update House**
  - `POST /house/update`
  - Required field: `uid`
  - Optional fields: `name`, `lat`, `lon`, `addr`, `floors`, `size`

- **Query Houses**
  - `GET /house/query`
  - Optional filters: `name`, `lat`, `lon`, `addr`, `uid`
  - Returns a list of matching houses.

### Room and Device Endpoints
(Implementation follows a similar pattern as the house endpoints)

## Running the Application
Run the Flask server using:
```bash
python app.py
```
By default, the application runs on `http://127.0.0.1:5000/`.

## Data Storage
- Houses are stored in `houses.json`.
- Rooms are stored in `rooms.json`.
- Devices are stored in `devices.json`.

## Future Enhancements
- Improve error handling and validation.
- Migrate data storage from JSON to a database.
- Implement authentication and access control.

## License
This project is open-source and available under the MIT License.

