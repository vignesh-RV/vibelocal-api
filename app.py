from controllers.order_products import create_order_product, delete_order_product, get_all_order_products, get_order_product, update_order_product
from controllers.orders import create_order, delete_order, get_all_orders, get_order, update_order
from controllers.products import create_product, delete_product, get_all_products, get_product, get_product_by_shop_id, get_user_Cart_products, update_product
from controllers.shops import create_shop, delete_shop, get_all_shops, get_shop, update_shop
from flask import Flask
from config.db_config import db, app
from controllers.users import create_user, get_users, get_user, update_user, delete_user, find_user_by_credentials
from controllers.cart_items import create_cart_item, get_cart_items_by_user, get_cart_item, update_cart_item, delete_cart_item

# 📌 Register Routes
app.route("/users", methods=["POST"])(create_user)
app.route("/users", methods=["GET"])(get_users)
app.route("/users/<int:user_id>", methods=["GET"])(get_user)
app.route("/users/<int:user_id>", methods=["PUT"])(update_user)
app.route("/users/<int:user_id>", methods=["DELETE"])(delete_user)
app.route("/users/login", methods=["POST"])(find_user_by_credentials)


app.route("/cart_items", methods=["POST"])(create_cart_item)
app.route("/cart_items/byuser/<int:user_id>", methods=["GET"])(get_cart_items_by_user)
app.route("/cart_items/id/<int:cart_item_id>", methods=["GET"])(get_cart_item)
app.route("/cart_items/id/<int:cart_item_id>", methods=["PUT"])(update_cart_item)
app.route("/cart_items/id/<int:cart_item_id>", methods=["DELETE"])(delete_cart_item)


app.route("/shops", methods=["POST"])(create_shop)
app.route("/shops", methods=["GET"])(get_all_shops)
app.route("/shops/<int:shop_id>", methods=["GET"])(get_shop)
app.route("/shops/<int:shop_id>", methods=["PUT"])(update_shop)
app.route("/shops/<int:shop_id>", methods=["DELETE"])(delete_shop)


app.route("/products", methods=["POST"])(create_product)
app.route("/products", methods=["GET"])(get_all_products)
app.route("/products/byshop/<int:shop_id>", methods=["GET"])(get_product_by_shop_id)
app.route("/products/<int:product_id>", methods=["GET"])(get_product)
app.route("/products/<int:product_id>", methods=["PUT"])(update_product)
app.route("/products/<int:product_id>", methods=["DELETE"])(delete_product)
app.route("/products/cart/byuser/<int:user_id>", methods=["GET"])(get_user_Cart_products)

app.route("/orders", methods=["POST"])(create_order)
app.route("/orders", methods=["GET"])(get_all_orders)
app.route("/orders/<int:order_id>", methods=["GET"])(get_order)
app.route("/orders/<int:order_id>", methods=["PUT"])(update_order)
app.route("/orders/<int:order_id>", methods=["DELETE"])(delete_order)

app.route("/order_products", methods=["POST"])(create_order_product)
app.route("/order_products", methods=["GET"])(get_all_order_products)
app.route("/order_products/<int:order_product_id>", methods=["GET"])(get_order_product)
app.route("/order_products/<int:order_product_id>", methods=["PUT"])(update_order_product)
app.route("/order_products/<int:order_product_id>", methods=["DELETE"])(delete_order_product)

# ========================= RUN FLASK SERVER =========================
if __name__ == "__main__":
    app.run(debug=True)
