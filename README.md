# University Timetable Mini Project-
This project creates a simple web application to display a university timetable based on user input for the academic level. It utilizes Docker for running PostgreSQL as the database and Flask for the web application.

## Project Features

A Flask web application for viewing a university timetable.
PostgreSQL database running inside a Docker container.
Dynamic display of timetable data based on user-selected academic levels.

## Technologies Used

Docker: To containerize the PostgreSQL database.
Flask: As the backend web framework.
PostgreSQL: To store timetable data.
pg8000: A lightweight PostgreSQL driver for Python.

## Prerequisites
Ensure you have the following installed:

Docker
Python 3.7+
A text editor or IDE (e.g., VSCode, PyCharm)
### 1.  Install Docker and Start PostgreSQL in Docker
### Pull the PostgreSQL Docker image:
```
 docker pull postgres:latest
```
### Run a PostgreSQL container:
```
 docker run --name Robiyabonu-db -e POSTGRES_USER=student -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:latest
```
### Verify the container is running:
```
 docker ps
```
### Access the PostgreSQL container:
```
docker exec -it Robiyabonu-db psql -U student
 ```
### 2. Set Up the PostgreSQL Database and Tables
```
CREATE TABLE Timetable (
  id SERIAL PRIMARY KEY,
  course_name VARCHAR(255),
  day VARCHAR(50),
  time VARCHAR(50),
  room VARCHAR(50),
  level INT
  );
INSERT INTO Timetable (id, course_name, day, time, room, level) VALUES
(1,'Introduction to Computer Science', 'Monday', '9:00 AM', 'Room 101', 1),
(2,'Operating Systems', 'Tuesday', '10:00 AM', 'Room 202', 2),
(3,'Database Management Systems', 'Wednesday', '1:00 PM', 'Room 303', 2),
(4,'Data Structures and Algorithms', 'Thursday', '11:00 AM', 'Room 204', 3),
(5,'Machine Learning', 'Friday', '2:00 PM', 'Room 305', 3);
```
### 3. Set Up the Flask Application
1. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```
2. Install the required dependencies:
```
pip install flask pg8000
```
3. Create a Flask application with the following structure:
```
project/
├── app.py
├── templates/
│   ├── index.html
│   ├── timetable.html
├── Dockerfile
├── docker-compose.yml
```
### 4. Create Flask Application
```
from flask import Flask, render_template, request
import psycopg2
import os

# Set up Flask app with the templates directory
template_dir = os.path.abspath('templates/')
app = Flask(__name__, template_folder=template_dir)

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host="db",               # Hostname of the database service in Docker
    database="Robiyabonu",   # Database name
    user='student',          # Database username
    password='password'      # Database password
)

cur = conn.cursor()  # Create a cursor to execute database queries

@app.route("/", methods=["GET", "POST"])
def index():
    """Display the main page and handle level input."""
    if request.method == "POST":
        level = request.form.get("level", "")  # Get level input from the user
        return render_template("timetable.html", level=level, data=[], message="Loading timetable...")
    
    return render_template("index.html")  # Show the input form

@app.route("/timetable", methods=["GET"])
def timetable():
    """Fetch and display the timetable for the selected level."""
    level = request.args.get("level")  # Retrieve the level parameter
    if not level:
        return render_template("timetable.html", data=[], message="Level is required.")
    
    # Query to fetch timetable data for the given level
    query = "SELECT * FROM Timetable WHERE level = %s;"
    cur.execute(query, (level,))
    rows = cur.fetchall()  # Fetch all matching rows
    message = "No data found for this level." if not rows else None
    return render_template("timetable.html", data=rows, message=message)

# Run the app if this file is executed
if __name__ == "__main__":
    app.run(debug=True)

```
### 5. Create a Dockerfile
```
# Use the official Python image as the base image, specifically the slim version of Python 3.9
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt requirements.txt

# Install the Python dependencies listed in the requirements file
RUN pip install -r requirements.txt

# Copy all other files from the current directory on the host machine to the working directory in the container
COPY . .

# Set the default command to run the Flask application
CMD ["python", "app.py"]

```
### 6. Create a docker-compose.yml File
```
version: '3.8'

services:
  db:
    image: postgres:latest  # Use PostgreSQL as the database
    environment:
      POSTGRES_USER: student       # Database username
      POSTGRES_PASSWORD: password  # Database password
      POSTGRES_DB: Robiyabonu      # Database name
    ports:
      - "5433:5432"  # Map host port 5433 to container port 5432
    volumes:
      - ./db-scripts:/docker-entrypoint-initdb.d  # Initialize DB with scripts

  web:
    build: .  # Build the web app from the current directory
    ports:
      - "8000:8000"  # Map host port 8000 to container port 8000
    depends_on:
      - db  # Ensure database starts first

```
### 7. HTML Templates for Flask
index.html 
```
<!DOCTYPE html>
<html>
<head>
    <title>Mini project of <Robiyabonu></title>
</head>
<body>
    <h1>Welcome to the University Timetable!</h1>
    <form action="/timetable" method="GET">
        <label for="level">Select Level:</label>
        <select name="level" id="level">
            <option value="1">Level 1</option>
            <option value="2">Level 2</option>
            <option value="3">Level 3</option>
        </select>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
```
timetable.html 
```
<!DOCTYPE html>
<html>
<head>
    <title>Timetable</title>
</head>
<body>
    <h2>Timetable for Level {{ level }}</h2>
    {% if data %}
    <table border="1">
        <tr>
            <th>Course ID</th>
            <th>Course Name</th>
            <th>Day</th>
            <th>Time</th>
            <th>Room</th>
        </tr>
        {% for row in data %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
            <td>{{ row[4] }}</td>
        </tr>
        {% endfor %}
    </table>
    {% else %}
    <p>{{ message }}</p>
    {% endif %
</body>
</html>
```
### 8. Build and Run the Application
Run the following command to build and start the application with Docker Compose:
```
docker-compose up --build

```
### Accessing the Application
Open your browser and navigate to:
```
http://127.0.0.1:8000/
```
You can now use the application to view timetables by entering a level.
