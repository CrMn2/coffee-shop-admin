"""配置模板：复制为 settings.py 后填入真实值（settings.py 已在 .gitignore 中排除）。

    copy settings.example.py settings.py

推荐用环境变量注入，不要把密码写进代码。
"""

import os

SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://user:password@127.0.0.1:3306/coffee?charset=utf8mb4",
)

SQLALCHEMY_TRACK_MODIFICATIONS = False

# 生成方式：python -c "import secrets;print(secrets.token_hex(32))"
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-before-deploy")

# 后台登录密码，通过环境变量 ADMIN_PASSWORD 注入
