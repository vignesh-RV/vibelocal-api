from flask import Flask, request, jsonify
from config.db_config import db, Shop

# ========================= CRUD OPERATIONS =========================

# 📌 1. Create a new shop (POST)
#@app.route("/shops", methods=["POST"])
def create_shop():
    try:
        data = request.json
        new_shop = Shop(
            shop_name=data["shop_name"],
            shop_logo=data["shop_logo"],
            category=data["category"],
            offer=data.get("offer"),
            location=data["location"],
            owner_id=data["owner_id"],
            phone_number=data.get("phone_number"),
            created_by=data.get("created_by", -1),
            last_modified_by=data.get("last_modified_by", -1),
        )
        db.session.add(new_shop)
        db.session.commit()
        return jsonify({"message": "Shop created successfully", "shop_id": new_shop.shop_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating shop: {str(e)}"}), 500

# 📌 2. Get all shops (GET)
#@app.route("/shops", methods=["GET"])
def get_all_shops():
    try:
        shops = Shop.query.all()
        if not shops:
            return jsonify({"message": "No shops found"}), 404
        
        shops_list = [
            {
                "shop_id": shop.shop_id,
                "shop_name": shop.shop_name,
                "shop_logo": shop.shop_logo,
                "category": shop.category,
                "offer": shop.offer,
                "location": shop.location,
                "owner_id": shop.owner_id,
                "phone_number": shop.phone_number,
                "created_date": shop.created_date,
                "created_by": shop.created_by,
                "last_modified_date": shop.last_modified_date,
                "last_modified_by": shop.last_modified_by
            } for shop in shops
        ]
        return jsonify(shops_list), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching shops: {str(e)}"}), 500

# 📌 3. Get a single shop by ID (GET)
#@app.route("/shops/<int:shop_id>", methods=["GET"])
def get_shop(shop_id):
    try:
        shop = Shop.query.get(shop_id)
        if not shop:
            return jsonify({"message": "Shop not found"}), 404
        
        return jsonify({
            "shop_id": shop.shop_id,
            "shop_name": shop.shop_name,
            "shop_logo": shop.shop_logo,
            "category": shop.category,
            "offer": shop.offer,
            "location": shop.location,
            "owner_id": shop.owner_id,
            "phone_number": shop.phone_number,
            "created_date": shop.created_date,
            "created_by": shop.created_by,
            "last_modified_date": shop.last_modified_date,
            "last_modified_by": shop.last_modified_by
        }), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching shop: {str(e)}"}), 500

# 📌 4. Update shop by ID (PUT)
#@app.route("/shops/<int:shop_id>", methods=["PUT"])
def update_shop(shop_id):
    try:
        shop = Shop.query.get(shop_id)
        if not shop:
            return jsonify({"message": "Shop not found"}), 404
        
        data = request.json
        shop.shop_name = data.get("shop_name", shop.shop_name)
        shop.shop_logo = data.get("shop_logo", shop.shop_logo)
        shop.category = data.get("category", shop.category)
        shop.offer = data.get("offer", shop.offer)
        shop.location = data.get("location", shop.location)
        shop.owner_id = data.get("owner_id", shop.owner_id)
        shop.phone_number = data.get("phone_number", shop.phone_number)
        shop.last_modified_by = data.get("last_modified_by", shop.last_modified_by)

        db.session.commit()
        return jsonify({"message": "Shop updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating shop: {str(e)}"}), 500

# 📌 5. Delete shop by ID (DELETE)
#@app.route("/shops/<int:shop_id>", methods=["DELETE"])
def delete_shop(shop_id):
    try:
        shop = Shop.query.get(shop_id)
        if not shop:
            return jsonify({"message": "Shop not found"}), 404

        db.session.delete(shop)
        db.session.commit()
        return jsonify({"message": "Shop deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting shop: {str(e)}"}), 500
