from tigereye.api import ApiView


class MiscView(ApiView):

    def check(self):
        return "I'm OK"

    def error(self):
        1 / 0