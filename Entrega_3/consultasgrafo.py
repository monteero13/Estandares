from rdflib import Graph
import rdflib
import re

# Cargar el grafo RDF
g = Graph()
g.parse("covid_data.ttl", format="turtle")

# Función para ejecutar una consulta SPARQL
def execute_sparql_query(graph, query):
    results = graph.query(query)
    return results

# Función para leer consultas y sus cabeceras desde un archivo
def read_sparql_queries(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    queries = content.split("\n\n\n")
    result = []
    for q in queries:
        if q.strip():
            header = re.search(r"^#\s*(.*)", q.strip(), re.MULTILINE).group(1)
            query_body = q.strip()
            result.append((header, query_body))
    return result

# Leer consultas y cabeceras desde el archivo
queries_with_headers = read_sparql_queries("consultas.sparql")

# Ejecutar y mostrar los resultados de cada consulta
for header, query in queries_with_headers:
    print(f"\n{header}")  # Imprimir la cabecera
    results = execute_sparql_query(g, query)

    if not results:
        print("Respuesta Vacía")
    else:
        for row in results:
            print(", ".join([str(item.value) if isinstance(item, rdflib.term.Literal) else str(item) for item in row]))