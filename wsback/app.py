from flask import Flask
from routes.dechets import dechets_bp
from routes.typeDechets import typedechets_bp
from routes.citoyen import citoyen_bp
from routes.aidechet import iadechet_bp

app = Flask(__name__)

# Enregistrement des Blueprints
app.register_blueprint(dechets_bp)
app.register_blueprint(typedechets_bp)
app.register_blueprint(citoyen_bp)
app.register_blueprint(iadechet_bp)


if __name__ == "__main__":
    app.run(debug=True)
