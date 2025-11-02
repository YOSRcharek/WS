from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper, POST
from rdflib import Literal
from rdflib.namespace import RDF, XSD
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, RDF_FILE

campagne_bp = Blueprint("campagne_bp", __name__)

@campagne_bp.route("/campagnes", methods=["POST"])
def add_campagne():
    data = request.json
    cid = data["campaignID"]
    uri = f"ex:{cid}"

    insert_query = PREFIX + f"""
    INSERT DATA {{
        {uri} a ex:Campagne ;
            ex:descriptioncampa "{data.get('descriptioncampa','')}"^^xsd:string ;
            ex:startDate "{data.get('startDate','')}"^^xsd:date ;
            ex:endDate "{data.get('endDate','')}"^^xsd:date ;
            ex:targetAudience "{data.get('targetAudience','')}"^^xsd:string ;
            ex:title "{data.get('title','')}"^^xsd:string .
            
        # Sous-classe Affiche
        ex:Affiche_{cid} a ex:Affiche ;
            ex:contenuimage "{data.get('contenuimage','')}"^^xsd:string ;
            ex:image "{data.get('image','')}"^^xsd:string ;
            ex:partOf {uri} .

        # Sous-classe RéseauxSociaux
        ex:Reseau_{cid} a ex:ReseauxSociaux ;
            ex:contenu "{data.get('contenu','')}"^^xsd:string ;
            ex:lien "{data.get('lien','')}"^^xsd:string ;
            ex:nomPlateforme "{data.get('nomPlateforme','')}"^^xsd:string ;
            ex:partOf {uri} .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setQuery(insert_query)
    sparql.setMethod(POST)
    sparql.query()

    # Local RDF (idem que Evenement)
    camp_ref = EX[cid]
    g.add((camp_ref, RDF.type, EX.Campagne))
    g.add((camp_ref, EX.descriptioncampa, Literal(data.get('descriptioncampa',''))))
    g.add((camp_ref, EX.startDate, Literal(data.get('startDate',''), datatype=XSD.date)))
    g.add((camp_ref, EX.endDate, Literal(data.get('endDate',''), datatype=XSD.date)))
    g.add((camp_ref, EX.targetAudience, Literal(data.get('targetAudience',''))))
    g.add((camp_ref, EX.title, Literal(data.get('title',''))))

    # Affiche
    aff_ref = EX[f"Affiche_{cid}"]
    g.add((aff_ref, RDF.type, EX.Affiche))
    g.add((aff_ref, EX.contenuimage, Literal(data.get('contenuimage',''))))
    g.add((aff_ref, EX.image, Literal(data.get('image',''))))
    g.add((aff_ref, EX.partOf, camp_ref))

    # RéseauxSociaux
    res_ref = EX[f"Reseau_{cid}"]
    g.add((res_ref, RDF.type, EX.ReseauxSociaux))
    g.add((res_ref, EX.contenu, Literal(data.get('contenu',''))))
    g.add((res_ref, EX.lien, Literal(data.get('lien',''))))
    g.add((res_ref, EX.nomPlateforme, Literal(data.get('nomPlateforme',''))))
    g.add((res_ref, EX.partOf, camp_ref))

    g.serialize(destination=RDF_FILE, format="turtle")

    return jsonify({"message": f"Campagne {cid} créée avec succès."})
