from datetime import datetime
from flask import request
from flask_classy import route
from tigereye.api import ApiView
from tigereye.extensions.validator import Validator, multi_int
from tigereye.helper.code import Code
from tigereye.models.order import Order, OrderStatus
from tigereye.models.seat import PlaySeat


class OrderView(ApiView):

    @route('/ticket/refund/', methods=['POST'])
    @Validator(orderno=str, ticket_flag=str, sid=multi_int)
    def refund_ticket(self):
        """退票接口"""
        orderno = request.params['orderno']
        ticket_flag = request.params['ticket_flag']
        seats = request.params['sid']

        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {"orderno": orderno}
        if order.status == OrderStatus.printed.value:
            return Code.ticket_printed_already, {}
        if order.status != OrderStatus.paid.value:
            return Code.order_not_paid_yet, {}
        if not order.validate(ticket_flag):
            return Code.ticket_flag_error, {'ticket_flag': ticket_flag}
        refund_num = PlaySeat.refund(orderno, order.pid, seats)
        if not refund_num:
            return Code.ticket_refund_failed, {}
        order.status = OrderStatus.refund.value
        order.refund_time = datetime.now()
        order.save()
        return {'refund_num': refund_num}

    @route('/ticket/print/', methods=['POST'])
    @Validator(orderno=str, ticket_flag=str, sid=multi_int)
    def print_ticket(self):
        """取票接口"""
        orderno = request.params['orderno']
        ticket_flag = request.params['ticket_flag']
        seats = request.params['sid']

        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {"orderno": orderno}
        if order.status == OrderStatus.printed.value:
            return Code.ticket_printed_already, {}
        if order.status != OrderStatus.paid.value:
            return Code.order_not_paid_yet, {}
        if not order.validate(ticket_flag):
            return Code.ticket_flag_error, {'ticket_flag': ticket_flag}
        # 修改座位状态为已取票
        printed_num = PlaySeat.print_tickets(orderno, order.pid, seats)
        if not printed_num:
            return Code.ticket_print_failed, {}
        # 设置订单状态为已取票
        order.status = OrderStatus.printed.value
        # 设置取票时间
        order.printed_time = datetime.now()
        order.save()
        return {'printed_num': printed_num}