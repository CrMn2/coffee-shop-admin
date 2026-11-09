from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import jwt
import os
import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('', methods=['POST'])
def login():
    # 读取json数据
    data = request.get_json()
    if not data:
        return jsonify({
            "code": 400,
            "msg": "账号或密码为空"
        })
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({
            "code": 400,
            "msg": "账号或密码为空"
        })

    # 后台密码通过环境变量注入；未配置时一律拒绝登录（fail closed）
    admin_password = os.getenv('ADMIN_PASSWORD', '')
    if username == 'admin' and admin_password and password == admin_password:
        expire = datetime.utcnow() + timedelta(minutes=30)
        payload = {
            "sub": username,
            "exp": expire
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return jsonify({
            "code": 200,
            "msg": "登录成功",
            "data": {
                "token": token
            }
        })
    else:
        return jsonify({
            "code": 401,
            "msg": "账号或密码错误"
        })
