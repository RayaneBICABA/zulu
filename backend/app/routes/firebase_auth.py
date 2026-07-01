from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from ..extensions import db
from ..models.user import User
from ..models.role import Role
from ..services.firebase_auth import verify_token

firebase_auth_bp = Blueprint('firebase_auth', __name__)


@firebase_auth_bp.route('/auth/firebase-login', methods=['POST'])
def firebase_login():
    """
    Authentification via token Firebase ID.
    Crée l'utilisateur s'il n'existe pas (upsert).
    Appelé par le frontend après signInWithEmailAndPassword, signInWithRedirect,
    ou signInWithCredential (deep link mobile).
    """
    data = request.get_json() or {}
    token = data.get('token')

    if not token:
        return jsonify({"error": "Token requis."}), 400

    # 1. Vérifier le token Firebase
    decoded = verify_token(token)
    if not decoded:
        return jsonify({"error": "Token Firebase invalide ou expiré."}), 401

    firebase_uid = decoded.get('uid')
    email = decoded.get('email')
    name = decoded.get('name') or ''

    # 2. Chercher l'utilisateur par firebase_uid
    user = User.query.filter_by(firebase_uid=firebase_uid).first()

    if not user:
        if not email:
            return jsonify({"error": "Email non disponible dans le token."}), 400

        # 3. Pas trouvé par firebase_uid → chercher par email (compte existant)
        user = User.query.filter_by(email=email).first()

        if user:
            # Lier le compte existant à Firebase
            user.firebase_uid = firebase_uid
        else:
            # 4. Créer un nouvel utilisateur
            name_parts = name.split(' ', 1)
            user = User(
                email=email,
                firebase_uid=firebase_uid,
                first_name=name_parts[0] if name_parts else '',
                last_name=name_parts[1] if len(name_parts) > 1 else '',
                is_verified=True,  # Google vérifie l'email
            )
            # Assigner le rôle client par défaut
            client_role = Role.query.filter_by(name='client').first()
            if client_role and client_role not in user.roles:
                user.roles.append(client_role)

        db.session.add(user)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erreur base de données: {str(e)}"}), 500

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "email": user.email,
            "is_verified": user.is_verified,
            "roles": [r.name for r in user.roles],
        },
        expires_delta=timedelta(minutes=15),
    )
    refresh_token = create_refresh_token(
        identity=str(user.id),
        expires_delta=timedelta(days=7),
    )

    return jsonify({
        "user": user.to_dict(),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }), 200