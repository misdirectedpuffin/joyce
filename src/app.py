"""Entrypoint to the application."""
import os

from flask import Flask

from bootstrap import create_app
from models.model import db

instance = Flask(__name__)

app = create_app(instance, os.getenv("FLASK_ENV", "development"))


@app.before_first_request
def create_database():
    """Create the database schema"""
    app.logger.info("Creating database")
    try:
        db.create_all()
    except Exception:  #  pylint: disable=broad-except
        app.logger.exception("Failed to create db tables.")
        db.session.rollback()
    else:
        app.logger.info("Successfully created db tables.")
        db.session.commit()


def main(port: int = 3000):
    """Run in the debug configuration enabling vscode to attach."""
    if os.getenv("DEBUGGER"):
        import multiprocessing
        if multiprocessing.current_process().pid > 1:
            import debugpy

            debugpy.listen(("0.0.0.0", port))
            print("⏳ VS Code debugger can now be attached, press F5 in VS Code ⏳", flush=True)
            debugpy.wait_for_client()
            print("🎉 VS Code debugger attached, enjoy debugging 🎉", flush=True)
        print("pid is not 1")
    else:
        app.run(host="0.0.0.0", port=5000, threaded=True)



if __name__ == "__main__":
    main()
