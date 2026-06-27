from marshmallow import Schema, fields, validate


class CommentaireSchema(Schema):
    id = fields.Int(dump_only=True)
    commerce_id = fields.Int(dump_only=True)
    auteur_id = fields.Int(dump_only=True)
    contenu = fields.Str(dump_only=True)
    is_visible = fields.Bool(dump_only=True)
    is_moderated = fields.Bool(dump_only=True)
    moderated_at = fields.DateTime(dump_only=True)
    moderated_by = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CommentaireCreateSchema(Schema):
    contenu = fields.Str(required=True, validate=validate.Length(min=1, max=2000))


class CommentaireModerateSchema(Schema):
    is_visible = fields.Bool(required=True)


class CommentaireAuteurSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)


class CommentaireResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    contenu = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    auteur = fields.Nested(CommentaireAuteurSchema, dump_only=True)
