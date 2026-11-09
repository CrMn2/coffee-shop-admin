from flask import Blueprint, jsonify, request
from model import Juice, db, Category

# 1. 创建蓝图对象
# 参数：蓝图名, 当前模块名, url_prefix 路由前缀(可选)
juice_page = Blueprint('juice', __name__, url_prefix='/juice')


# 2. 写该模块下的路由
@juice_page.route('/list', methods=['GET'])
def get_juice():
    juices = Juice.query.all()
    juice_list = []
    for juice in juices:
        juice_list.append({
            "id": juice.id,
            "type": juice.category.type_name,
            "content": juice.content,
            "price": juice.price,
            "vip_price": juice.vip_price,
            "sales": juice.sales,
            "is_recommend": juice.is_recommend,
            "title": juice.title
        })
    return jsonify({
        "code": 200,
        "message": "获取饮品数据成功",
        "data": juice_list
    })


@juice_page.route('/edit/<int:id>', methods=['GET'])
def edit_juice(id):
    juice = Juice.query.filter_by(id=id).first()
    juice_list = []
    if not juice:
        return jsonify({
            "code": 400,
            "msg": "饮品数据不存在"
        })
    else:
        juice_list.append({
            "type": juice.category.type_name,
            "content": juice.content,
            "price": juice.price,
            "vip_price": juice.vip_price,
            "sales": juice.sales,
            "is_recommend": juice.is_recommend,
            "title": juice.title
        })
        return jsonify({
            "code": 200,
            "msg": "获取饮品数据成功",
            "data": juice_list
        })


@juice_page.route('/update', methods=['POST'])
def update_juice():
    # 1. 获取前端json
    data = request.get_json()
    id = data.get('id')
    if not data:
        return jsonify({"code": 400, "msg": "请求数据不能为空"})

    # 2. 查询饮品
    juice = Juice.query.get(id)
    if not juice:
        return jsonify({"code": 404, "msg": "饮品不存在"})

    # 取出前端传过来的饮品字段
    title = data.get("title")
    content = data.get("content")
    price = data.get("price")
    vip_price = data.get("vip_price")
    is_recommend = data.get("is_recommend")

    # 简单校验：饮品名称不能为空
    if not title:
        return jsonify({"code": 400, "msg": "饮品名称不能为空"})

    # 原地修改juice对象，前端不传的字段，就保留数据库原有值
    juice.title = title
    juice.content = content
    juice.price = price
    juice.vip_price = vip_price
    juice.is_recommend = is_recommend

    db.session.commit()
    return jsonify({"code": 200, "msg": "饮品更新成功"})


@juice_page.route('/delete/<int:id>', methods=['POST'])
def delete_juice(id):
    # 根据id查找用户
    juice = Juice.query.get(id)
    if not juice:
        return jsonify({"code": 404, "msg": "饮品不存在"})

    # 删除用户
    db.session.delete(juice)
    db.session.commit()

    return jsonify({"code": 200, "msg": "删除饮品成功"})


@juice_page.route('/add', methods=['POST'])
def add_juice():
    data = request.get_json()
    if not data:
        return jsonify({"code": 400, "msg": "饮品数据缺失"})
    name = data.get("name")
    category = data.get('category')
    intro = data.get('intro')
    price = data.get('price')
    vipPrice = data.get('vipPrice')
    isRecommend = data.get('isRecommend')

    exist_type = Category.query.filter_by(type_name=category).first()
    if not exist_type:
        new_category = Category(type_name=category)
        db.session.add(new_category)
        db.session.flush()
        exist_type = new_category

    if not all([name, category, price, vipPrice]):
        return jsonify({"code": 400, "msg": "饮品数据缺失"})

    # 前端传 0/1，转布尔存入is_recommend
    is_recommend_bool = bool(isRecommend)

    new_juice = Juice(title=name,
                      content=intro,
                      price=price,
                      vip_price=vipPrice,
                      is_recommend=is_recommend_bool,
                      juice_type=exist_type.id,
                      sales=0)
    db.session.add(new_juice)
    db.session.commit()
    return jsonify({"code": 200, "msg": "新增饮品成功"})


# 获取分类下拉列表接口
@juice_page.route('/category/list', methods=['GET'])
def get_category_list():
    category_list = Category.query.all()
    res = []
    for item in category_list:
        res.append({
            "id": item.id,
            "name": item.type_name
        })
    return jsonify({"code":200, "data": res})

