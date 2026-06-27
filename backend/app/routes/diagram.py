from flask import Blueprint, Response
from ..services.diagram_service import generate_mermaid, get_html_diagram

diagram_bp = Blueprint("diagram", __name__)


@diagram_bp.route("/diagram", methods=["GET"])
def diagram_raw():
    """Retourne le diagramme en format Mermaid (texte brut)."""
    return Response(generate_mermaid(), mimetype="text/plain")


@diagram_bp.route("/diagram/view", methods=["GET"])
def diagram_view():
    """Page HTML interactive avec rendu Mermaid.js + telechargement PNG."""
    return Response(get_html_diagram(), mimetype="text/html")
