import json
import logging
from flask import current_app

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Tu es un analyste de sentiment pour une plateforme d'artisans nommee Zulu.
Tu recois une liste de commentaires laisses par des clients sur un commerce.
Analyse le ton global (positif, negatif, mitige) et attribue une note de 1.00 a 5.00.

Barème:
- 1.00-1.50 = Tres mauvais (plaintes graves, arnaque)
- 1.50-2.50 = Mauvais (problemes recurrents, decontentement fort)
- 2.50-3.50 = Moyen (experience mitigee, bons et mauvais points egaux)
- 3.50-4.25 = Bon (satisfait, petits defauts mineurs)
- 4.25-5.00 = Excellent (eloges unanimes, tres satisfaits)

Reponds UNIQUEMENT avec un JSON valide (pas de texte avant ou apres):
{"note": X.XX, "justification": "resume en une phrase"}

Exemples de reponse:
{"note": 4.50, "justification": "Les clients sont tres satisfaits du travail et de l'acceuil."}
{"note": 2.00, "justification": "Plusieurs plaintes sur la qualite et les delais."}
{"note": 3.25, "justification": "Avis mitiges, du positif comme du negatif."}
"""


def _build_user_prompt(commentaires):
    lines = []
    for c in commentaires:
        lines.append(f"- \"{c['contenu']}\"")
    return "\n".join(lines)


def _parse_llm_response(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    data = json.loads(text)
    note = float(data["note"])
    note = max(1.0, min(5.0, round(note, 2)))
    justification = str(data.get("justification", ""))
    return note, justification


def _call_gemini(user_prompt):
    import google.generativeai as genai
    api_key = current_app.config.get("GEMINI_API_KEY", "")
    if not api_key:
        raise ValueError("GEMINI_API_KEY non configuree.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT,
    )
    response = model.generate_content(user_prompt)
    return response.text


def analyze_commentaires(commentaires):
    if not commentaires:
        return None, "Aucun commentaire a analyser."

    user_prompt = _build_user_prompt(commentaires)

    try:
        raw = _call_gemini(user_prompt)
        return _parse_llm_response(raw)
    except Exception as e:
        logger.error(f"[AI] Gemini a echoue: {e}")
        return None, None


def compute_etoiles(rating):
    if rating is None or rating <= 0:
        return {"pleines": 0, "demies": 0, "vides": 5}
    pleines = int(rating)
    decimal = rating - pleines
    if decimal >= 0.75:
        pleines += 1
        demies = 0
    elif decimal >= 0.25:
        demies = 1
    else:
        demies = 0
    vides = 5 - pleines - demies
    return {"pleines": pleines, "demies": demies, "vides": vides}


POSITIVE_WORDS = {
    "super", "excellent", "genial", "parfait", "merci", "bravo", "tres bien",
    "satisfait", "recommande", "top", "qualite", "professionnel", "rapide",
    "accueillant", "sympa", "agreable", "propre", "bon", "bien", "nickel",
    "impeccable", "exceptionnel", "incroyable", "magnifique", "parfait",
}

NEGATIVE_WORDS = {
    "mauvais", "deplorable", "horrible", "null", "deçu", "decevant",
    "lent", "cher", "impoli", "sale", "casse", "probleme", "arnaque",
    "insatisfait", "dommage", "pas bien", "pas bon", "mediocre",
    "a eviter", "fuyez", "derniere fois", "jamais",
}


def _keyword_analysis(commentaires):
    if not commentaires:
        return None, "Aucun commentaire."

    total_score = 0.0
    for c in commentaires:
        contenu = c["contenu"].lower()
        pos = sum(1 for w in POSITIVE_WORDS if w in contenu)
        neg = sum(1 for w in NEGATIVE_WORDS if w in contenu)
        total = pos + neg
        if total == 0:
            score = 3.0
        else:
            score = 3.0 + 2.0 * (pos - neg) / total
        score = max(1.0, min(5.0, score))
        total_score += score

    avg = round(total_score / len(commentaires), 2)
    return avg, f"Analyse lexicale: {avg}/5"


def analyze_and_update_rating(commerce_id):
    from app.models.commerce import CommerceStats, Commerce
    from app.models.commentaire import Commentaire
    from app.extensions import db

    commerce = Commerce.query.get(commerce_id)
    if not commerce:
        return

    commentaires = (
        Commentaire.query
        .filter_by(commerce_id=commerce_id, is_visible=True)
        .all()
    )

    comment_data = [{"contenu": c.contenu} for c in commentaires]

    note, justification = None, None

    api_key = current_app.config.get("GEMINI_API_KEY", "")
    if api_key:
        note, justification = analyze_commentaires(comment_data)

    if note is None:
        note, justification = _keyword_analysis(comment_data)

    stats = CommerceStats.query.filter_by(commerce_id=commerce_id).first()
    if not stats:
        stats = CommerceStats(commerce_id=commerce_id)
        db.session.add(stats)

    if note is not None:
        stats.average_rating = note
        stats.rating_count = len(commentaires)
    # Keep previous rating if both AI and fallback fail

    db.session.commit()
    logger.info(
        f"[AI] Commerce {commerce_id}: note={note}, "
        f"count={len(commentaires)}, justification={justification}"
    )
