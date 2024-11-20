# PROYECTO FINAL

<details>
  <summary><h2>T2 - Documentos XML y vistas HTML mediante XSLT</h2></summary>

# Conversor JSON a HTML via MongoDB, XSLT

Este script Python realiza consultas a una base de datos MongoDB, transforma los resultados a XML y luego aplica una transformación XSLT para generar un documento HTML.

## Requisitos

* Bibliotecas Python: `pymongo`, `lxml`, `json`, `xml.etree.ElementTree`, `re`
* MongoDB
* Un archivo XSLT para la transformación
* Un archivo JSON con la consulta

## Instalación

1. Instala las bibliotecas Python necesarias:

```bash
pip install pymongo lxml re
```

## Uso

1. **Configura la conexión MongoDB:** Modifica las variables `mongo_uri` y `database` en el script para que coincidan con tu configuración.

2. **Define la consulta:** Crea un archivo JSON que contenga la consulta de agregación de MongoDB. **Es crucial que el archivo JSON incluya una cabecera que especifique la colección a usar, con el siguiente formato:**

```json
// Coleccion: NombreDeLaColeccion
[
  { /* etapas de la consulta */ }
]
```

Por ejemplo:

```json
// Coleccion: Pruebas
[
  {
    "$match": {
      "campo": "valor"
    }
  }
]
```

3. **Especifica las rutas:** Ajusta las variables `query_file` y `xslt_path` en el script para que apunten a las ubicaciones de tu archivo de consulta JSON y el archivo XSLT, respectivamente.


## Consideraciones

* El script maneja errores de conexión a MongoDB y muestra mensajes de error apropiados.
* Si la consulta no devuelve resultados, se imprimirá un mensaje informando de ello.
*  La función `extraer_coleccion_de_json` busca específicamente la línea `// Coleccion: NombreDeLaColeccion`.  Es **indispensable** usar este formato exacto, incluyendo mayúsculas y minúsculas, para que el script funcione correctamente.


## Flujo de trabajo

1. Lee la consulta JSON y extrae el nombre de la colección.
2. Elimina los comentarios del JSON y lo convierte en un objeto Python.
3. Ejecuta la consulta en MongoDB.
4. Convierte los resultados de la consulta a formato XML.
5. Aplica la transformación XSLT al XML.
6. Guarda el HTML resultante en un archivo.

</details>
