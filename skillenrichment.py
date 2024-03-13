from rdflib import Graph, Namespace, URIRef
import pymongo
from database import mongo


def enrich(skill_set):
    # Load the ESCO ontology into an RDF graph
    g = Graph()
    g.parse('ESCOontology/esco.rdf', format='xml')
    # print(len(g))  # should print the number of triples in the graph
    skillset = skill_set
    # Define the ESCO namespace
    ESCO = Namespace('http://data.europa.eu/esco/model/1.2')

    # Connect to MongoDB and get skill and occupation collections
    client = pymongo.MongoClient("mongodb+srv://pidan321:pidan321@cluster0.yq8rugc.mongodb.net/test")
    db = client["mydatabase1"]
    skills_collection = db["skills"]
    occupations_collection = db["occupations"]
    relation_collection = db["skill_occupation_relation"]

    # Loop through each skill in the skillset and find related skills and occupations
    for skill in skillset:
        # Find the skill URI from the skills collection
        skill_doc = skills_collection.find_one({"label": skill})
        if skill_doc:
            skill_uri = skill_doc["id"]
            query = """
            SELECT ?label
            WHERE {{
                <{uri}> <{broader}> ?parent .
                ?parent <{prefLabel}> ?label .
            }}
            """.format(uri=skill_uri, broader=ESCO.broader, prefLabel=ESCO.prefLabel)

            # Execute the SPARQL query and add related skills to the skillset
            results = g.query(query)
            for row in results:
                related_skill = row[0].value.title()
                if related_skill not in skillset:
                    skillset.append(related_skill)

            # Find occupations that require the skill from the relation collection
            occupations = occupations_collection.find(
                {"id": {"$in": [r['occupation_id'] for r in relation_collection.find({"skill_id": skill_uri})]}})
            for occupation in occupations:
                if occupation["label"] not in skillset:
                    skillset.append(occupation["label"])

    # Print the enriched skillset
    print('1')
    print(skillset)
    return (skillset)
