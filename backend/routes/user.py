from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from commons.libs.get_random_nickname import get_random_nickname
from model import User
from model import db

# 1. 创建蓝图对象
# 参数：蓝图名, 当前模块名, url_prefix 路由前缀(可选)
user_page = Blueprint('user', __name__, url_prefix='/user')


# 2. 写该模块下的路由
@user_page.route('/list', methods=['GET'])
def get_user():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "mobile": user.mobile,
            "email": user.email,
            "password": user.password,
            "sex": user.sex,
            "create_time": user.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": user.update_time.strftime("%Y-%m-%d %H:%M:%S"),
            "vip": user.vip,
            "add": user.add
        })
    return jsonify({
        "code": 200,
        "message": "获取用户数据成功",
        "data": user_list
    })


@user_page.route(rule='/add', methods=['POST'])
def add_user():
    # 1. 获取前端传过来的json数据
    data = request.get_json()
    if not data:
        return jsonify({"code": 400, "msg": "请求数据不能为空"})

    # 2. 取出表单字段（根据你form里面的字段修改）
    username = data.get("username")
    password = data.get("password")
    mobile = data.get("mobile")
    email = data.get("email")
    sex = data.get('sex')
    add = data.get("add")
    nickname = get_random_nickname()
    password = generate_password_hash(password)

    # 简单校验
    if not username or not password:
        return jsonify({"code": 400, "msg": "用户名和密码不能为空"})

    # 判断用户名是否已存在
    exist_user = User.query.filter_by(username=username).first()
    if exist_user:
        return jsonify({"code": 400, "msg": "用户名已存在"})

    # 3. 创建用户存入数据库
    new_user = User(
        username=username,
        password=password,
        nickname=nickname,
        mobile=mobile,
        email=email,
        sex=sex,
        add=add
    )
    db.session.add(new_user)
    db.session.commit()

    # 4. 返回和前端匹配的结果 code=200 成功
    return jsonify({"code": 200, "msg": "新增用户成功"})


@user_page.route('/edit/<int:id>')
def edit_user(id):
    user = User.query.filter_by(id=id).first()
    user_list = []
    if not user:
        return jsonify({"code": 400, "msg": "该用户不存在"})
    else:
        user_list.append({
            "username": user.username,
            "nickname": user.nickname,
            "mobile": user.mobile,
            "email": user.email,
            "sex": user.sex,
        })
        return jsonify({"code": 200, "msg": "获取该用户数据成功", "data": user_list})


@user_page.route('/update/<int:id>', methods=['POST'])
def update_user(id):
    # 1. 获取前端传过来的json数据
    data = request.get_json()
    if not data:
        return jsonify({"code": 400, "msg": "请求数据不能为空"})

    # 2. 根据id查询要修改的用户
    user = User.query.get(id)
    if not user:
        return jsonify({"code": 404, "msg": "用户不存在"})

    # 取出表单字段
    username = data.get("username")
    password = data.get("password")
    nickname = data.get("nickname")
    mobile = data.get("mobile")
    email = data.get("email")
    sex = data.get('sex')
    add = data.get("add")

    # 基础校验：用户名不能为空
    if not username:
        return jsonify({"code": 400, "msg": "用户名不能为空"})

    # 判断用户名是否被其他用户占用（排除当前这条自己）
    exist_user = User.query.filter(User.username == username, User.id != id).first()
    if exist_user:
        return jsonify({"code": 400, "msg": "用户名已存在"})

    # 3. 原地修改用户对象，不new新对象
    user.username = username
    # 如果前端不传password，就保留原来密码；传了才更新
    if password:
        user.password = password
    user.nickname = nickname
    user.mobile = mobile
    user.email = email
    user.sex = sex
    user.add = add

    db.session.commit()

    # 4. 返回结果
    return jsonify({"code": 200, "msg": "用户更新成功"})


@user_page.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    # 根据id查找用户
    user = User.query.get(id)
    if not user:
        return jsonify({"code": 404, "msg": "用户不存在"})

    # 删除用户
    db.session.delete(user)
    db.session.commit()

    return jsonify({"code": 200, "msg": "删除用户成功"})
