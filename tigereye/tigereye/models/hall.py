from tigereye.models import db, Model


class Hall(db.Model, Model):
    """影厅表"""

    """影厅ID，主键"""
    hid = db.Column(db.Integer, primary_key=True)
    """cid，影院ID"""
    cid = db.Column(db.Integer)
    """影厅名称"""
    name = db.Column(db.String(64), nullable=False)
    """屏幕的类型"""
    screen_type = db.Column(db.String(32))
    """音响类型"""
    audio_type = db.Column(db.String(32))
    """座位数量"""
    seats_num = db.Column(db.Integer, default=0, nullable=False)
    """状态"""
    status = db.Column(db.Integer, default=0, nullable=False, index=True)
