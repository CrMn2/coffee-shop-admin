# coding: utf-8
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, info='类别id')
    type_name = db.Column(db.String(50), nullable=False, info='类别名称')


class Juice(db.Model):
    __tablename__ = 'juice'

    id = db.Column(db.Integer, primary_key=True)
    juice_type = db.Column(db.ForeignKey('category.id'), nullable=False, index=True, info='饮品类别，关联category.id')
    content = db.Column(db.String(500), info='简介')
    title = db.Column(db.String(100), nullable=False, info='名称')
    price = db.Column(db.Numeric(10, 2), nullable=False, info='价格')
    vip_price = db.Column(db.Numeric(10, 2), info='会员价')
    sales = db.Column(db.Integer, server_default=db.FetchedValue(), info='销售量')
    is_recommend = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否推荐，0不推荐1推荐')

    category = db.relationship('Category', primaryjoin='Juice.juice_type == Category.id', backref='juices')


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False, index=True, info='关联用户id，关联user.id')
    juice_id = db.Column(db.ForeignKey('juice.id'), nullable=False, index=True, info='关联饮品id，关联juice.id')
    juice_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='饮品数量')
    create_time = db.Column(db.DateTime, server_default=db.FetchedValue(), info='订单创建时间')
    sum_price = db.Column(db.Numeric(10, 2), nullable=False, info='价格')
    user_add = db.Column(db.String(255), info='订单地址')

    juice = db.relationship('Juice', primaryjoin='Order.juice_id == Juice.id', backref='orders')
    user = db.relationship('User', primaryjoin='Order.user_id == User.id', backref='orders')


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, info='自增id')
    username = db.Column(db.String(50), nullable=False, info='用户名，登录时使用')
    nickname = db.Column(db.String(50), info='用户昵称，注册随机生成，可修改')
    mobile = db.Column(db.String(11), info='手机号')
    email = db.Column(db.String(100), info='邮件')
    sex = db.Column(db.Integer, server_default=db.FetchedValue(), info='性别，0未知，1男，2女')
    password = db.Column(db.String(255), nullable=False, info='用户登录密码')
    create_time = db.Column(db.DateTime, server_default=db.FetchedValue(), info='用户创建时间')
    update_time = db.Column(db.DateTime, server_default=db.FetchedValue(), info='用户信息更新时间')
    vip = db.Column(db.Integer, server_default=db.FetchedValue(), info='用户是否是vip用户 0否1是')
    add = db.Column(db.Text, info='用户地址')
