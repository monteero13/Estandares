import json
import pymongo
import xml.etree.ElementTree as ET
from lxml import etree
import re

def extraer_coleccion_de_json(json_string):
    try:
        # Busca el nombre de la colección usando una expresión regular.
        match = re.search(r"//.*Coleccion:\s*(\w+)", json_string, re.IGNORECASE)
        if match:
            return match.group(1)
        else:
            return "No se ha podido encontrar la colección en el JSON."
    except json.JSONDecodeError as e:
        return f"Error al extraer la colección: {e}"

def remove_comments_from_json(json_str):
    """Remove comments from a JSON string."""
    return re.sub(r'//.*?(\n|$)', '', json_str)

def execute_query(mongo_uri, database, collection, pipeline):
    """Connect to MongoDB and execute a query."""
    client = pymongo.MongoClient(mongo_uri)
    db = client[database]
    coll = db[collection]
    try:
        result = coll.aggregate(pipeline)
        client.close()
        return list(result)
    except Exception as e:
        print(f"Error executing query: {e}")
        client.close()
        return None

def json_to_xml(json_obj):
    """Convert JSON object to XML."""
    def build_element(element, data):
        if isinstance(data, dict):
            for key, value in data.items():
                sub_elem = ET.SubElement(element, key)
                build_element(sub_elem, value)
        elif isinstance(data, list):
            for item in data:
                sub_elem = ET.SubElement(element, "item")
                build_element(sub_elem, item)
        else:
            element.text = str(data)

    root = ET.Element("root")
    build_element(root, json_obj)
    return ET.tostring(root, encoding="unicode")

def apply_xslt(xml_str, xslt_path):
    """Apply XSLT to XML and return the transformed HTML."""
    xml = etree.fromstring(xml_str)
    xslt = etree.parse(xslt_path)
    transform = etree.XSLT(xslt)
    return str(transform(xml))

def main():
    mongo_uri = "mongodb+srv://Administrador:Grupo5@basededatos.wplin.mongodb.net/"
    database = "Covid"
    query_file = "consulta3.json"
    xslt_path = "plantilla.xslt"
    output_html = "salida_consulta3.html"

    # Leer la consulta desde el archivo JSON y eliminar comentarios
    with open(query_file, "r") as file:
        query_data = file.read()
        collection = extraer_coleccion_de_json(query_data)
        query_data_clean = remove_comments_from_json(query_data)
        pipeline = json.loads(query_data_clean)

    # Ejecutar la consulta
    results = execute_query(mongo_uri, database, collection, pipeline)
    print(results)

    # Si la consulta tiene éxito
    if results:
        # Transformar a XML
        xml_str = json_to_xml(results)

        # Aplicar la plantilla XSLT y generar HTML
        html_content = apply_xslt(xml_str, xslt_path)

        # Asegurar que el HTML esté en UTF-8
        html_content_utf8 = f'<?xml version="1.0" encoding="UTF-8"?>\n{html_content}'

        # Guardar el resultado en un archivo HTML con codificación UTF-8
        with open(output_html, "w", encoding="utf-8") as output_file:
            output_file.write(html_content_utf8)
    else:
        print("La consulta no devolvió resultados o hubo un error.")

if __name__ == "__main__":
    main()
