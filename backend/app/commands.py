import click
from flask.cli import with_appcontext
from .models.role import Role
from .extensions import db


@click.command("seed-roles")
@with_appcontext
def seed_roles():
    defaults = [
        ("client", "Client — cherche des services"),
        ("artisan", "Artisan — prestataire de service"),
        ("admin", "Administrateur du systeme"),
    ]
    created = 0
    for name, desc in defaults:
        if not Role.query.filter_by(name=name).first():
            role = Role(name=name, description=desc)
            db.session.add(role)
            created += 1
    db.session.commit()
    click.echo(f"{created} role(s) cree(s).")
