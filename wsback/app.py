from flask import Flask
from flask_cors import CORS
from routes.dechets.dechets import dechets_bp

from routes.typeDechets.typeDechets import typedechets_bp
from routes.aidechet import iadechet_bp
from routes.events.event import evenement_bp
from routes.events.collect import collecte_bp
from routes.events.formation import formation_bp
from routes.compagne.campagne import campagne_bp
from routes.compagne.reseaux import reseaux_bp
from routes.compagne.affiche import affiche_bp
from routes.ia_sparql import ia_bp   
from routes.centres.centres import centres_bp
from routes.points_collecte.points_collecte import points_collecte_bp
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
#citoyen and municipalite
from routes.municipalites.municipalite import municipalite_bp
from routes.citoyens.citoyens import citoyen_bp
from routes.citizen_matching_ai import citizen_matching_bp
from routes.citizen_requests import citizen_requests_bp

app = Flask(__name__)
CORS(app)
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
app.register_blueprint(municipalite_bp, url_prefix='/api')
app.register_blueprint(citoyen_bp)

# Enregistrement des Blueprints
app.register_blueprint(dechets_bp)
app.register_blueprint(centres_bp)
app.register_blueprint(points_collecte_bp)
app.register_blueprint(ia_bp)
app.register_blueprint(typedechets_bp)
app.register_blueprint(iadechet_bp)

app.register_blueprint(citizen_matching_bp)
app.register_blueprint(citizen_requests_bp) 

if __name__ == "__main__":
    app.run(debug=True)

