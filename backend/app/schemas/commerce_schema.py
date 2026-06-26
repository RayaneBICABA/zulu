from marshmallow import Schema, fields, validate


class CommercePhotoSchema(Schema):
    id = fields.Int(dump_only=True)
    commerce_id = fields.Int(dump_only=True)
    url = fields.Str(required=True, validate=validate.Length(max=500))
    alt_text = fields.Str(validate=validate.Length(max=255))
    ordre = fields.Int()
    is_principale = fields.Bool()


class HoraireOuvertureSchema(Schema):
    id = fields.Int(dump_only=True)
    commerce_id = fields.Int(dump_only=True)
    jour = fields.Str(required=True)
    heure_ouverture = fields.Str()
    heure_fermeture = fields.Str()
    est_ferme = fields.Bool()
    est_24h = fields.Bool()


class CommerceSchema(Schema):
    id = fields.Int(dump_only=True)
    nom_commercial = fields.Str(required=True, validate=validate.Length(max=200))
    whatsapp_numero = fields.Str(validate=validate.Length(max=20))
    contact_telephonique = fields.Str(validate=validate.Length(max=20))
    categorie_id = fields.Int(required=True)
    description = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()
    adresse_complete = fields.Str(validate=validate.Length(max=500))
    is_verified = fields.Bool(dump_only=True)
    is_active = fields.Bool()
    photos = fields.List(fields.Nested(CommercePhotoSchema), dump_only=True)
    horaires = fields.List(fields.Nested(HoraireOuvertureSchema), dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CommerceSummarySchema(Schema):
    id = fields.Int(dump_only=True)
    nom_commercial = fields.Str(dump_only=True)
    is_verified = fields.Bool(dump_only=True)
    is_active = fields.Bool(dump_only=True)
