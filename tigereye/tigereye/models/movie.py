from tigereye.models import db, Model


class Movie(db.Model, Model):
    """电影信息表"""

    """电影ID，主键"""
    mid = db.Column(db.Integer, primary_key=True)
    """电影名称"""
    name = db.Column(db.String(64), nullable=False)
    """语言"""
    language = db.Column(db.String(32))
    """字幕"""
    subtitle = db.Column(db.String(32))
    """上映时间"""
    show_date = db.Column(db.Date)
    """电影格式，比如胶字、数字"""
    mode = db.Column(db.String(16))
    """放映类型，3D 2D"""
    vision = db.Column(db.String(16))
    """屏幕尺寸"""
    screen_size = db.Column(db.String(16))
    """内容简介"""
    introduction = db.Column(db.Text)
    """状态"""
    status = db.Column(db.Integer, default=0, nullable=False, index=True)