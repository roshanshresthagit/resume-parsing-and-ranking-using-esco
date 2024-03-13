from rdflib import Graph, Namespace, URIRef
import pymongo

# Load the ESCO ontology into an RDF graph
g = Graph()
g.parse('esco.rdf', format='xml')
print(len(g))  # should print the number of triples in the graph

# Define the ESCO namespace
ESCO = Namespace('http://data.europa.eu/esco/model/1.2')

# Connect to MongoDB and get skill and occupation collections
client = pymongo.MongoClient("mongodb+srv://pidan321:pidan321@cluster0.yq8rugc.mongodb.net/test")
db = client["mydatabase"]
skills_collection = db["skills"]
occupations_collection = db["occupations"]
relation_collection = db["skill_occupation_relation"]

# Loop through each skill in the skills collection and find related skills and occupations
for skill_doc in skills_collection.find():
    print('skill search start')
    skill_uri = skill_doc["id"]
    skillset = [skill_doc["label"]]  # Initialize skillset with the current skill

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
    print('skill search finish')
    # Find occupations that require the skill from the relation collection
    occupations = occupations_collection.find({"id": {"$in": [r['occupation_id'] for r in relation_collection.find({"skill_id": skill_uri})]}})
    print('occupation search start')
    for occupation in occupations:
        if occupation["label"] not in skillset:
            skillset.append(occupation["label"])

    # Update the skill document in the skills collection with the enriched skillset
    skills_collection.update_one({"id": skill_uri}, {"$set": {"enriched_skills": skillset}})
    print('occupation search finish')
# Print the enriched skillset for a specific skill to verify it has been updated in the skills collection
print(skills_collection.find_one({"label": "Machine learning"}))
