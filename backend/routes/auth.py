from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from commons.libs.get_random_nickname import get_random_nickname
from model import User, db, Juice, Order, Category
import settings
import jwt
import datetime
import re
import json

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
SECRET_KEY = settings.SECRET_KEY

# 昵称词库，咖啡主题
prefix_list = ["咖啡", "拿铁", "美式", "摩卡", "瑞幸", "冰吸", "椰云", "生椰", "陨石", "厚乳"]
suffix_list = ["爱好者", "达人", "星友", "玩家", "小主", "食客", "追光者", "少年", "晚风", "橘子"]


@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json(silent=True) or request.form
    username = data.get('username')
    password = data.get('password')
    if not all([username, password]):
        return jsonify({"code": 400, "msg": "账号和密码不能为空"})

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"code": 401, "msg": "用户名或密码错误"})

    payload = {
        "uid": user.id,
        "username": user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "code": 200,
        "msg": "登录成功",
        "data": {
            "token": token,
            "uid": user.id,
            "username": user.username,
            'nickname': user.nickname,
            'mobile': user.mobile,
            'address': user.add,
            'sex': user.sex,
            'vip': user.vip
        }
    })


@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json(silent=True) or request.form
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({"code": 400, "msg": "账号和密码不能为空"})

    if User.query.filter_by(username=username).first():
        return jsonify({"code": 409, "msg": "用户名已被占用"})

    if len(password) < 6:
        return jsonify({"code": 400, "msg": "密码至少6位"})

    hash_pwd = generate_password_hash(password)
    new_nick = get_random_nickname()

    new_user = User(
        username=username,
        password=hash_pwd,
        nickname=new_nick,
        mobile=data.get('mobile') or "",
        add="",
        sex=data.get('sex') or 0,  # 0 而不是 ""
        vip=0
    )
    db.session.add(new_user)
    db.session.commit()

    # 注册成功直接生成token，和登录接口逻辑一样
    payload = {
        "uid": new_user.id,
        "username": new_user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    # 返回结构和登录完全一样！前端一套代码处理登录/注册成功
    return jsonify({
        "code": 200,
        "msg": "注册成功",
        "data": {
            "token": token,
            "uid": new_user.id,
            "username": new_user.username,
            "nickname": new_user.nickname,
            "mobile": new_user.mobile,
            "address": new_user.add,
            "sex": new_user.sex,
            "vip": new_user.vip
        }
    })


@auth_bp.route('/edit', methods=['POST'])
def edit_user():
    data = request.get_json(silent=True) or request.form

    # 和 login 发 token 对应，从 header 里解出来确认是谁在改
    token = request.headers.get('Authorization', '')
    if token.startswith('Bearer '):
        token = token[7:]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except Exception:
        return jsonify({"code": 401, "msg": "登录已过期，请重新登录"}), 401

    user = User.query.get(payload.get('uid'))
    if not user:
        return jsonify({"code": 401, "msg": "用户不存在，请重新登录"}), 401

    nickname = (data.get('nickname') or '').strip()
    mobile = (data.get('mobile') or '').strip()
    email = (data.get('email') or '').strip()
    address = (data.get('add') or data.get('address') or '').strip()
    sex = data.get('sex')

    if not nickname:
        return jsonify({"code": 400, "msg": "昵称不能为空"})
    if mobile and not re.match(r'^1[3-9]\d{9}$', mobile):
        return jsonify({"code": 400, "msg": "手机号格式不对"})
    if email and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return jsonify({"code": 400, "msg": "邮箱格式不对"})
    # 昵称别的用户占用就不让用，自己原来的不算
    if User.query.filter(User.nickname == nickname, User.id != user.id).first():
        return jsonify({"code": 409, "msg": "昵称已被占用"})

    try:
        sex = int(sex) if sex is not None and str(sex) != '' else 0
    except (TypeError, ValueError):
        sex = 0
    if sex not in (0, 1, 2):
        sex = 0

    user.nickname = nickname
    user.mobile = mobile
    user.email = email
    user.add = address
    user.sex = sex
    db.session.commit()

    # 返回结构和登录完全一样，前端一套代码处理
    return jsonify({
        "code": 200,
        "msg": "修改成功",
        "data": {
            "uid": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "mobile": user.mobile,
            "email": user.email,
            "address": user.add,
            "sex": user.sex,
            "vip": user.vip
        }
    })


@auth_bp.route('/address', methods=['POST'])
def add_address():
    data = request.get_json(silent=True) or request.form

    # 鉴权方式和你刚写的 edit 一样
    token = request.headers.get('Authorization', '')
    if token.startswith('Bearer '):
        token = token[7:]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except Exception:
        return jsonify({"code": 401, "msg": "登录已过期，请重新登录"}), 401

    user = User.query.get(payload.get('uid'))
    if not user:
        return jsonify({"code": 401, "msg": "用户不存在，请重新登录"}), 401

    address = (data.get('address') or '').strip()
    if not address:
        return jsonify({"code": 400, "msg": "地址不能为空"})
    if len(address) > 100:
        return jsonify({"code": 400, "msg": "地址最长100个字符"})

    # add 存的是 '["地址a","地址b"]' 这种 JSON 数组字符串
    try:
        addr_list = json.loads(user.add) if user.add else []
        if not isinstance(addr_list, list):
            addr_list = []
    except Exception:
        addr_list = []

    if address in addr_list:
        return jsonify({"code": 409, "msg": "地址已存在"})

    addr_list.append(address)
    user.add = json.dumps(addr_list, ensure_ascii=False)  # 不要 \u 转义，好调试
    db.session.commit()

    # 直接返回全量列表，前端拿到就渲染
    return jsonify({"code": 200, "msg": "添加成功", "data": addr_list})


@auth_bp.route('/pay', methods=['POST'])
def pay_order():
    data = request.get_json(silent=True) or request.form

    # ---- 鉴权（同 edit / address）----
    token = request.headers.get('Authorization', '')
    if token.startswith('Bearer '):
        token = token[7:]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except Exception:
        return jsonify({"code": 401, "msg": "登录已过期，请重新登录"}), 401
    user = User.query.get(payload.get('uid'))
    if not user:
        return jsonify({"code": 401, "msg": "用户不存在，请重新登录"}), 401

    # ---- 取参数 ----
    items = data.get('items') or []
    address = (data.get('address') or '').strip()
    if not items:
        return jsonify({"code": 400, "msg": "订单不能为空"})
    if not address:
        return jsonify({"code": 400, "msg": "请先填写收货地址"})
    if len(address) > 255:
        return jsonify({"code": 400, "msg": "地址过长"})

    is_vip = (user.vip == 1)

    # ---- 逐个饮品创建 Order 行，销量 +num ----
    new_orders = []
    total = 0.0
    for item in items:
        try:
            juice_id = int(item.get('id'))
        except (TypeError, ValueError):
            return jsonify({"code": 400, "msg": "商品参数错误"}), 400
        try:
            num = int(item.get('count') or 0)
        except (TypeError, ValueError):
            num = 0
        if num <= 0:
            continue

        juice = Juice.query.get(juice_id)
        if not juice:
            db.session.rollback()
            return jsonify({"code": 400, "msg": "商品不存在或已下架"}), 400

        # 价格以后端为准；VIP 用会员价（没配会员价就退回原价）
        price = juice.price
        if is_vip and juice.vip_price is not None:
            price = juice.vip_price
        row_price = round(float(price) * num, 2)

        order = Order(
            user_id=user.id,
            juice_id=juice.id,
            juice_num=num,
            sum_price=row_price,
            user_add=address
        )
        # 销量 + 购买数量
        juice.sales = (juice.sales or 0) + num
        db.session.add(order)
        new_orders.append(order)
        total += row_price

    if not new_orders:
        return jsonify({"code": 400, "msg": "订单数量必须大于 0"}), 400

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"code": 500, "msg": "下单失败，请稍后再试"}), 500

    # ---- 这里就是你自己支付方式的接入点 ----
    # 前端约定：code 200 即支付成功。如果你要接三方支付，
    # 把"生成支付参数返回给前端调起"放在这一步，支付回调里再改订单状态。
    return jsonify({
        "code": 200,
        "msg": "下单成功",
        "data": {
            "order_ids": [o.id for o in new_orders],
            "total": round(total, 2)
        }
    })
