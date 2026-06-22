from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.Str(
        required=True,
        validate=[
            validate.Length(min=8, max=128),
        ],
    )
    first_name = fields.Str(validate=validate.Length(max=150))
    last_name = fields.Str(validate=validate.Length(max=150))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email()
    first_name = fields.Str()
    last_name = fields.Str()
    is_verified = fields.Bool()
    is_active = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
