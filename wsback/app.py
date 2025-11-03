from flask import Flask
from routes.dechets.dechets import dechets_bp
from routes.events.event import evenement_bp
from routes.events.collect import collecte_bp
from routes.events.formation import formation_bp
from routes.compagne.campagne import campagne_bp
from routes.compagne.reseaux import reseaux_bp
from routes.compagne.affiche import affiche_bp
from routes.ia_sparql import ia_bp   
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3006"], supports_credentials=True)
# Enregistrement des Blueprints
app.register_blueprint(evenement_bp)
app.register_blueprint(collecte_bp)
app.register_blueprint(formation_bp)
app.register_blueprint(campagne_bp)
app.register_blueprint(affiche_bp)
app.register_blueprint(reseaux_bp)
app.register_blueprint(dechets_bp)
app.register_blueprint(ia_bp) 

if __name__ == "__main__":
    app.run(debug=True)

