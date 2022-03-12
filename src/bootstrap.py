"""Bootstrap the application"""
from blueprints import healthcheck, backend, loader
from constants import DATABASE_CONFIG
from extensions import db, migrate


def make_connection_uri(**options):
    """Postgres connection string."""
    return "postgresql+psycopg2://{username}:{password}@{host}:{port}".format(
        **options
    )


def configure_db(app, database_name):
    """Create default and named databases."""
    connection = make_connection_uri(**DATABASE_CONFIG[database_name])
    app.config["SQLALCHEMY_DATABASE_URI"] = connection
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = True
    return app


def create_app(instance, database_name):
    """Bootstrap the app. Takes an instance of the Flask obj/app."""
    instance = configure_db(instance, database_name)
    register_extensions(instance)
    register_blueprints(instance)
    return instance


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    return app


def register_blueprints(app):
    """Register blueprints with the app."""
    app.register_blueprint(healthcheck.bp)
    app.register_blueprint(backend.bp)
    app.register_blueprint(loader.bp)
