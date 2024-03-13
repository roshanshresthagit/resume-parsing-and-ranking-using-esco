import csv
import pymongo

# connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://pidan321:pidan321@cluster0.yq8rugc.mongodb.net/test")
db = client["mydatabase1"]

# create collections for skills and occupations
skills_collection = db["skills"]
occupations_collection = db["occupations"]

# load skill.csv into skills collection
with open('skills_en.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        skill = {
            "id": row["concept_uri"].split("/")[-1],
            "label": row["preferred_label"].lower()
        }
        skills_collection.insert_one(skill)

# load occupation.csv into occupations collection
with open('occupations_en.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        occupation = {
            "id": row["concept_uri"].split("/")[-1],
            "label": row["preferred_label"].lower()
        }
#         occupations_collection.insert_one(occupation)

# create skill-occupation relationship collection and load skillocupationrelation.csv
relation_collection = db["skill_occupation_relation"]
with open('occupationSkillRelations.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        relation = {
            "skill_id": row["skillUri"].split("/")[-1],
            "occupation_id": row["occupationUri"].split("/")[-1],
            "importance": row["importance"]
        }
        relation_collection.insert_one(relation)

