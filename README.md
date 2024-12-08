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

<details>
  <summary><h2>T3 - Diseño de ontología en Protege y consultas SPARQL</h2></summary>

# Diseño y Consulta de Ontologías con Protege y SPARQL

Este proyecto implementa una ontología basada en la estructura de una base de datos MongoDB, modelando las relaciones entre clases e individuos. Además, se ejecutan consultas SPARQL para explorar la ontología y, como reto, se generan grafos RDF dinámicamente desde MongoDB mediante scripts en Python.

## Requisitos

### Herramientas necesarias
* **Protege**: Para el diseño y razonamiento de la ontología.
* **Python**: Para la generación de grafos RDF y ejecución de consultas SPARQL (opcional).
* **Bibliotecas Python**: `rdflib`, `pymongo` (para los retos).

### Archivos entregables
* `ontologia.owl`: Archivo principal de la ontología.
* `ontologia_reasoned.owl`: Ontología después de aplicar el razonador.
* `grafo.py`: Script de Python para la generación de grafos y su posterior ejecución con un txt con consultas.
* `consultasOntology.txt`: Consultas SPARQL realizadas para ejecutar sobre la **ontologia razonada**.
* `consultaspy.txt`: Consultas SPARQL realizadas para ejecutar con el script de python sobre el grafo.

### Archivos adicionales
* `covid_data.ttl`: Grafo generado tras la ejecución del script (para usar en caso de error).

## Instrucciones

### 1. Diseño de la Ontología
1. Se utiliza **Protege** para modelar las interacciones con la base de datos:
   * Se define clases, propiedades de objeto y propiedades de datos que reflejen las relaciones de las colecciones JSON.
   * Se añade individuos manualmente para representar datos relevantes en la base.

2. Se guarda el archivo resultante como `ontologia.owl`.

### 2. Razonamiento
1. Se aplica un razonador en **Protege** (Pellet) para inferir nuevas relaciones y mejorar la accesibilidad de la información.
2. Se guarda el resultado como `ontologia_reasoned.owl`.

### 3. Consultas SPARQL
1. Encuentra todos los pacientes con diagnóstico "Confirmado" y severidad "Crítico".
2. Lista los pacientes que requieren ventilación mecánica y el hospital donde fueron tratados.
3. Recupera el número de dosis de vacuna y el fabricante para cada paciente.
4. Obtiene los pacientes con resultado de PCR "Positivo" que están hospitalizados.
5. Lista los medicamentos utilizados en la UCI y sus proveedores para los pacientes.
6. Encuentra pacientes con síntomas específicos (como fiebre) en una fecha determinada.

### 4. (Reto) Generación de Grafo RDF desde MongoDB
1. Se escribe un script en Python que:
   * Conecta a la base de datos MongoDB usando `pymongo`.
   * Extrae datos de las colecciones relevantes.
   * Genera un grafo RDF usando `rdflib`.
2. Guarda el resultado como un archivo RDF o trabaja directamente con el grafo en memoria.

### 5. (Reto) Ejecución de Consultas SPARQL desde el Script
1. Se modifica la estructura de las consultas para que se adecuen a la estructura del grafo.
2. Se usa `rdflib` para ejecutar las consultas SPARQL sobre el grafo generado.
3. Se diseña el script para aceptar dinámicamente diferentes consultas SPARQL.

## Configuración del Script

1. **Conexión a MongoDB**: Modifica la URI de conexión `uri` para que coincida con tu configuración de base de datos MongoDB.
2. **Definir el Namespace**: Asegúrate de que el namespace `covid` coincida con la ontología que estás utilizando.
3. **Carga de Datos**: El script obtiene datos de las colecciones `Casos`, `Hospitalizaciones`, `Pruebas`, y `Vacunaciones` en MongoDB, y genera un grafo RDF con tripletas.
4. **Ejecutar Consultas SPARQL**: Lee y ejecuta las consultas SPARQL desde un archivo, mostrando los resultados obtenidos.
  </details>
