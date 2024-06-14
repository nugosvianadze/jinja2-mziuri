from app import create_app
from app.blog.models import Role
from enums import RoleEnum
from app.extensions import db

import click

app = create_app()


@app.cli.command('create_roles')
def create_roles():
    roles = [Role(title=role.value) for role in RoleEnum]
    db.session.add_all(roles)
    db.session.commit()
    click.echo('roles successfully created')
