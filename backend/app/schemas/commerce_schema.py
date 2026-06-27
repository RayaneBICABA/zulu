from marshmallow import Schema, fields, validate


JOURS_VALIDES = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


class HoraireInputSchema(Schema):
    jour = fields.Str(required=True, validate=validate.OneOf(JOURS_VALIDES))
    heure_ouverture = fields.Str(allow_none=True, validate=validate.Regexp(r"^\d{2}:\d{2}$", error="Format attendu: HH:MM"))
    heure_fermeture = fields.Str(allow_none=True, validate=validate.Regexp(r"^\d{2}:\d{2}$", error="Format attendu: HH:MM"))
    est_ferme = fields.Bool()
    est_24h = fields.Bool()


class CommerceStep1Schema(Schema):
    nom_commercial = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    whatsapp_numero = fields.Str(validate=validate.Length(max=20))
    contact_telephonique = fields.Str(validate=validate.Length(max=20))
    categorie_id = fields.Int(required=True)
    description = fields.Str(validate=validate.Length(max=2000))
    is_vendeur_produits = fields.Bool()


class CommerceStep2Schema(Schema):
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    adresse_complete = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    horaires = fields.List(
        fields.Nested(HoraireInputSchema),
        required=True,
        validate=validate.Length(min=7, max=7),
    )


class CommercePhotoSchema(Schema):
    id = fields.Int(dump_only=True)
    commerce_id = fields.Int(dump_only=True)
    url = fields.Str(dump_only=True)
    alt_text = fields.Str(validate=validate.Length(max=255))
    ordre = fields.Int(dump_only=True)
    is_principale = fields.Bool(dump_only=True)


class HoraireOuvertureSchema(Schema):
    id = fields.Int(dump_only=True)
    commerce_id = fields.Int(dump_only=True)
    jour = fields.Str(dump_only=True)
    heure_ouverture = fields.Str(dump_only=True)
    heure_fermeture = fields.Str(dump_only=True)
    est_ferme = fields.Bool(dump_only=True)
    est_24h = fields.Bool(dump_only=True)


class CommerceStatsSchema(Schema):
    id = fields.Int(dump_only=True)
    commerce_id = fields.Int(dump_only=True)
    nb_vues_profile = fields.Int(dump_only=True)
    nb_favoris = fields.Int(dump_only=True)
    last_vue_at = fields.DateTime(dump_only=True)


class FavoriSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    commerce_id = fields.Int(dump_only=True)


class FavoriCreateSchema(Schema):
    commerce_id = fields.Int(required=True)


class VueProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    commerce_id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    ip_address = fields.Str(dump_only=True)
    user_agent = fields.Str(dump_only=True)
    viewed_at = fields.DateTime(dump_only=True)


class ProduitImageSchema(Schema):
    id = fields.Int(dump_only=True)
    commerce_id = fields.Int(dump_only=True)
    url = fields.Str(dump_only=True)
    ordre = fields.Int(dump_only=True)


class ProduitImageCreateSchema(Schema):
    url = fields.Str(required=True, validate=validate.Length(max=500))
    ordre = fields.Int(required=True)


class CommerceSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    nom_commercial = fields.Str(dump_only=True)
    whatsapp_numero = fields.Str(dump_only=True)
    contact_telephonique = fields.Str(dump_only=True)
    categorie_id = fields.Int(dump_only=True)
    description = fields.Str(dump_only=True)
    latitude = fields.Float(dump_only=True)
    longitude = fields.Float(dump_only=True)
    adresse_complete = fields.Str(dump_only=True)
    is_vendeur_produits = fields.Bool(dump_only=True)
    is_verified = fields.Bool(dump_only=True)
    is_active = fields.Bool(dump_only=True)
    step = fields.Int(dump_only=True)
    stats = fields.Nested(CommerceStatsSchema, dump_only=True)
    photos = fields.List(fields.Nested(CommercePhotoSchema), dump_only=True)
    horaires = fields.List(fields.Nested(HoraireOuvertureSchema), dump_only=True)
    produit_images = fields.List(fields.Nested(ProduitImageSchema), dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CommerceSummarySchema(Schema):
    id = fields.Int(dump_only=True)
    nom_commercial = fields.Str(dump_only=True)
    is_verified = fields.Bool(dump_only=True)
    is_active = fields.Bool(dump_only=True)


class ArtisanProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    email = fields.Str(dump_only=True)
    is_verified = fields.Bool(dump_only=True)


class CommerceProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    nom_commercial = fields.Str(dump_only=True)
    whatsapp_numero = fields.Str(dump_only=True)
    contact_telephonique = fields.Str(dump_only=True)
    is_active = fields.Bool(dump_only=True)
