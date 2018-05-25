import functools
from flask import request, Response, jsonify, make_response
from flask_classy import FlaskView

from tigereye.helper.code import Code


class ApiView(FlaskView):
    @classmethod
    def make_proxy_method(cls, name):
        """Creates a proxy function that can be used by Flasks routing. The
        proxy instantiates the FlaskView subclass and calls the appropriate
        method.

        :param name: the name of the method to create a proxy for
        """

        i = cls()
        view = getattr(i, name)

        if cls.decorators:
            for decorator in cls.decorators:
                view = decorator(view)

        @functools.wraps(view)
        def proxy(**forgettable_view_args):
            # Always use the global request object's view_args, because they
            # can be modified by intervening function before an endpoint or
            # wrapper gets called. This matches Flask's behavior.
            del forgettable_view_args

            if hasattr(i, "before_request"):
                response = i.before_request(name, **request.view_args)
                if response is not None:
                    return response

            before_view_name = "before_" + name
            if hasattr(i, before_view_name):
                before_view = getattr(i, before_view_name)
                response = before_view(**request.view_args)
                if response is not None:
                    return response

            response = view(**request.view_args)

            # 是否是Response对象，如果不是，则进入我们自己的处理流程
            if not isinstance(response, Response):
                # 读取response的类型
                response_type = type(response)
                # 如果是元组，并且长度大于1，则视为是接口错误提示
                if response_type is tuple and len(response) > 1:
                    # 分别提取错误码，和数据
                    rc, _data = response
                    # 返回错误码和数据提示的json响应
                    response = jsonify(
                        rc=rc.value,
                        msg=rc.name,
                        data=_data
                    )
                else:
                    # 正常返回数据，此时response就量个正常的列表或者字典
                    response = jsonify(
                        rc=Code.succ.value,
                        msg=Code.succ.name,
                        data=response,
                    )
                response = make_response(response)

            after_view_name = "after_" + name
            if hasattr(i, after_view_name):
                after_view = getattr(i, after_view_name)
                response = after_view(response)

            if hasattr(i, "after_request"):
                response = i.after_request(name, response)

            return response

        return proxy