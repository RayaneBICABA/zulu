from math import asin, cos, radians, sin, sqrt
from urllib.parse import urlencode
from ..models.commerce import Commerce


DEFAULT_RAYON_KM = 25
DEFAULT_LIMIT = 10
EARTH_RADIUS_KM = 6371.0


class InterfaceMapService:

    def get_commerces_proches(self, data):
        client_latitude = data["latitude"]
        client_longitude = data["longitude"]
        rayon_km = data.get("rayon_km", DEFAULT_RAYON_KM)
        limit = data.get("limit", DEFAULT_LIMIT)
        categorie_id = data.get("categorie_id")

        query = Commerce.query.filter(
            Commerce.is_active.is_(True),
            Commerce.latitude.isnot(None),
            Commerce.longitude.isnot(None),
        )

        if categorie_id:
            query = query.filter_by(categorie_id=categorie_id)

        commerces = []
        for commerce in query.all():
            distance_km = _distance_km(
                client_latitude,
                client_longitude,
                float(commerce.latitude),
                float(commerce.longitude),
            )

            if distance_km <= rayon_km:
                item = commerce.to_dict()
                item["distance_km"] = round(distance_km, 2)
                item["itineraire_url"] = _build_itineraire_url(
                    client_latitude,
                    client_longitude,
                    float(commerce.latitude),
                    float(commerce.longitude),
                )
                commerces.append(item)

        commerces = sorted(commerces, key=lambda item: item["distance_km"])[:limit]

        return {
            "position_client": {
                "latitude": client_latitude,
                "longitude": client_longitude,
            },
            "rayon_km": rayon_km,
            "count": len(commerces),
            "commerce_plus_proche": commerces[0] if commerces else None,
            "commerces": commerces,
        }


def _distance_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return EARTH_RADIUS_KM * c


def _build_itineraire_url(origin_lat, origin_lon, destination_lat, destination_lon):
    params = urlencode({
        "api": "1",
        "origin": f"{origin_lat},{origin_lon}",
        "destination": f"{destination_lat},{destination_lon}",
        "travelmode": "driving",
    })
    return f"https://www.google.com/maps/dir/?{params}"
