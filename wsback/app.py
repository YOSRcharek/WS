from flask import Flask
from routes.dechets import dechets_bp
from routes.event import evenement_bp
from routes.campagne import campagne_bp

app = Flask(__name__)

app.register_blueprint(evenement_bp)
app.register_blueprint(campagne_bp)

# Enregistrement des Blueprints
app.register_blueprint(dechets_bp)


if __name__ == "__main__":
    app.run(debug=True)
