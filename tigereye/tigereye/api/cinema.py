from flask import jsonify,request
from flask_classy import FlaskView
from tigereye.models.cinema import Cinema
from tigereye.models.hall import Hall
from tigereye.api import ApiView
from tigereye.helper.code import Code


class CinemaView(ApiView):

    def all(self):
        return Cinema.query.all()

    def halls(self):
        cid = request.args['cid']
        cinema = Cinema.get(cid)
        if not cinema:
            return Code.cinema_does_not_exist, request.args
        cinema.halls = Hall.query.filter_by(cid=cid).all()
        return cinema