from flask import Flask
from database import init_db
from routes.items import items_bp
from routes.logs import logs_bp
from routes.home import home_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(items_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(home_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)