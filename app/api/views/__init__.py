from .authorization import requires_authorization

import marshmallow

from flask import views, request, jsonify


__all__ = [

]


class SerializerBaseSchema(marshmallow.Schema):

    SERIALIZE_TO = dict

    @marshmallow.post_load
    def make_instance(self, data, **_kwargs):
        return self.SERIALIZE_TO(**data)


class __MetaView(views.MethodViewType):

    NAME = ROUTE = str()
    decorators = []
    REQUIRES_AUTHORIZATION = False

    def __init__(cls, *args, **kwargs):
        if not cls.ROUTE:
            raise NotImplementedError("View class should define a valid route as endpoint.")
        if cls.REQUIRES_AUTHORIZATION:
            cls.decorators.append(requires_authorization)
        super().__init__(*args, **kwargs)
        cls.NAME = cls.__name__.lower() if not cls.NAME else cls.NAME


class BaseView(views.MethodView, metaclass=__MetaView):

    REQUEST_SERIALIZER = None
    RESPONSE_SERIALIZER = None

    @classmethod
    def as_view(cls, *args, **kwargs):
        return super().as_view(cls.NAME, *args, **kwargs)

    def dispatch_request(self, *args, **kwargs):
        json = request.get_json()
        try:
            instance = self.REQUEST_SERIALIZER().load(**json)
        except marshmallow.ValidationError as exc:
            return jsonify(errors=exc.messages), 400
        except TypeError:
            ret = super().dispatch_request(*args, **kwargs)
        else:
            ret = super().dispatch_request(*args, **kwargs, instance=instance)

        try:
            return self.RESPONSE_SERIALIZER().dump(ret)
        except TypeError:
            return ret
