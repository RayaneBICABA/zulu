from marshmallow import Schema, fields, validate


class ClientPositionSchema(Schema):
    latitude = fields.Float(required=True, validate=validate.Range(min=-90, max=90))
    longitude = fields.Float(required=True, validate=validate.Range(min=-180, max=180))
    rayon_km = fields.Float(
        load_default=25,
        validate=validate.Range(min=0.1, max=500),
    )
    limit = fields.Int(
        load_default=10,
        validate=validate.Range(min=1, max=50),
    )
    categorie_id = fields.Int(load_default=None, allow_none=True)
