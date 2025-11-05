import os
from config import RDF_FILE

print(f"Chemin du fichier RDF: {RDF_FILE}")
print(f"Le fichier existe: {os.path.exists(RDF_FILE)}")
print(f"Chemin absolu: {os.path.abspath(RDF_FILE)}")
