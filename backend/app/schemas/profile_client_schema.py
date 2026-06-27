from marshmallow import Schema, fields


class ProfileClientSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(dump_only=True)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    is_verified = fields.Bool(dump_only=True)
    is_active = fields.Bool(dump_only=True)
    roles = fields.List(fields.Str(), dump_only=True)
    can_become_artisan = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)