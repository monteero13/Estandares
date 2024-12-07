from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD
from pymongo import MongoClient
import json

# Conexión a MongoDB
uri = "mongodb+srv://Administrador:Grupo5@basededatos.wplin.mongodb.net/"
client = MongoClient(uri)
db = client["Covid"]

# Crear un grafo RDF
g = Graph()

# Definir el namespace
covid = Namespace("http://www.semanticweb.org/grupo5/covid-ontology#")
g.bind("covid", covid)


# Función para agregar tripletas al grafo
def add_triples(subject, predicate, obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_subject = URIRef(subject + "/" + key)
            g.add((subject, predicate, new_subject))
            add_triples(new_subject, covid[key], value)
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict):

                key = list(item.keys())[0]
                new_subject = URIRef(subject + "/" + key)
                g.add((subject, predicate, new_subject))
                add_triples(new_subject, covid[key], item[key])
                for item_key, item_value in item.items():
                    if item_key != key:
                        add_triples(new_subject, covid[item_key], item_value)
            else:
                g.add((subject, predicate, Literal(item)))

    else:
        g.add((subject, predicate, Literal(obj)))


# Cargar datos de casos y agregar al grafo
casos_collection = db["Casos"]
for caso in casos_collection.find():
    paciente_uri = covid["paciente/" + caso["id_paciente"]]
    g.add((paciente_uri, RDF.type, covid.Paciente))
    for key, value in caso.items():
        if key != "_id":
            add_triples(paciente_uri, covid[key], value)

# Cargar datos de hospitalizaciones y agregar al grafo
hospitalizaciones_collection = db["Hospitalizaciones"]
for hospitalizacion in hospitalizaciones_collection.find():
    hosp_uri = covid["hospitalizacion/" + hospitalizacion["_id"]]
    g.add((hosp_uri, RDF.type, covid.Hospitalizacion))
    for key, value in hospitalizacion.items():
        if key != "_id":
            add_triples(hosp_uri, covid[key], value)

# Cargar datos de pruebas y agregar al grafo
pruebas_collection = db["Pruebas"]
for prueba in pruebas_collection.find():
    prueba_uri = covid["prueba/" + prueba["_id"]]
    g.add((prueba_uri, RDF.type, covid.Prueba))
    for key, value in prueba.items():
        if key != "_id":
            add_triples(prueba_uri, covid[key], value)

# Cargar datos de vacunaciones y agregar al grafo
vacunaciones_collection = db["Vacunaciones"]
for vacunacion in vacunaciones_collection.find():
    vacuna_uri = covid["vacunacion/" + vacunacion["_id"]]
    g.add((vacuna_uri, RDF.type, covid.Vacunacion))
    for key, value in vacunacion.items():
        if key != "_id":
            add_triples(vacuna_uri, covid[key], value)

# Guardar el grafo en formato Turtle
g.serialize(destination="covid_data.ttl", format="turtle")