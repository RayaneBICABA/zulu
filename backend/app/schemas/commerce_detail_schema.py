from marshmallow import Schema, fields, validate


class CommerceDetailPositionSchema(Schema):
    latitude = fields.Float(validate=validate.Range(min=-90, max=90), allow_none=True)
    longitude = fields.Float(validate=validate.Range(min=-180, max=180), allow_none=True)


class CommerceAvisCreateSchema(Schema):
    note = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    commentaire = fields.Str(validate=validate.Length(max=1000), allow_none=True)


class CommerceAvisSchema(Schema):
    id = fields.Int(dump_only=True)
    commerce_id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    auteur = fields.Str(dump_only=True)
    note = fields.Int(dump_only=True)
    commentaire = fields.Str(dump_only=True)
    date_relative = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


class CommerceDetailSchema(Schema):
    id = fields.Int(dump_only=True)
    nom_commercial = fields.Str(dump_only=True)
    categorie = fields.Dict(dump_only=True)
    quartier = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    couverture = fields.Dict(dump_only=True)
    produit_images = fields.List(fields.Dict(), dump_only=True)
    note_moyenne = fields.Float(dump_only=True)
    nombre_avis = fields.Int(dump_only=True)
    contacts = fields.Dict(dump_only=True)
    localisation = fields.Dict(dump_only=True)
    horaires = fields.Dict(dump_only=True)
    derniers_avis = fields.List(fields.Nested(CommerceAvisSchema), dump_only=True)
    peut_laisser_avis = fields.Bool(dump_only=True)
