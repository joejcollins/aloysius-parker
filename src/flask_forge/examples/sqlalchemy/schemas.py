from marshmallow import Schema, fields


class UserSchema(Schema):
    name = fields.String(required=True, description="The name of the user")
    email = fields.String(required=True, description="The email of the user")
