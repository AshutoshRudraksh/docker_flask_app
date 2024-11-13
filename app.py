#app.py
from flask import Flask, request, jsonify
import sqlite3


# Create a Flask app
app = Flask(__name__)

#DATABASE setup 
DATABASE = 'app.db'

# Create a connection to the SQLite database
def init_db():
	with sqlite3.connect(DATABASE) as conn:
		try:
			conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, message TEXT)')
			conn.commit()
			print("Table created or updated successfully!")
		except sqlite3.Error as e:
			print(f"Error creating table: {e}")
# Initialize the database
init_db()

# Route to greet a user by name.
@app.route('/')
def home():
	return "Hello, Docker!"

"""
Route to greet a user by name.

This route accepts a name parameter in the URL path and returns a greeting message for the user.

Args:
    name (str): The name of the user to greet.

Returns:
    str: A greeting message for the user.
"""
# Route to greet a user by name.
@app.route('/greet/<name>', methods=['GET'])
def greet(name):
	email = request.args.get('email') # Get email from query parameters
	message = f"Hello, {name}! Welcom to Docker!"	
    #store  the greeting in the database 
	with sqlite3.connect(DATABASE) as conn:
		conn.execute('INSERT INTO users (name, email, message) VALUES (?, ?, ?)', (name, email, message))
		conn.commit()
	return jsonify({"name":name, "email": email, "message": message})

# Route to list all users
@app.route('/users', methods=['GET'])
def list_users():
	with sqlite3.connect(DATABASE) as conn:
		cursor = conn.execute('SELECT * FROM users')
		users = [{"id": row[0], "name": row[1], "email": row[2], "message": row[3]} for row in cursor.fetchall()]
	return jsonify(users)

# Route to get a user by ID
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5001)

