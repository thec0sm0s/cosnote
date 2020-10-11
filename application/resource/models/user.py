from ..fields import UsernameField
from ..fields import PasswordField

from .notes import Note
from . import BaseDocument

from mongoengine import EmbeddedDocument, ListField, ReferenceField
from mongoengine import EmbeddedDocumentField, BooleanField, EmailField, CASCADE


class UserPreferences(EmbeddedDocument):

    developer = BooleanField(default=False)


class User(BaseDocument):

    username = UsernameField(minimum_length=5, max_length=20, primary_key=True)
    email = EmailField(unique=True, sparse=True)
    password = PasswordField()
    preferences = EmbeddedDocumentField(UserPreferences, default=UserPreferences)

    notes = ListField(ReferenceField(Note, reverse_delete_rule=CASCADE))

    def authorize(self, password):
        return PasswordField.verify(self.password, password)