#app.py
from flask import Flask, request, jsonify, render_template
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
	username = Column(String, unique=True, nullable=False)
	password = Column(String, nullable=False)
	name = Column(String)
	email = Column(String)
	message = Column(String)

# create forum post model
class ForumPost(Base):
	__tablename__ = 'forum_posts'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, nullable=False)
	message = Column(String, nullable=False)
	
# Create the table in the database

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# # Create the table in the database
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()

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
def index():
    return render_template('index.html')


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

# Post a message to the forun
@app.route('/forum/post', methods=['POST'])
def post_message():
	try:
		user_id = request.json.get('user_id')
		message = request.json.get('message')
		if not user_id or not message:
			return jsonify({"error": "User ID and message are required"}), 400
		#enforce that the length of the message is less than 250 characters
		if len(message) < 5 or len(message)>500:
			return jsonify({"error": "Message must be between 5 and 500 characters"}), 400
		
		# check for duplicates in existing posts
		existing_post = session.query(ForumPost).filter_by(user_id=user_id, message=message).first()
		if existing_post: 
			return jsonify({"error": "Post already exists, Duplicate post not allowed"}), 400
			
		# add the post forum 
		new_post = ForumPost(user_id = user_id, message = message)
		session.add(new_post)
		session.commit()
		return jsonify({"message": "Post created successfully!"})
		
	except Exception as e:
		return jsonify({"error": str(e)}), 500

# route to view all the post
@app.route('/forum/messages', methods=["GET"])
def view_messages():
	posts = session.query(ForumPost).all()
	return jsonify([{"id": post.id,	"user_id": post.user_id, "message": post.message} for post in posts])
							

# Update User
@app.route('/users/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
	user = session.query(User).filter_by(id=user_id).first()
	if not user:
		return jsonify({"error": "User not found"}), 404
	
	name = request.json.get('name')
	email = request.json.get('email')
	if name:
		user.name = name
	if email:
		user.email = email
	session.commit()
	return jsonify({"message": "User updated successfully!"})	


#Delete a user and their forum posts
@app.route('/users/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
	user = session.query(User).filter_by(id = user_id).first()
	if not user:
		return jsonify({"error": "User not found"}), 404
	session._query(ForumPost).filter_by(user_id=user_id).delete()
	session.delete(User)
	session.commit()
	return jsonify({"message": "User and associated posts deleted successfully!"})


# Route to list all users
@app.route('/users', methods=['GET'])
def list_users():
	users = session.query(User).all()
	return jsonify([{"id": user.id, "name": user.name, "email": user.email, "message": user.message} for user in users])
	
	
	
	# with sqlite3.connect(DATABASE) as conn:
	# 	cursor = conn.execute('SELECT * FROM users')
	# 	users = [{"id": row[0], "name": row[1], "email": row[2], "message": row[3]} for row in cursor.fetchall()]
	# return jsonify(users)

#signup route
@app.route('/signup', methods=['GET','POST'])
def signup():
	data = request.json
	username = data.get('username')
	password = data.get('password')

	#validate the username and password
	if not username or not password:
		return jsonify({"success": False, "message": "Username and password are required"}), 400
	
	#check if the username already exists
	existing_user = session.query(User).filter_by(username=username).first()
	if existing_user:
		return jsonify({"success": False, "message": "Username already exists"}), 400

	#create a new user
	new_user = User(username=username, password=password)
	session.add(new_user)
	session.commit()
	return jsonify({"success": True, "message": "User created successfully!"})

# Login route
@app.route('/login', methods=['POST'])
def login():
	data = request.json
	username = data.get('username')
	password = data.get('password')

	#validate the username and password
	if not username or not password:
		return jsonify({"success": False, "message": "Username and password are required"}), 400
	
	#check if the username already exists
	user = session.query(User).filter_by(username=username).first()
	if not user:
		return jsonify({"success": False, "message": "Invalid username or password"}), 401
	
	#check if the password is correct
	if user.password != password:
		return jsonify({"success": False, "message": "Invalid username or password"}), 401

	#login successful
	return jsonify({"success": True, "message": "Login successful!"})


# logout route
@app.route('/logout', methods=['POST'])
def logout():
	return jsonify({"success": True, "message": "Logout successful!"})

# Route to get a user by ID
if __name__ == "__main__":

	app.run(debug=True, host='0.0.0.0', port=5001)

