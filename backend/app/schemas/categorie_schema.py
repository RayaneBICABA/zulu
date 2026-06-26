from marshmallow import Schema, fields, validate


class CategorieSchema(Schema):
    id = fields.Int(dump_only=True)
    nom = fields.Str(required=True, validate=validate.Length(max=150))
    description = fields.Str(validate=validate.Length(max=500))
    icone = fields.Str(validate=validate.Length(max=255))
    is_active = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CategorieSummarySchema(Schema):
    id = fields.Int(dump_only=True)
    nom = fields.Str(dump_only=True)
    icone = fields.Str(dump_only=True)
