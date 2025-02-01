from flask import request, jsonify
from config.db_config import db, User

# 📌 1. Create a new user (POST)
def create_user():
    try:
        data = request.json
        new_user = User(
            first_name=data["first_name"],
            last_name=data.get("last_name"),
            mobile_number=data["mobile_number"],
            password=data["password"],
            profile_image=data.get("profile_image"),
            created_by=data.get("created_by", -1),
            last_modified_by=data.get("last_modified_by", -1),
            user_type=data.get("user_type", "BUYER")
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully", "user_id": new_user.user_id}), 201
    except Exception as e:
        return jsonify({"status":"ERRROR","message": f"{str(e.__dict__['orig']) }"}), 500

# 📌 2. Get all users (GET)
def get_users():
    users = User.query.all()
    users_list = [
        {
            "user_id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "mobile_number": user.mobile_number,
            "profile_image": user.profile_image,
            "created_date": user.created_date,
            "created_by": user.created_by,
            "last_modified_date": user.last_modified_date,
            "last_modified_by": user.last_modified_by,
            "user_type": user.user_type,
        }
        for user in users
    ]
    return jsonify(users_list), 200

# 📌 3. Get a single user by ID (GET)
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "user_id": user.user_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "mobile_number": user.mobile_number,
        "profile_image": user.profile_image,
        "created_date": user.created_date,
        "created_by": user.created_by,
        "last_modified_date": user.last_modified_date,
        "last_modified_by": user.last_modified_by,
        "user_type": user.user_type,
    }), 200

# 📌 4. Update user by ID (PUT)
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.mobile_number = data.get("mobile_number", user.mobile_number)
    user.password = data.get("password", user.password)
    user.profile_image = data.get("profile_image", user.profile_image)
    user.last_modified_by = data.get("last_modified_by", user.last_modified_by)
    user.user_type = data.get("user_type", user.user_type)

    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

# 📌 5. Delete user by ID (DELETE)
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200


# 📌 6. Find user by mobile_number and password (GET)
def find_user_by_credentials():
    data = request.json

    if not data['mobile_number'] or not data['password']:
        return jsonify({"message": "Mobile number and password are required"}), 400

    # Query the database to find the user based on mobile_number and password
    user = User.query.filter_by(mobile_number=data['mobile_number'], password=data['password']).first()

    if not user:
        return jsonify({"message": "Invalid mobile number or password"}), 404

    # Return the user details
    return jsonify({
        "user_id": user.user_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "mobile_number": user.mobile_number,
        "profile_image": user.profile_image,
        "created_date": user.created_date,
        "created_by": user.created_by,
        "last_modified_date": user.last_modified_date,
        "last_modified_by": user.last_modified_by,
        "user_type": user.user_type,
    }), 200
