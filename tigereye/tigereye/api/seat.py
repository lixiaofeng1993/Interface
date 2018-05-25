from datetime import datetime

from flask import request
from flask_classy import route

from tigereye.api import ApiView
from tigereye.extensions.validator import Validator, multi_int, multi_complex_int
from tigereye.helper.code import Code
from tigereye.models.order import Order, OrderStatus
from tigereye.models.play import Play
from tigereye.models.seat import PlaySeat


class SeatView(ApiView):

    @Validator(pid=int, sid=multi_int, price=int, orderno=str)
    @route('/lock/', methods=['POST'])
    def lock(self):
        pid = request.params['pid']
        sid = request.params['sid']
        price = request.params['price']
        orderno = request.params['orderno']
        play = Play.get(pid)
        if not play:
            return Code.play_does_not_exist, {'pid': pid}
        if price < play.lowest_price:
            return Code.price_less_than_the_lowest_price, {'price': price}

        locked_seat_num = PlaySeat.lock(orderno, pid, sid)
        if not locked_seat_num:
            return Code.seat_lock_failed, {'lock_seat_num': locked_seat_num}
        order = Order.create(play.cid, pid, sid)
        order.seller_order_no = orderno
        order.status = OrderStatus.locked.value
        order.save()
        return {'locked_seat_num': locked_seat_num}

    @Validator(pid=int, sid=multi_int, orderno=str)
    @route('/unlock/', methods=['POST'])
    def unlock(self):
        pid = request.params['pid']
        sid = request.params['sid']
        orderno = request.params['orderno']
        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {'orderno': orderno}
        if order.status != OrderStatus.locked.value:
            return Code.order_status_error, {}
        unlocked_seats_num = PlaySeat.unlock(orderno, pid, sid)
        if not unlocked_seats_num:
            return Code.seat_unlock_failed, {}
        order.status = OrderStatus.unlocked.value
        order.save()
        return {'unlocked_seats_num': unlocked_seats_num}

    # "1-2-3,1-2-3"
    #[(1,2,3),(1,2,3)]
    @Validator(seats=multi_complex_int, orderno=str)
    @route('/buy/', methods=['POST'])
    def buy(self):
        seats = request.params['seats']
        orderno = request.params['orderno']
        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {'orderno': orderno}
        if order.status != OrderStatus.locked.value:
            return Code.order_status_error, {}
        sid_list = []
        for sid, handle_fee, price in seats:
            order.amount += handle_fee + price
            sid_list.append(sid)
        bought_seats_num = PlaySeat.buy(orderno, order.pid, sid_list)
        if not bought_seats_num:
            return Code.seat_buy_failed, {}
        order.paid_time = datetime.now()
        order.status = OrderStatus.paid.value
        order.gen_ticket_flag()
        order.save()
        return {
            'bought_seats_num': bought_seats_num,
            'ticket_flag': order.ticket_flag,
        }