# 饮品门店后台管理系统

面向中小饮品门店的前后端分离管理后台：商品与分类、订单、用户，以及经营数据看板。
独立完成从库表设计、接口开发、前端联调到 Nginx 上线的完整流程。

- 在线演示：<http://101.42.65.153>
- 前端：Vue 3 + Vite + Element Plus + ECharts
- 后端：Flask + Flask-SQLAlchemy + PyJWT + MySQL

## 功能模块

| 模块 | 能力 |
| --- | --- |
| 数据总览 | 用户 / 订单 / 分类 / 饮品总量；近一周、1 个月、3 个月、6 个月、1 年 5 个时间维度的新增用户、新增订单、售出杯数；分类饮品占比饼图 |
| 商品管理 | 饮品增删改查、分类归属、会员价、是否推荐、销量 |
| 分类管理 | 分类列表，供商品表单下拉选择 |
| 订单管理 | 订单列表（下单用户、饮品、金额、收货地址、下单时间） |
| 用户管理 | 用户增删改查、VIP 标记、多收货地址 |
| 登录鉴权 | JWT（HS256）签发与校验，后台令牌 30 分钟过期；前端路由守卫解析 `exp` 判断登录态 |

## 目录结构

```
.
├─ frontend/                     # 前端（Vue 3 + Vite）
│  ├─ src/
│  │  ├─ router/index.js         # 路由表 + 全局前置守卫（JWT 过期校验）
│  │  ├─ utils/request.js        # axios 实例、拦截器、统一错误处理
│  │  ├─ utils/message.js        # 统一消息提示
│  │  └─ views/
│  │     ├─ Home.vue             # 数据总览（ECharts 看板）
│  │     ├─ admin/Admin.vue      # 登录页
│  │     ├─ juice/{Juice,Add,Edit}.vue
│  │     ├─ user/{User,Add,Edit}.vue
│  │     └─ orders/Orders.vue
│  ├─ public/
│  └─ vite.config.js             # /api 代理到 localhost:5000
│
├─ backend/                      # 后端（Flask）
│  ├─ app.py                     # 入口，注册 6 个蓝图、开启 CORS
│  ├─ settings.py                # 配置（已在 .gitignore 中排除）
│  ├─ settings.example.py        # 配置模板
│  ├─ model.py                   # 4 张表：category / juice / orders / user
│  ├─ requirements.txt
│  ├─ routes/
│  │  ├─ admin.py                # 后台登录，签发 JWT
│  │  ├─ auth.py                 # 注册、登录、资料、地址、下单支付
│  │  ├─ index.py                # 数据看板聚合接口
│  │  ├─ juice.py                # 饮品与分类的增删改查
│  │  ├─ orders.py               # 订单列表
│  │  └─ user.py                 # 用户增删改查
│  └─ commons/                   # 工具函数（随机昵称等）
│
├─ README.md
└─ .gitignore
```

## 接口一览

共 19 个接口，按业务拆成 6 个 Flask Blueprint。

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/admin` | 后台登录，返回 JWT |
| POST | `/auth/register` | 注册（密码哈希入库） |
| POST | `/auth/login` | 登录，返回 JWT |
| POST | `/auth/edit` | 修改个人资料（需鉴权） |
| POST | `/auth/address` | 新增收货地址（需鉴权） |
| POST | `/auth/pay` | 下单支付，生成订单并累加销量（需鉴权） |
| GET | `/index` | 数据看板：总量 + 5 个时间维度 + 分类占比 |
| GET | `/juice/list` | 饮品列表 |
| GET | `/juice/edit/<id>` | 饮品详情 |
| POST | `/juice/add` | 新增饮品 |
| POST | `/juice/update` | 修改饮品 |
| POST | `/juice/delete/<id>` | 删除饮品 |
| GET | `/juice/category/list` | 分类列表 |
| GET | `/order/list` | 订单列表 |
| GET | `/user/list` | 用户列表 |
| POST | `/user/add` | 新增用户 |
| GET | `/user/edit/<id>` | 用户详情 |
| POST | `/user/update/<id>` | 修改用户 |
| POST | `/user/delete/<id>` | 删除用户 |

统一响应格式：`{ "code": 200, "message": "...", "data": ... }`

## 数据模型

| 表 | 字段数 | 说明 |
| --- | --- | --- |
| `category` | 2 | 饮品分类 |
| `juice` | 7 | 饮品：名称、简介、价格、会员价、销量、是否推荐、所属分类 |
| `orders` | 8 | 订单：用户、饮品、数量、金额、地址、创建时间 |
| `user` | 11 | 用户：账号、昵称、手机、邮箱、性别、密码哈希、VIP、地址 |

3 个外键：`juice.juice_type → category.id`、`orders.user_id → user.id`、`orders.juice_id → juice.id`，均建立索引。

## 本地运行

**后端**（需 Python 3.9+、MySQL 8）：

```bash
cd backend
cp settings.example.py settings.py     # Windows: copy settings.example.py settings.py
pip install -r requirements.txt

# 配置通过环境变量注入，不要把密码写进代码
export DATABASE_URL="mysql+pymysql://user:password@127.0.0.1:3306/coffee?charset=utf8mb4"
export SECRET_KEY="$(python -c 'import secrets;print(secrets.token_hex(32))')"
export ADMIN_PASSWORD="换成你自己的后台密码"    # 未设置时后台登录一律拒绝

python app.py          # 默认 http://127.0.0.1:5000
```

Windows 用 `set` 或 `$env:DATABASE_URL="..."` 代替 `export`。

**前端**（需 Node 18+）：

```bash
cd frontend
npm install
npm run dev            # http://localhost:5173
npm run build          # 产物输出到 frontend/dist
```

`vite.config.js` 已把 `/api` 代理到 `http://localhost:5000` 并去掉前缀，所以前端请求写 `/api/user/list` 即可命中后端的 `/user/list`。

## 部署

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/coffee/frontend/dist;

    # 前端 SPA：刷新 /user 这类深层路由时回退到 index.html
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 后端接口反向代理
    location /api/ {
        proxy_pass http://127.0.0.1:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 开启压缩，减小首屏体积
    gzip on;
    gzip_comp_level 6;
    gzip_min_length 1024;
    gzip_types text/css application/javascript application/json image/svg+xml;
}
```

## Roadmap

- [ ] 列表接口加分页（当前 `query.all()` 全量返回）
- [ ] 订单列表用 `joinedload` 预加载关联，消除 N+1 查询
- [ ] 看板统计改为 `GROUP BY` 聚合，减少往返次数
- [ ] ECharts 改按需引入，压缩首屏主包体积
- [ ] 生产环境启用 HTTPS（小程序端要求）
- [ ] 补 pytest 接口测试
