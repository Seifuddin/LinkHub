from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="colonel",
    password="@Gsu2024",
    database="linkhub"
)

cursor = db.cursor()

@app.route('/')
def home():
    return jsonify({"message": "Flask Backend is Running!"})

# Add a computer
@app.route('/add_computer', methods=['POST'])
def add_computer():
    data = request.json
    cursor.execute(
        "INSERT INTO computers (brand, name, processor, ram, capacity, shelf) VALUES (%s, %s, %s, %s, %s, %s)",
        (data['brand'], data['name'], data['processor'], data['ram'], data['capacity'], data['shelf'])
    )
    db.commit()
    return jsonify({"message": "Computer added successfully!"})

# Search for computers by name
@app.route('/search_computers', methods=['GET'])
def search_computers():
    name = request.args.get('name', '')
    cursor.execute("SELECT id, brand, name, processor, ram, capacity, shelf FROM computers WHERE name LIKE %s", ('%' + name + '%',))
    results = cursor.fetchall()

    # Structure results properly
    computers = []
    for row in results:
        computers.append({
            "id": row[0],
            "brand": row[1],
            "name": row[2],
            "processor": row[3],
            "ram": row[4],
            "capacity": row[5],
            "shelf": row[6]
        })

    return jsonify(computers)

if __name__ == '__main__':
    app.run(debug=True)