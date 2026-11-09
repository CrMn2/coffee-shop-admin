from flask import Blueprint, request, jsonify
from model import Order, User, Juice, Category

order_page = Blueprint('order_page', __name__, url_prefix="/order")


@order_page.route("/list", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    order_list = []
    if not orders:
        return jsonify({
            "code": 400,
            "message": "数据库中没有数据"
        })
    for order in orders:
        order_list.append({
            "id": order.id,
            "user": order.user.username,
            "juice": order.juice.title,
            "price": order.sum_price,
            "address": order.user_add,
            "date": order.create_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify({
        "code": 200,
        "message": "订单数据获取成功",
        "data": order_list
    })
