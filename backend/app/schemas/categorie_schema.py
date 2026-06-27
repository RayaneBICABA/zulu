from marshmallow import Schema, fields, validate


class CategorieCreateSchema(Schema):
    nom = fields.Str(required=True, validate=validate.Length(min=1, max=150))


class CategorieSchema(Schema):
    id = fields.Int(dump_only=True)
    nom = fields.Str(dump_only=True)
    is_active = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CategorieSummarySchema(Schema):
    id = fields.Int(dump_only=True)
    nom = fields.Str(dump_only=True)
