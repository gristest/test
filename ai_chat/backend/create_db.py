

from api import create_app

app = create_app()
with app.app_context():
    print("Database initialized successfully")

