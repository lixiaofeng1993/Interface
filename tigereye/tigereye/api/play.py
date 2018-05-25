from flask import request

from tigereye.extensions.validator import Validator
from tigereye.models.play import Play
from tigereye.api import ApiView
from tigereye.models.seat import PlaySeat, SeatType


class PlayView(ApiView):

    def all(self):
        return Play.query.all()

    @Validator(pid=int)
    def seats(self):
        pid = request.params['pid']
        return PlaySeat.query.filter(
            PlaySeat.pid == pid,
            PlaySeat.seat_type != SeatType.road.value
        ).all()
