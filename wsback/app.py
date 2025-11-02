from flask import Flask
from routes.dechets import dechets_bp

app = Flask(__name__)

# Enregistrement des Blueprints
app.register_blueprint(dechets_bp)


if __name__ == "__main__":
    app.run(debug=True)
