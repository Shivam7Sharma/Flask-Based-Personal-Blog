from flask import Blueprint, request, jsonify, session
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, BlogPost, db
from app import mongo

routes_blueprint = Blueprint('routes', __name__)

# User Registration Endpoint


@routes_blueprint.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400

    hashed_password = generate_password_hash(data['password']).decode('utf-8')
    new_user = User(email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    # Log to MongoDB
    mongo.db.logs.insert_one({"action": "register", "email": data['email']})
    return jsonify({'message': 'User registered successfully'})

# User Login Endpoint


@routes_blueprint.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        login_user(user)
        session['user_id'] = user.id

        # Debugging
        print({"message": "Login successful", "token": str(user.id)})

        return jsonify({'message': 'Login successful', 'token': str(user.id)})

    print({"error": "Invalid credentials"})
    return jsonify({'error': 'Invalid credentials'}), 401


# Fetch Blogs for the Logged-in User


def get_user_from_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None, 'Authorization header is missing'
    try:
        token = auth_header.split(' ')[1]
        user = User.query.get(token)
        if not user:
            return None, 'Invalid token'
        return user, None
    except IndexError:
        return None, 'Token is malformed'


@routes_blueprint.route('/api/posts', methods=['GET'])
def get_posts():
    user, error = get_user_from_token()
    if error:
        return jsonify({'error': error}), 401

    posts = BlogPost.query.filter_by(user_id=user.id).all()
    return jsonify([post.to_dict() for post in posts])


@routes_blueprint.route('/api/myblogs', methods=['GET'])
@login_required
def get_user_blogs():
    user_id = session.get('user_id')
    blogs = BlogPost.query.filter_by(user_id=user_id).all()

    # Convert blogs to dictionary format
    blogs_data = [
        {
            "id": blog.id,
            "title": blog.title,
            "content": blog.content,
            "date_posted": blog.date_posted.strftime("%Y-%m-%d %H:%M:%S")
        }
        for blog in blogs
    ]
    return jsonify({"blogs": blogs_data})

# Create a New Blog Post


@routes_blueprint.route('/api/posts', methods=['POST'])
@login_required
def create_post():
    data = request.json
    user_id = session.get('user_id')

    if not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Title and Content are required'}), 400

    new_post = BlogPost(
        title=data['title'],
        content=data['content'],
        user_id=user_id
    )
    db.session.add(new_post)
    db.session.commit()

    return jsonify({'message': 'Post created successfully'})
