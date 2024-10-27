from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.hash import bcrypt

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

User_Pydantic = pydantic_model_creator(User, name='User', exclude=['password_hash'])
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)


class Note(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    body = fields.CharField(max_length=255)
    author = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE, related_name='notes')
    created_at = fields.DatetimeField(auto_now_add=True)

Note_Pydantic = pydantic_model_creator(Note, name='Note')
NoteIn_Pydantic = pydantic_model_creator(Note, name='NoteIn', exclude_readonly=True)
