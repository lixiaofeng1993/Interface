from tigereye.models import db, Model


class Play(db.Model, Model):
    """排期表，存储排期相关信息"""

    """排期ID，主键"""
    pid = db.Column(db.Integer, primary_key=True)
    """电影院ID"""
    cid = db.Column(db.Integer, default=0, nullable=False)
    """影厅ID"""
    hid = db.Column(db.Integer, default=0, nullable=False)
    """电影ID"""
    mid = db.Column(db.Integer, default=0, nullable=False)
    """放映开始时间"""
    start_time = db.Column(db.DateTime, nullable=False)
    """放映时长"""
    duration = db.Column(db.Integer, default=0, nullable=False)
    """价格类型"""
    price_type = db.Column(db.Integer)
    """价格"""
    price = db.Column(db.Integer)
    """销售价格"""
    market_price = db.Column(db.Integer)
    """最低价格"""
    lowest_price = db.Column(db.Integer)
    """创建时间"""
    created_time = db.Column(db.DateTime)
    """最后更新时间"""
    updated_time = db.Column(db.DateTime)
    """状态"""
    status = db.Column(db.Integer, default=0, nullable=False, index=True)


