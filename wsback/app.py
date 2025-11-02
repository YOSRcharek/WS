from flask import Flask
from routes.dechets import dechets_bp
from routes.events.event import evenement_bp
from routes.events.collect import collecte_bp
from routes.events.formation import formation_bp
from routes.compagne.campagne import campagne_bp

app = Flask(__name__)

app.register_blueprint(evenement_bp)
app.register_blueprint(collecte_bp)
app.register_blueprint(formation_bp)
app.register_blueprint(campagne_bp)

# Enregistrement des Blueprints
app.register_blueprint(dechets_bp)


if __name__ == "__main__":
    app.run(debug=True)
