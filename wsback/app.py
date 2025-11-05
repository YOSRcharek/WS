from flask import Flask,request, jsonify
from routes.dechets.dechets import dechets_bp
import smtplib
from email.message import EmailMessage


from routes.typeDechets.typeDechets import typedechets_bp
from routes.aidechet import iadechet_bp
from routes.events.event import evenement_bp
from routes.events.collect import collecte_bp
from routes.events.formation import formation_bp
from routes.compagne.campagne import campagne_bp
from routes.compagne.reseaux import reseaux_bp
from routes.compagne.affiche import affiche_bp
from routes.ia_sparql import ia_bp   
from flask_cors import CORS

# Import des équipements depuis le dossier equipements
from routes.equipements.equipement import equipement_bp
from routes.equipements.broyeur import broyeur_bp
from routes.equipements.camion_benne import camion_benne_bp
from routes.equipements.compacteur import compacteur_bp
from routes.equipements.conteneur import conteneur_bp

# Import des services de transport depuis le dossier services_transport
from routes.services_transport.service_transport import service_transport_bp
from routes.services_transport.camion_dechets import camion_dechets_bp
from routes.services_transport.transport_dechets_dangereux import transport_dechets_dangereux_bp

app = Flask(__name__)
CORS(app, origins=["http://localhost:3006"], supports_credentials=True)
# Enregistrement des Blueprints
app.register_blueprint(evenement_bp)
app.register_blueprint(collecte_bp)
app.register_blueprint(formation_bp)
app.register_blueprint(campagne_bp)
app.register_blueprint(affiche_bp)
app.register_blueprint(reseaux_bp)
app.register_blueprint(equipement_bp, url_prefix='/api')
app.register_blueprint(service_transport_bp, url_prefix='/api')

# Equipment subclasses
app.register_blueprint(broyeur_bp, url_prefix='/api')
app.register_blueprint(camion_benne_bp, url_prefix='/api')
app.register_blueprint(compacteur_bp, url_prefix='/api')
app.register_blueprint(conteneur_bp, url_prefix='/api')

# Transport service subclasses
app.register_blueprint(camion_dechets_bp, url_prefix='/api')
app.register_blueprint(transport_dechets_dangereux_bp, url_prefix='/api')

# Enregistrement des Blueprints
app.register_blueprint(dechets_bp)
app.register_blueprint(typedechets_bp)
app.register_blueprint(iadechet_bp)

app.register_blueprint(ia_bp) 




if __name__ == "__main__":
    app.run(debug=True)

