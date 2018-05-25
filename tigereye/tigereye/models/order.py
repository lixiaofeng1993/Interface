from enum import Enum

from random import randint

from sqlalchemy import text
from sqlalchemy.sql import func
from tigereye.helper import tetime
from tigereye.models import db, Model


class OrderStatus(Enum):
    """描述订单状态"""

    """已锁定"""
    locked = 1
    """已经解锁"""
    unlocked = 2
    """已支付"""
    paid = 4
    """已出票"""
    printed = 5
    """已退款"""
    refund = 6



class Order(db.Model, Model):
    """订单表"""

    __tablename__ = 'orders'

    """订单ID，主键"""
    oid = db.Column(db.String(32), primary_key=True)
    """排期ID，主键"""
    pid = db.Column(db.Integer)
    """电影院ID"""
    cid = db.Column(db.Integer, default=0, nullable=False)
    """座位ID"""
    sid = db.Column(db.String(32), nullable=False)
    """取票码"""
    ticket_flag = db.Column(db.String(64))
    """订单总金额"""
    amount = db.Column(db.Integer, default=0, nullable=False)
    """销售方订单号"""
    seller_order_no = db.Column(db.String(32), unique=True)
    """支付时间"""
    paid_time = db.Column(db.DateTime)
    """取票时间"""
    printed_time = db.Column(db.DateTime)
    """创建时间"""
    created_time = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))
    """最后更新时间"""
    updated_time = db.Column(db.DateTime, onupdate=func.now())
    """订单状态"""
    status = db.Column(db.Integer, default=0, nullable=False)

    @classmethod
    def create(cls, cid, pid, sid):
        """根据影院ID，排期ID和座位ID，创建订单对象"""
        order = cls()
        order.oid = '%s%s%s' % (tetime.now(), randint(100000, 999999), pid)
        order.cid = cid
        order.pid = pid
        order.sid = ','.join(str(i) for i in sid)
        return order

    @classmethod
    def getby_orderno(cls, orderno):
        """根据销售方订单号获取order记录"""
        return Order.query.filter_by(seller_order_no=orderno).first()

    def gen_ticket_flag(self):
        """生成取票码"""
        self.ticket_flag = ''.join([str(randint(1000, 9999)) for i in range(8)])

    def validate(self, ticket_flag):
        """验证取票码的有效性"""
        return self.ticket_flag == ticket_flag