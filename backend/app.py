from flask import Flask
from flask_cors import CORS
from routes.user import user_page
from routes.juice import juice_page
from routes.admin import admin
from routes.index import index
from routes.auth import auth_bp
from routes.orders import order_page
from model import db
import settings

app = Flask(__name__)
CORS(app)
# 新增这一行，新版flask关闭unicode转义
app.json.ensure_ascii = False
app.config.from_object(settings)

db.init_app(app)
app.register_blueprint(user_page)
app.register_blueprint(juice_page)
app.register_blueprint(auth_bp)
app.register_blueprint(admin)
app.register_blueprint(index)
app.register_blueprint(order_page)

if __name__ == '__main__':
    # 简单一行打印，直接看所有路由
    print(app.url_map)
    app.run(debug=True)
