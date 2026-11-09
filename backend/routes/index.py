from flask import Blueprint, jsonify
from model import Juice, User, Order, Category, db
from sqlalchemy import func
from datetime import datetime, timedelta

index = Blueprint('index', __name__, url_prefix="/index")

@index.route("", methods=["GET"])
def get_dashboard():
    # ========== 1. 全局总数 ==========
    user_total = User.query.count()
    order_total = Order.query.count()
    category_total = Category.query.count()
    juice_total = Juice.query.count()

    # ========== 2. 封装时间范围统计函数 ==========
    def get_stat(begin_time):
        # 新增用户
        new_user = User.query.filter(User.create_time >= begin_time).count()
        # 新增订单
        new_order = Order.query.filter(Order.create_time >= begin_time).count()
        # 统计该时间段内所有订单的饮品总数量（juice_num）
        sale_result = Order.query.filter(Order.create_time >= begin_time).with_entities(Order.juice_num).all()
        drink_sale = sum(item[0] for item in sale_result)
        return new_user, new_order, drink_sale

    now = datetime.now()
    time_list = [
        {"label": "近一周", "start": now - timedelta(days=7), "cardColor": '#e8f4ff'},
        {"label": "近1个月", "start": now - timedelta(days=30), "cardColor": '#fff3e8'},
        {"label": "近3个月", "start": now - timedelta(days=90), "cardColor": '#e8f9ee'},
        {"label": "近6个月", "start": now - timedelta(days=180), "cardColor": '#f3e8ff'},
        {"label": "近1年", "start": now - timedelta(days=365), "cardColor": '#e8fafa'},
    ]
    time_data = []
    for item in time_list:
        nu, no, ds = get_stat(item["start"])
        time_data.append({
            "label": item["label"],
            "newUser": nu,
            "newOrder": no,
            "drinkSale": ds,
            "cardColor": item["cardColor"]
        })

    # ==========3. 饮品类型占比饼图【统计每个分类下饮品的款数】==========
    pie_data = []
    categories = Category.query.all()
    for cat in categories:
        # 统计该分类下一共有多少款饮品Juice
        juice_count = Juice.query.filter(Juice.juice_type == cat.id).count()
        pie_data.append({
            "name": cat.type_name,
            "value": juice_count
        })

    # ========== 返回给前端 ==========
    return jsonify({
        "code": 200,
        "msg": "获取数据成功",
        "data": {
            "overview": {
                "totalUser": user_total,
                "totalOrder": order_total,
                "totalCategory": category_total,
                "totalJuice": juice_total,
                "timeData": time_data
            },
            "drinkPie": pie_data
        }
    })
