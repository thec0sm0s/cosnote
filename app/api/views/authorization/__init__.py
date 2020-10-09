from flask import jsonify, session
from app.resource import models

from .. import BaseView
from .serializers import RegisterSchema
from ..user.serializer import UserSchema


class Register(BaseView):

    ROUTE = "/register/"

    REQUEST_SERIALIZER = RegisterSchema
    RESPONSE_SERIALIZER = UserSchema

    @staticmethod
    def post(*, instance):
        user = models.User.objects(username=instance["username"]).first()
        if user:
            return jsonify(errors=dict(username=["Specified username is already registered."])), 400
        user = models.User(**instance)
        user.save()
        session["username"] = user.username
        return user


class Authorize(BaseView):

    ROUTE = "/authorize/"
