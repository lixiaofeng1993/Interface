from datetime import datetime
from enum import Enum
from sqlalchemy import text

from tigereye.models import db, Model


class SeatType(Enum):
    """过道"""
    road = 0
    """单人"""
    single = 1
    """双人"""
    couple = 2


class SeatStatus(Enum):
    """排期座位状态"""

    """正常状态，可购买"""
    ok = 0
    """已锁定"""
    locked = 1
    """已售出"""
    sold = 2
    """已取票"""
    printed = 3


class Seat(db.Model, Model):
    """物理座位表"""

    """座位ID，主键"""
    sid = db.Column(db.Integer, primary_key=True)
    """影厅ID"""
    hid = db.Column(db.Integer)
    """影院ID"""
    cid = db.Column(db.Integer)

    """x座标"""
    x = db.Column(db.Integer, default=0, nullable=False)
    """y座标"""
    y = db.Column(db.Integer, default=0, nullable=False)
    """显示的行名称"""
    row = db.Column(db.String(8))
    """显示的列名称"""
    column = db.Column(db.String(8))

    """区域"""
    area = db.Column(db.String(16))
    """座位类型"""
    seat_type = db.Column(db.String(16))
    """是否是情侣座"""
    love_seats = db.Column(db.String(32))
    """状态"""
    status = db.Column(db.Integer, default=0, nullable=False, index=True)


class PlaySeat(db.Model, Model):
    """排期座位表"""

    """排期座位ID，主键"""
    psid = db.Column(db.Integer, primary_key=True)
    """第三方订单号"""
    orderno = db.Column(db.String(32), index=True)
    """座位ID"""
    sid = db.Column(db.Integer, nullable=False)
    """排期ID"""
    pid = db.Column(db.Integer, nullable=False)
    """影院ID"""
    cid = db.Column(db.Integer, nullable=False)
    """影厅ID"""
    hid = db.Column(db.Integer, nullable=False)
    """x座标"""
    x = db.Column(db.Integer, default=0, nullable=False)
    """y座标"""
    y = db.Column(db.Integer, default=0, nullable=False)
    """显示的行名称"""
    row = db.Column(db.String(8))
    """显示的列名称"""
    column = db.Column(db.String(8))
    """区域"""
    area = db.Column(db.String(16))
    """座位类型"""
    seat_type = db.Column(db.String(16))
    """是否是情侣座"""
    love_seats = db.Column(db.String(32))
    """座位锁定时间"""
    locked_time = db.Column(db.DateTime)
    """创建时间"""
    created_time = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))
    """状态"""
    status = db.Column(db.Integer, default=0, nullable=False, index=True)

    def copy(self, seat):
        """将一个Seat对象中的信息拷贝到PlaySeat对象中"""

        self.sid = seat.sid
        self.cid = seat.cid
        self.hid = seat.hid
        self.x = seat.x
        self.y = seat.y
        self.row = seat.row
        self.column = seat.column
        self.area = seat.area
        self.love_seats = seat.love_seats
        self.seat_type = seat.seat_type
        self.status = seat.status

    @classmethod
    def lock(cls, orderno, pid, sid_list):
        # 创建数据库session
        session = db.create_scoped_session()
        # 查询出pid,status,sid符合锁定条件的座位
        rows = session.query(PlaySeat).filter(
            PlaySeat.pid == pid,
            PlaySeat.status == SeatStatus.ok.value,
            PlaySeat.sid.in_(sid_list)
        # 然后更新这些座位的信息
        ).update({
            'orderno': orderno,
            'status': SeatStatus.locked.value,
            'locked_time': datetime.now()
        }, synchronize_session=False)
        # 如果更新的行数量与我们传入的座位数量不符，则回滚，并返回0
        if rows != len(sid_list):
            session.rollback()
            return 0
        # 如果数量符合，则提交，并返回锁定的座位数量
        session.commit()
        return rows

    @classmethod
    def unlock(cls, orderno, pid, sid_list):
        """解锁play_seat表的锁座信息"""

        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter_by(
            orderno=orderno,
            status=SeatStatus.locked.value
        ).update({
            'orderno': None,
            'status': SeatStatus.ok.value,
        }, synchronize_session=False)
        # 如果更新的行数量与我们传入的座位数量不符，则回滚，并返回0
        if rows != len(sid_list):
            session.rollback()
            return 0
        # 如果数量符合，则提交，并返回锁定的座位数量
        session.commit()
        return rows

    @classmethod
    def buy(cls, orderno, pid, sid_list):
        """购买座位"""
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter_by(
            orderno=orderno,
            status=SeatStatus.locked.value
        ).update({
            'status': SeatStatus.sold.value,
        }, synchronize_session=False)
        # 如果更新的行数量与我们传入的座位数量不符，则回滚，并返回0
        if rows != len(sid_list):
            session.rollback()
            return 0
        # 如果数量符合，则提交，并返回锁定的座位数量
        session.commit()
        return rows

    @classmethod
    def refund(cls, orderno, pid, sid_list):
        """退款，修改座位状态"""
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter_by(
            orderno=orderno,
            status=SeatStatus.sold.value
        ).update({
            # 修改座位状态为正常，并将订单号设为空
            'status': SeatStatus.ok.value,
            'orderno': None,
        }, synchronize_session=False)
        # 如果更新的行数量与我们传入的座位数量不符，则回滚，并返回0
        if rows != len(sid_list):
            session.rollback()
            return 0
        # 如果数量符合，则提交，并返回锁定的座位数量
        session.commit()
        return rows

    @classmethod
    def print_tickets(cls, orderno, pid, sid_list):
        """执行取票操作，修改座位状态"""
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter_by(
            orderno=orderno,
            status=SeatStatus.sold.value
        ).update({
            # 修改座位状态为正常，并将订单号设为空
            'status': SeatStatus.printed.value,
            # 'orderno': None,
        }, synchronize_session=False)
        # 如果更新的行数量与我们传入的座位数量不符，则回滚，并返回0
        if rows != len(sid_list):
            session.rollback()
            return 0
        # 如果数量符合，则提交，并返回锁定的座位数量
        session.commit()
        return rows