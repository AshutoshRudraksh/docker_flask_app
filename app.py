#app.py
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import sqlite3


# Create a Flask app
app = Flask(__name__)

#DATABASE setup 
DATABASE = "postgresql://user:password@db:5432/app_db"
engine = create_engine(DATABASE)
Base = declarative_base()

# Define a User model
class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True)
	name = Column(String)
	email = Column(String)
	message = Column(String)

# Create the table in the database
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Create a connection to the SQLite database
# def init_db():
# 	with sqlite3.connect(DATABASE) as conn:
# 		try:
# 			conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, message TEXT)')
# 			conn.commit()
# 			print("Table created or updated successfully!")
# 		except sqlite3.Error as e:
# 			print(f"Error creating table: {e}")
# # Initialize the database
# init_db()

#Route to greet a user by name.
@app.route('/')
def home():
	return "Hello, Docker!"

# Route to greet a user by name.
@app.route('/greet/<name>', methods=['GET'])
def greet(name):
	email = request.args.get('email') # Get email from query parameters
	message = f"Hello, {name}! Welcom to Docker!"	
	new_user = User(name=name, email=email, message=message)
	session.add(new_user)
	session.commit()
	return jsonify({"name":name, "email": email, "message": message})	
	
	#store  the greeting in the database 
	# with sqlite3.connect(DATABASE) as conn:
	# 	conn.execute('INSERT INTO users (name, email, message) VALUES (?, ?, ?)', (name, email, message))
	# 	conn.commit()
	# return jsonify({"name":name, "email": email, "message": message})

# Route to list all users
@app.route('/users', methods=['GET'])
def list_users():
	users = session.query(User).all()
	return jsonify([{"id": user.id, "name": user.name, "email": user.email, "message": user.message} for user in users])
	
	
	
	# with sqlite3.connect(DATABASE) as conn:
	# 	cursor = conn.execute('SELECT * FROM users')
	# 	users = [{"id": row[0], "name": row[1], "email": row[2], "message": row[3]} for row in cursor.fetchall()]
	# return jsonify(users)

# Route to get a user by ID
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5001)

