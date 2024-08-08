from flask import current_app
from flask.cli import with_appcontext
import click
from seeder import seed_all

@click.command(name='seed')
@with_appcontext
def seed():
    """Seed the database"""
    seed_all()
    current_app.logger.info("Database seeded successfully")
