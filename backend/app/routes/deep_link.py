from flask import Blueprint, jsonify, make_response, request

deep_link_bp = Blueprint("deep_link", __name__)

SHA256_FINGERPRINT = "E7:C0:55:BA:C7:F9:E3:87:BC:09:FB:1B:77:4C:FE:EF:38:8E:4C:4E:18:F8:0C:F2:98:18:E5:99:E4:16:DD:6A"


@deep_link_bp.route("/.well-known/assetlinks.json")
def assetlinks():
    return jsonify([
        {
            "relation": ["delegate_permission/common.handle_all_urls"],
            "target": {
                "namespace": "android_app",
                "package_name": "com.zawani.app",
                "sha256_cert_fingerprints": [SHA256_FINGERPRINT],
            },
        }
    ])


@deep_link_bp.route("/reinitialiser-mot-de-passe")
def reset_password_fallback():
    token = request.args.get("token", "")
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Reinitialisation du mot de passe - ZAWANI</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
display:flex;justify-content:center;align-items:center;min-height:100vh;
margin:0;background:#f5f5f5;color:#333;}}
.card{{background:#fff;border-radius:16px;padding:32px;max-width:420px;
width:90%;box-shadow:0 2px 8px rgba(0,0,0,0.1);text-align:center;}}
h1{{font-size:1.5rem;margin-bottom:8px;color:#1a1a2e;}}
p{{color:#666;margin-bottom:24px;font-size:0.9rem;line-height:1.5;}}
.btn{{background:#6366f1;color:#fff;border:none;padding:14px 28px;
border-radius:8px;font-size:1rem;cursor:pointer;text-decoration:none;
display:inline-block;margin-top:12px;}}
.btn:hover{{background:#4f46e5;}}
.footer{{margin-top:32px;font-size:0.8rem;color:#999;}}
</style>
<script>
try {{
  window.location.href = 'zawani://auth/reinitialiser-mot-de-passe?token={token}';
}} catch(e) {{}}
setTimeout(function() {{
  document.getElementById('fallback').style.display = 'block';
}}, 3000);
</script>
</head>
<body>
<div class="card">
<div id="loading">
<h1>Redirection vers l'application...</h1>
<p>Si rien ne se passe, cliquez sur le bouton ci-dessous.</p>
</div>
<div id="fallback" style="display:none;">
<h1>Reinitialisation du mot de passe</h1>
<p>Utilisez l'application ZAWANI pour reinitialiser votre mot de passe en toute securite.</p>
<a href="zawani://auth/reinitialiser-mot-de-passe?token={token}" class="btn">
Ouvrir dans l'application
</a>
<p style="margin-top:16px;font-size:0.8rem;word-break:break-all;background:#f0f0f0;padding:12px;border-radius:8px;text-align:left;">
<strong>Token :</strong><br>{token}
</p>
</div>
<div class="footer">&copy; ZAWANI</div>
</div>
</body>
</html>"""
    resp = make_response(html)
    resp.headers["Content-Type"] = "text/html"
    return resp
