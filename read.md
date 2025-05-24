<p align="center">
  <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" alt="Python Logo" width="150" style="margin-right: 20px;"/>
  <img src="https://raw.githubusercontent.com/pallets/flask/main/docs/_static/flask-logo.png" alt="Flask Logo" width="150" style="margin-right: 20px;"/>
  <img src="https://webassets.mongodb.com/_com_assets/cms/MongoDB_Logo_FullColor_RGB-4td3yuxzjs.png" alt="MongoDB Logo" width="200" style="margin-right: 20px;"/>
  <img src="https://www.mysql.com/common/logos/logo-mysql-170x115.png" alt="MySQL Logo" width="150" style="margin-right: 20px;"/>
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/New_Power_BI_Logo.svg/1200px-New_Power_BI_Logo.svg.png" alt="Power BI Logo" width="100"/>
</p>

# 🎬 Proyecto Final: API RESTful para Gestión de Cine (SQL, MongoDB & Power BI) 🍿

**Bienvenido al README detallado del Proyecto Final del Tercer Corte.**

Este documento sirve como una guía exhaustiva para entender, configurar, ejecutar y probar la API RESTful desarrollada. El sistema está construido con **Flask (Python)** y está diseñado para gestionar las operaciones de un complejo de cine. Una característica clave es su interacción con dos tipos de bases de datos: una relacional **MySQL** para datos estructurados y una NoSQL **MongoDB** para flexibilidad con ciertos tipos de datos. La API expone un conjunto completo de operaciones CRUD (Crear, Leer, Actualizar, Eliminar) para ambas fuentes de datos.

Finalmente, este README explica cómo los datos expuestos por esta API pueden ser consumidos, transformados y visualizados utilizando **Power BI**, permitiendo así el análisis de la información del cine.

---

## 🌟 Índice de Contenidos

1.  [🎯 **Objetivo Detallado del Proyecto**](#-objetivo-detallado-del-proyecto)
2.  [🛠️ **Prerrequisitos de Software y Herramientas**](#️-prerrequisitos-de-software-y-herramientas)
3.  [🚀 **Guía Detallada de Configuración e Instalación**](#-guía-detallada-de-configuración-e-instalación)
    * [3.1. Obtención del Código Fuente](#31-obtención-del-código-fuente)
    * [3.2. Configuración del Entorno Virtual y Gestión de Dependencias](#32-configuración-del-entorno-virtual-y-gestión-de-dependencias)
    * [3.3. Preparación Exhaustiva de las Bases de Datos](#33-preparación-exhaustiva-de-las-bases-de-datos)
        * [Configuración de MySQL](#configuración-de-mysql)
        * [Configuración de MongoDB](#configuración-de-mongodb)
    * [3.4. Configuración Específica de la API (app.py)](#34-configuración-específica-de-la-api-apppy)
4.  [▶️ **Ejecución y Verificación Inicial de la API**](#️-ejecución-y-verificación-inicial-de-la-api)
5.  [🧩 **Arquitectura y Endpoints de la API Explicados**](#-arquitectura-y-endpoints-de-la-api-explicados)
6.  [🔗 **Mecanismos de Conexión a Bases de Datos Detallados**](#-mecanismos-de-conexión-a-bases-de-datos-detallados)
    * [Interacción con SQL (MySQL) vía Flask-SQLAlchemy](#interacción-con-sql-mysql-vía-flask-sqlalchemy)
    * [Interacción con NoSQL (MongoDB) vía PyMongo](#interacción-con-nosql-mongodb-vía-pymongo)
7.  [📊 **Guía Paso a Paso para Visualización en Power BI**](#-guía-paso-a-paso-para-visualización-en-power-bi)
8.  [🧪 **Población de Datos Masivos para Pruebas (Opcional)**](#-población-de-datos-masivos-para-pruebas-opcional)
9.  [📁 **Análisis de la Estructura del Proyecto**](#-análisis-de-la-estructura-del-proyecto)
10. [🤔 **Guía de Solución de Problemas Comunes (Troubleshooting)**](#-guía-de-solución-de-problemas-comunes-troubleshooting)
11. [👨‍💻 **Autor(es) del Proyecto**](#-autores-del-proyecto)

---

## 🎯 Objetivo Detallado del Proyecto

El propósito fundamental de este proyecto es demostrar la habilidad para:
* **Diseñar y desarrollar una API RESTful** utilizando el framework Flask en Python, siguiendo los principios REST.
* **Integrar y gestionar múltiples tipos de bases de datos**: una base de datos relacional (MySQL) y una base de datos NoSQL (MongoDB), cada una adecuada para diferentes tipos de datos o necesidades.
* **Implementar operaciones CRUD** (Crear, Leer, Actualizar, Eliminar) de manera completa y eficiente para todas las entidades principales del sistema en ambas bases de datos.
* **Exponer datos de manera segura y estructurada** (JSON) a través de los endpoints de la API.
* **Consumir datos de la API desde una herramienta de Business Intelligence (Power BI)**, incluyendo la transformación de datos necesaria para su correcta visualización y análisis, permitiendo generar informes y dashboards.

Este proyecto busca consolidar conocimientos en desarrollo backend, gestión de bases de datos heterogéneas y principios básicos de inteligencia de negocios.

---

## 🛠️ Prerrequisitos de Software y Herramientas

Para asegurar una configuración y ejecución exitosa del proyecto, es indispensable contar con el siguiente software y herramientas instaladas y operativas en tu sistema:

* **Python:** Se recomienda la versión 3.8 o una superior. Python es el lenguaje de programación principal del proyecto. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).
* **PIP:** Es el sistema de gestión de paquetes de Python, utilizado para instalar y administrar las librerías necesarias. Usualmente se instala de forma automática con Python.
* **Virtualenv:** (Altamente Recomendado) Herramienta para crear entornos virtuales de Python. Esto permite aislar las dependencias del proyecto, evitando conflictos con otros proyectos o con las librerías globales del sistema. Se instala con `pip install virtualenv`.
* **Servidor MySQL:** Se requiere una instancia de MySQL Community Server (versión 5.7 o superior, idealmente 8.x) en ejecución. Esta será la base de datos SQL. Puedes descargarlo desde [dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/).
    * **Herramienta de Gestión MySQL:** Se recomienda una interfaz gráfica como **MySQL Workbench** para facilitar la administración de la base de datos, ejecución de scripts y visualización de datos. [Descargar MySQL Workbench](https://dev.mysql.com/downloads/workbench/).
* **Servidor MongoDB:** Se necesita una instancia de MongoDB Community Server (versión 4.x o superior) en ejecución. Esta será la base de datos NoSQL. Puedes descargarlo desde [www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community).
    * **MongoDB Shell (`mongosh`):** Es la interfaz de línea de comandos para interactuar con MongoDB, esencial para ejecutar scripts y verificar datos. [Instalar mongosh](https://www.mongodb.com/docs/mongodb-shell/install/).
* **Power BI Desktop:** La herramienta de Microsoft para la visualización de datos y creación de informes. [Descargar Power BI Desktop](https://powerbi.microsoft.com/es-es/desktop/).
* **(Opcional pero Recomendado para Pruebas) Cliente API:** Herramientas como [Postman](https://www.postman.com/downloads/) o [Insomnia](https://insomnia.rest/download) son extremadamente útiles para enviar peticiones a los endpoints de la API, probar diferentes métodos HTTP (GET, POST, PUT, DELETE) y visualizar las respuestas.

---

## 🚀 Guía Detallada de Configuración e Instalación

Sigue estos pasos meticulosamente para asegurar una correcta configuración del proyecto en tu entorno de desarrollo local.

### 3.1. Obtención del Código Fuente

* **Opción A: Clonar el Repositorio (si está en Git)**
    Si el código fuente del proyecto está alojado en un servicio como GitHub, GitLab o Bitbucket, clónalo utilizando Git:
    ```bash
    git clone <https://github.com/ales45/Api_Cine>
    cd <NOMBRE_DE_LA_CARPETA_DEL_PROYECTO_EJ:tu_proyecto>
    ```
    *Reemplaza los placeholders con la información real de tu repositorio.*
* **Opción B: Descarga Directa**
    Si tienes los archivos del proyecto en un archivo comprimido (ej. ZIP), descárgalo y extráelo en una carpeta de tu elección.

### 3.2. Configuración del Entorno Virtual y Gestión de Dependencias

**¿Por qué un entorno virtual?** Es una práctica estándar en Python para aislar las dependencias (librerías y sus versiones específicas) de tu proyecto. Esto previene conflictos entre las dependencias de diferentes proyectos y asegura que el proyecto funcione con las versiones de librerías con las que fue desarrollado.

1.  **Navega a la carpeta raíz del proyecto** en tu terminal o línea de comandos.
    * *Este es el directorio donde se encuentra el archivo `app.py` y otros archivos principales.*
2.  **Crea un entorno virtual:** Se recomienda nombrar la carpeta del entorno como `.venv` o `env`.
    ```bash
    python -m venv .venv
    ```
    * *El comando `python -m venv <nombre_entorno>` invoca el módulo `venv` de Python para crear el entorno. El `.` al inicio de `.venv` es una convención para indicar que es una carpeta "oculta" o de configuración.*
3.  **Activa el entorno virtual:** Este paso es crucial. Los comandos varían según tu sistema operativo y terminal.
    * **Windows (CMD):**
        ```bash
        .\.venv\Scripts\activate.bat
        ```
    * **Windows (PowerShell):**
        ```bash
        .\.venv\Scripts\Activate.ps1
        ```
        *(Si encuentras un error de ejecución de scripts en PowerShell, puede que necesites cambiar la política de ejecución con `Set-ExecutionPolicy Unrestricted -Scope Process` y luego intentar activar de nuevo.)*
    * **macOS / Linux (bash/zsh):**
        ```bash
        source .venv/bin/activate
        ```
    * *Una vez activado, el prompt de tu terminal cambiará, usualmente mostrando `(.venv)` al inicio, indicando que cualquier comando de Python o `pip` se ejecutará dentro de este entorno aislado.*
4.  **Instala las dependencias de Python:**
    Las dependencias son las librerías externas que tu API necesita para funcionar.
    * Idealmente, el proyecto debería incluir un archivo `requirements.txt`. Si es así, puedes instalar todas las dependencias con un solo comando:
        ```bash
        pip install -r requirements.txt
        ```
        *(Puedes generar este archivo tú mismo una vez que hayas instalado todo manualmente, usando: `pip freeze > requirements.txt`)*
    * Si no hay `requirements.txt`, instala las librerías necesarias manualmente:
        ```bash
        pip install Flask Flask-SQLAlchemy pymongo mysql-connector-python Faker
        ```
        * **`Flask`:** Es el microframework web sobre el que se construye la API.
        * **`Flask-SQLAlchemy`:** Una extensión de Flask que integra SQLAlchemy, un potente ORM (Object-Relational Mapper) para interactuar con bases de datos SQL.
        * **`pymongo`:** El driver oficial de Python para MongoDB, necesario para todas las interacciones con la base de datos NoSQL.
        * **`mysql-connector-python`:** El driver que SQLAlchemy (a través de Flask-SQLAlchemy) usará para comunicarse con tu base de datos MySQL. (Si optaste por `mysqlclient`, asegúrate de instalar ese en su lugar y de que tu cadena de conexión lo refleje).
        * **`Faker`:** (Opcional) Una librería muy útil para generar datos falsos (de prueba). Solo es necesaria si planeas ejecutar el script `poblar_datos.py`.

### 3.3. Preparación Exhaustiva de las Bases de Datos

La API se conecta a dos bases de datos. Ambas deben estar configuradas y accesibles.

#### Configuración de MySQL
1.  **Asegúrate de que tu servidor MySQL esté iniciado y funcionando.**
2.  Conéctate a tu instancia de MySQL utilizando tu herramienta de gestión preferida (ej. MySQL Workbench, DBeaver, o el cliente de línea de comandos `mysql -u tu_usuario -p`).
3.  **Crea la base de datos `proyectoCine`:** Es importante usar el juego de caracteres y la colación adecuados para soportar diversos caracteres, como `utf8mb4`.
    ```sql
    CREATE DATABASE proyectoCine CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ```
4.  **Selecciona la base de datos `proyectoCine`** para asegurar que los siguientes comandos se ejecuten en el contexto correcto:
    ```sql
    USE proyectoCine;
    ```
5.  **Ejecuta el contenido completo del script `ProyectoCine.sql`:** Este archivo contiene las sentencias `CREATE TABLE` para todas tus entidades (Pelicula, Sala, Cliente, Funcion, Boleto), así como las `CREATE VIEW` para las vistas y `CREATE TRIGGER` para la lógica de validación de capacidad. Ejecuta todo el script.

#### Configuración de MongoDB
1.  **Asegúrate de que tu servidor MongoDB (`mongod`) esté iniciado y funcionando.**
2.  Abre el **MongoDB Shell (`mongosh`)** en tu terminal.
3.  **Selecciona la base de datos `proyectoCineMongo`**. Si la base de datos no existe, MongoDB la creará implícitamente cuando insertes el primer documento o crees la primera colección.
    ```javascript
    use proyectoCineMongo;
    ```
4.  **Ejecuta el script `script.js`** (o el nombre que le hayas asignado, ej: `crear_mongo_proyecto_cine.js`). Este script debería contener comandos para:
    * Crear las colecciones (`db.createCollection("peliculas");`, etc.), aunque esto es opcional ya que MongoDB las crea al primer `insert`.
    * Opcionalmente, insertar algunos documentos de ejemplo para que la base de datos no esté vacía.
    Puedes pegar el contenido del script directamente en `mongosh` o usar el comando `load()` si el script está en un archivo:
    ```javascript
    // Ejemplo de cómo cargar un script desde mongosh:
    load('/ruta/absoluta/o/relativa/a/tu/script.js');
    ```

### 3.4. Configuración Específica de la API (app.py)

El archivo principal de la API, `app.py`, necesita conocer cómo conectarse a tu base de datos MySQL.

1.  Abre el archivo `app.py` en tu editor de código.
2.  Localiza la sección donde se configura la `SQLALCHEMY_DATABASE_URI`. Esta cadena de conexión es vital.
3.  **Actualiza la cadena con tus credenciales de MySQL y detalles del servidor:**
    ```python
    # Dentro de app.py:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://TU_USUARIO_MYSQL:TU_CONTRASEÑA_MYSQL@localhost/proyectoCine'
    ```
    * Reemplaza `TU_USUARIO_MYSQL` con tu nombre de usuario de MySQL (comúnmente `root` para entornos locales).
    * Reemplaza `TU_CONTRASEÑA_MYSQL` con la contraseña correspondiente. Si tu usuario `root` local no tiene contraseña, la cadena podría ser `mysql+mysqlconnector://root:@localhost/proyectoCine`.
    * `localhost` asume que MySQL corre en tu misma máquina. Si está en otro host o puerto, ajústalo (ej: `hostname:puerto`).
    * `/proyectoCine` es el nombre de la base de datos que creaste.
    * **Importante:** El dialecto `mysql+mysqlconnector` debe coincidir con el driver de Python que instalaste (`mysql-connector-python`). Si instalaste `mysqlclient`, el dialecto sería `mysql+mysqlclient`.

---

## ▶️ Ejecución y Verificación Inicial de la API

Con toda la configuración lista, puedes iniciar la API:

1.  Asegúrate de que tu **entorno virtual (`.venv`) esté activado** en la terminal.
2.  Verifica que estés en la **carpeta raíz del proyecto** (donde reside `app.py`).
3.  Ejecuta el siguiente comando para iniciar el servidor de desarrollo de Flask:
    ```bash
    python app.py
    ```
4.  **Observa la salida en la terminal.** Si todo es correcto, Flask iniciará el servidor y mostrará mensajes similares a estos:
    ```
     * Serving Flask app 'app' (lazy loading)
     * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
     * Debug mode: on
     * Running on [http://127.0.0.1:5000/](http://127.0.0.1:5000/) (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: XXX-XXX-XXX
    ```
    * La línea `Running on http://127.0.0.1:5000/` indica que tu API está activa y escuchando peticiones en esa dirección y puerto.
    * El "Debug mode: on" es muy útil durante el desarrollo, ya que proporciona mensajes de error detallados en el navegador y recarga automáticamente el servidor cuando haces cambios en el código.
5.  **Verificación rápida:** Abre tu navegador web y visita `http://127.0.0.1:5000/`. Deberías ver una respuesta JSON como: `{"mensaje": "API del Proyecto Cine funcionando!"}`. Esta es la ruta raíz definida en `app.py` y confirma que la API está respondiendo.

---

## 🧩 Arquitectura y Endpoints de la API Explicados

La API está estructurada para ser RESTful, lo que significa que utiliza:
* URLs (endpoints) para identificar recursos.
* Métodos HTTP (GET, POST, PUT, DELETE) para definir las acciones sobre esos recursos.
* JSON como formato estándar para el intercambio de datos.

### Entidades Principales Gestionadas
La API maneja las siguientes entidades clave del sistema de cine:
* **Pelicula:** Información sobre las películas (título, género, duración, etc.).
* **Sala:** Detalles de las salas de cine (nombre, capacidad, tipo).
* **Cliente:** Datos de los clientes registrados.
* **Funcion:** Programación de las películas en salas específicas, con fechas, horas y precios.
* **Boleto:** Registros de los boletos vendidos para funciones específicas a clientes.

### Convención de Rutas (Endpoints)
Para diferenciar entre las operaciones de las dos bases de datos, se utilizan prefijos en las rutas:
* Operaciones sobre la base de datos **MySQL**: Todas las rutas comienzan con `/sql/...`
* Operaciones sobre la base de datos **MongoDB**: Todas las rutas comienzan con `/mongo/...`

### Resumen de Operaciones CRUD Típicas
La siguiente tabla muestra el patrón general para los endpoints CRUD de cada entidad:

| Método HTTP | Ruta Ejemplo                               | Descripción Detallada                                  |
| :---------- | :----------------------------------------- | :----------------------------------------------------- |
| `GET`       | `/sql/peliculas`                           | Recupera una lista de todas las películas desde MySQL.    |
| `POST`      | `/sql/peliculas`                           | Crea una nueva película en MySQL. Espera datos JSON en el cuerpo. |
| `GET`       | `/sql/peliculas/<id_pelicula_sql>`         | Recupera una película específica de MySQL por su ID.      |
| `PUT`       | `/sql/peliculas/<id_pelicula_sql>`         | Actualiza una película existente en MySQL. Espera datos JSON. |
| `DELETE`    | `/sql/peliculas/<id_pelicula_sql>`         | Elimina una película específica de MySQL por su ID.       |
| `GET`       | `/mongo/peliculas`                         | Recupera una lista de todas las películas desde MongoDB.  |
| `POST`      | `/mongo/peliculas`                         | Crea una nueva película en MongoDB. Espera datos JSON.    |
| `GET`       | `/mongo/peliculas/<id_pelicula_mongo>`     | Recupera una película específica de MongoDB por su _id. |
| `PUT`       | `/mongo/peliculas/<id_pelicula_mongo>`     | Actualiza una película existente en MongoDB. Espera datos JSON. |
| `DELETE`    | `/mongo/peliculas/<id_pelicula_mongo>`     | Elimina una película específica de MongoDB por su _id.  |

*Este patrón se repite para las entidades `salas`, `clientes`, `funciones`, y `boletos` en ambos prefijos (`/sql/` y `/mongo/`).*

### Endpoints Especiales (Simulación de Vistas)
Para replicar la funcionalidad de las vistas SQL definidas en `ProyectoCine.sql`, se han creado endpoints específicos que realizan las consultas o agregaciones necesarias:
* `/sql/vista/funciones` y `/mongo/vista/funciones`: Muestran información combinada sobre las funciones (película, sala, horario, precio).
* `/sql/vista/ingresos-por-pelicula` y `/mongo/vista/ingresos-por-pelicula`: Calculan y muestran los ingresos totales generados por cada película.

*Para una especificación exhaustiva de cada endpoint, incluyendo los campos esperados en las solicitudes POST/PUT y la estructura exacta de las respuestas JSON, es fundamental consultar el código fuente en el archivo `app.py`.*

---

## 🔗 Mecanismos de Conexión a Bases de Datos Detallados

La API interactúa con dos sistemas de bases de datos fundamentalmente diferentes, utilizando las herramientas y técnicas adecuadas para cada uno.

### Interacción con SQL (MySQL) vía Flask-SQLAlchemy
* **Flask-SQLAlchemy** es una extensión de Flask que simplifica el uso de **SQLAlchemy**, un popular y potente kit de herramientas SQL y Mapeador Objeto-Relacional (ORM) para Python.
* **Configuración:** La conexión se establece a través de la `SQLALCHEMY_DATABASE_URI` en la configuración de la aplicación Flask (`app.config`). Esta URI contiene toda la información necesaria:
    ```python
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://usuario:contraseña@host/basedatos'
    ```
    * `mysql+mysqlconnector`: Especifica el dialecto (MySQL) y el driver (mysql-connector-python).
* **Modelos ORM:** Se definen clases en Python (ej. `PeliculaSQL`, `SalaSQL` en `app.py`) que heredan de `db_sql.Model` (donde `db_sql = SQLAlchemy(app)`). Estas clases representan las tablas de la base de datos. Cada atributo de la clase corresponde a una columna en la tabla.
    * Esto permite realizar consultas y manipulaciones de datos de una manera más "Pythónica" y orientada a objetos, abstrayendo gran parte del SQL directo. Ejemplo: `PeliculaSQL.query.all()` o `db_sql.session.add(nueva_pelicula)`.
* **Sesiones:** SQLAlchemy utiliza un objeto `Session` (`db_sql.session`) para gestionar las transacciones. Los cambios se agrupan y se envían a la base de datos con `db_sql.session.commit()`, o se pueden revertir con `db_sql.session.rollback()`.

### Interacción con NoSQL (MongoDB) vía PyMongo
* **PyMongo** es el driver oficial de Python recomendado por MongoDB para trabajar con bases de datos MongoDB. Proporciona una interfaz directa para ejecutar comandos y operaciones de MongoDB.
* **Configuración:**
    ```python
    MONGO_URI = "mongodb://localhost:27017/" # URI del servidor MongoDB
    MONGO_DB_NAME = "proyectoCineMongo"      # Nombre de la base de datos a usar
    client = MongoClient(MONGO_URI)         # Se crea un cliente
    db_mongo = client[MONGO_DB_NAME]        # Se selecciona la base de datos
    ```
* **Operaciones sobre Colecciones:** En MongoDB, los datos se almacenan en colecciones (similares a tablas) como documentos BSON (formato binario similar a JSON). PyMongo permite interactuar directamente con estas colecciones:
    * `db_mongo.peliculas.find()`: Recupera documentos de la colección `peliculas`.
    * `db_mongo.salas.insert_one({"nombre": "Sala Nueva", ...})`: Inserta un nuevo documento.
    * `db_mongo.clientes.update_one({"_id": ObjectId(id)}, {"$set": {"correo": "nuevo@correo.com"}})`: Actualiza un documento.
    * `db_mongo.boletos.delete_one({"_id": ObjectId(id)})`: Elimina un documento.
* **Manejo de `ObjectId`:** Los IDs de los documentos en MongoDB (`_id`) son del tipo `ObjectId`. PyMongo los maneja, pero al enviar/recibir datos a través de la API JSON, es común convertirlos a/desde strings.

---

## 📊 Guía Paso a Paso para Visualización en Power BI

Power BI puede consumir datos directamente desde los endpoints de tu API Flask. Esto permite crear informes dinámicos basados en la información más reciente de tus bases de datos.

1.  **Prerrequisito Indispensable:** Asegúrate de que tu **API Flask esté en ejecución** y sea accesible desde la máquina donde tienes Power BI Desktop (normalmente, si ambos están en tu PC local, la API en `http://127.0.0.1:5000/` será accesible).
2.  **Abre Power BI Desktop.**
3.  En la cinta de opciones "Inicio", haz clic en el botón **"Obtener datos"**. En el menú desplegable que aparece, busca y selecciona **"Web"**. (También puedes encontrarlo en "Obtener datos" -> "Más..." -> "Otros" -> "Web").
4.  Aparecerá el cuadro de diálogo **"Desde la Web"**:
    * Asegúrate de que la opción **"Básico"** esté seleccionada.
    * En el campo **"URL"**, introduce la dirección URL completa de uno de los endpoints `GET` de tu API que devuelve los datos que deseas importar. Es crucial que este endpoint devuelva los datos en formato JSON.
        * *Ejemplo para obtener todas las películas de la base de datos SQL:*
            `http://127.0.0.1:5000/sql/peliculas`
        * *Ejemplo para obtener la vista de funciones de la base de datos MongoDB:*
            `http://127.0.0.1:5000/mongo/vista/funciones`
    * Haz clic en **"Aceptar"**. Power BI intentará conectarse al endpoint y descargar los datos.
5.  **Transformación de Datos en el Editor de Power Query:**
    Si la conexión es exitosa, se abrirá el **Editor de Power Query** con una vista previa de los datos recuperados. El tratamiento de los datos JSON es un paso común:
    * **Si los datos aparecen como una Lista (List):**
        Si la API devuelve una lista de objetos JSON (muy común para endpoints que devuelven múltiples registros), Power BI podría mostrar esto como una "Lista". Verás una opción en la cinta de opciones (pestaña "Transformar") o en la barra de herramientas contextual que dice **"Convertir en tabla"**. Haz clic en ella. Acepta las opciones predeterminadas en el pequeño diálogo que aparece (normalmente no se necesita un delimitador).
    * **Expandir Columnas de Registros (Records):**
        Después de convertir a tabla (o si Power BI ya lo interpretó como una tabla con una columna que contiene `Record` en cada celda), necesitas "desplegar" estos registros para ver los campos individuales como columnas. Busca la columna que contiene los `Record`s y haz clic en el **icono de expansión** en su encabezado (parece dos flechas apuntando en direcciones opuestas ↖️↘️).
        * En el menú desplegable de expansión, puedes desmarcar la casilla "Usar nombre de columna original como prefijo" para evitar que los nombres de las nuevas columnas tengan un prefijo largo (ej. `Column1.titulo` en lugar de solo `titulo`).
        * Selecciona todas las columnas (campos del JSON) que deseas incluir en tu tabla de Power BI.
        * Haz clic en "Aceptar".
    * **Verificar y Ajustar Tipos de Datos:**
        Power BI intentará adivinar el tipo de dato para cada nueva columna (texto, número, fecha, etc.). Es crucial revisar estos tipos. Puedes cambiar el tipo de dato haciendo clic en el icono a la izquierda del nombre de la columna (ej. "ABC", "123", "📅") y seleccionando el tipo correcto (ej. "Número decimal", "Número entero", "Fecha", "Texto").
6.  **Cargar Datos al Modelo:**
    Una vez que los datos estén limpios y con el formato tabular correcto en el Editor de Power Query, haz clic en el botón **"Cerrar y aplicar"** (ubicado en la pestaña "Inicio" del editor). Esto cargará los datos en el modelo de datos de Power BI.
7.  **Obtener Datos de Múltiples Endpoints:**
    Para traer datos de diferentes partes de tu API (ej. películas SQL, funciones MongoDB, clientes SQL), **repite los pasos 3 a 6** para cada endpoint relevante. Cada endpoint consumido se convertirá en una tabla separada (o "consulta") en tu panel "Campos" de Power BI.
8.  **Crear Visualizaciones:**
    Con los datos cargados:
    * Puedes ir a la vista **"Modelo"** (icono de diagrama a la izquierda) para establecer relaciones entre tus tablas si es necesario (ej. si importaste "Funciones" y "Películas" por separado y quieres relacionarlas por un ID común).
    * Luego, ve a la vista **"Informe"** (icono de gráfico de barras). Aquí es donde construyes tus visualizaciones. Arrastra campos desde el panel "Campos" (que ahora contiene tus tablas importadas) al lienzo del informe y elige diferentes tipos de visualización del panel "Visualizaciones" (gráficos de barras, gráficos de pastel, tablas, tarjetas, mapas, etc.).

---

## 🧪 Poblar Bases de Datos con Datos Masivos (Opcional)

Para realizar pruebas de rendimiento de la API o tener un volumen de datos más significativo para las visualizaciones en Power BI, puedes utilizar el script `poblar_datos.py`.

1.  **Instalar `Faker`:** Si aún no lo has hecho, instala la librería Faker en tu entorno virtual activado:
    ```bash
    pip install Faker
    ```
2.  **Configurar el Script:**
    * Abre el archivo `poblar_datos.py`.
    * Al inicio del script, encontrarás variables para la configuración de la conexión a MySQL (ej. `DB_USER_SQL`, `DB_PASSWORD_SQL`). Asegúrate de que estas credenciales sean correctas para tu entorno local.
    * Puedes ajustar las variables `NUM_PELICULAS`, `NUM_SALAS`, etc., si deseas generar una cantidad diferente de registros.
3.  **Ejecutar el Script:**
    Desde tu terminal, con el entorno virtual activado y ubicado en la carpeta raíz del proyecto:
    ```bash
    python poblar_datos.py
    ```
    * El script comenzará a generar e insertar datos en ambas bases de datos (MySQL y MongoDB). Imprimirá mensajes de progreso en la consola. Este proceso puede tardar varios minutos dependiendo de la cantidad de datos a generar (los valores por defecto son 5000 para la mayoría de las entidades).
    * El script está diseñado para crear las tablas SQL si no existen, utilizando las definiciones de los modelos SQLAlchemy.

---

/nombre_del_proyecto_cine/       <-- Carpeta raíz del proyecto
|
|-- .venv/                          <-- (Creada automáticamente) Carpeta del entorno virtual.
|   |                                   Contiene las librerías de Python específicas para este proyecto.
|   |                                   (No se debe incluir en el control de versiones, ej. .gitignore).
|
|-- app.py                          <-- CORAZÓN DE LA API.
|   |                                   Contiene toda la lógica de la aplicación Flask:
|   |                                   - Inicialización de Flask.
|   |                                   - Configuración de SQLAlchemy y PyMongo.
|   |                                   - Definición de los modelos ORM de SQLAlchemy para las tablas SQL.
|   |                                   - Definición de todas las rutas (endpoints) de la API.
|   |                                   - Lógica para las operaciones CRUD y otras consultas.
|
|-- ProyectoCine.sql                <-- SCRIPT DE BASE DE DATOS SQL.
|   |                                   Contiene las sentencias DDL (Data Definition Language) para:
|   |                                   - Crear la base de datos proyectoCine.
|   |                                   - Crear todas las tablas (Pelicula, Sala, Cliente, Funcion, Boleto).
|   |                                   - Crear las vistas (VistaFunciones, IngresosPorPelicula).
|   |                                   - Crear el trigger (validar_capacidad).
|
|-- script.js                       <-- SCRIPT DE CONFIGURACIÓN DE MONGODB.
|   |   (o crear_mongo_proyecto_cine.js)    Contiene comandos para mongosh para:
|   |                                   - Crear colecciones (opcional, ya que se crean al primer insert).
|   |                                   - Opcionalmente, insertar datos de ejemplo iniciales.
|
|-- poblar_datos.py                 <-- (Opcional) SCRIPT DE GENERACIÓN DE DATOS.
|   |                                   Utiliza la librería Faker para insertar una gran cantidad
|   |                                   de datos de prueba en ambas bases de datos (MySQL y MongoDB).
|
|-- README.md                       <-- ESTE ARCHIVO.
|   |                                   Documentación principal del proyecto, explicando cómo
|   |                                   configurarlo, ejecutarlo y utilizarlo.
|
|-- (opcional) requirements.txt     <-- ARCHIVO DE DEPENDENCIAS.
|   |                                   Lista todas las librerías de Python necesarias para el proyecto
|   |                                   y sus versiones. Permite una fácil reinstalación de
|   |                                   dependencias en otros entornos (pip install -r requirements.txt).


---

## 🤔 Guía de Solución de Problemas Comunes (Troubleshooting)

Aquí hay algunos problemas comunes que podrías encontrar y sus posibles soluciones:

* **Error: `sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:mysql.mysqlclient`**
    * **Causa:** SQLAlchemy está intentando usar el driver `mysqlclient`, pero no está instalado o no se puede cargar correctamente.
    * **Solución 1:** Asegúrate de que `mysqlclient` esté instalado en tu entorno virtual (`pip install mysqlclient`). La instalación de `mysqlclient` puede ser complicada en algunos sistemas (especialmente Windows) porque puede requerir compiladores de C++ o librerías de desarrollo de MySQL.
    * **Solución 2 (Recomendada si la Solución 1 falla):** Cambia a `mysql-connector-python`.
        1.  Instálalo: `pip install mysql-connector-python`
        2.  Desinstala `mysqlclient` si lo intentaste instalar: `pip uninstall mysqlclient`
        3.  **Importante:** Modifica tu cadena de conexión en `app.py` de `mysql+mysqlclient://...` a `mysql+mysqlconnector://...`

* **Error: `(mysql.connector.errors.ProgrammingError) 1049 (42000): Unknown database 'proyectocine'`**
    * **Causa:** La API se conectó al servidor MySQL, pero la base de datos llamada `proyectocine` no existe en ese servidor.
    * **Solución:** Asegúrate de haber ejecutado `CREATE DATABASE proyectoCine;` en tu MySQL antes de intentar ejecutar la API o el script `ProyectoCine.sql`.

* **Error: `(mysql.connector.errors.ProgrammingError) 1146 (42S02): Table 'proyectocine.pelicula' doesn't exist` (o similar para otras tablas)**
    * **Causa:** La base de datos `proyectoCine` existe, pero la tabla específica (ej. `Pelicula`) no fue creada dentro de ella.
    * **Solución:** Asegúrate de haber ejecutado `USE proyectoCine;` en MySQL *antes* de ejecutar las sentencias `CREATE TABLE` de tu script `ProyectoCine.sql`. Vuelve a ejecutar la parte de creación de tablas de tu script.

* **Error: `sqlalchemy.exc.DataError: (...) Data too long for column 'nombre_columna' at row X`**
    * **Causa:** Estás intentando insertar un valor en una columna de MySQL que es más largo que el tamaño definido para esa columna (ej. un `VARCHAR(20)` intentando almacenar 30 caracteres).
    * **Solución 1:** Aumenta el tamaño de la columna en tu esquema MySQL usando `ALTER TABLE NombreTabla MODIFY COLUMN nombre_columna VARCHAR(nuevo_tamaño);`.
    * **Solución 2:** Modifica tu código (API o script de población) para que los datos generados o recibidos no excedan el límite de la columna (ej. acortando strings).

* **Errores de Conexión a MongoDB (ej. `ServerSelectionTimeoutError`)**
    * **Causa:** La API no puede conectarse a tu servidor MongoDB.
    * **Solución:**
        1.  Verifica que el servicio `mongod` (el demonio de MongoDB) esté efectivamente en ejecución en tu sistema.
        2.  Confirma que la `MONGO_URI` en `app.py` (usualmente `mongodb://localhost:27017/` para conexiones locales estándar) sea la correcta para tu configuración de MongoDB.
        3.  Revisa si hay algún firewall bloqueando la conexión al puerto 27017.

* **La API se inicia, pero los endpoints devuelven errores `500 Internal Server Error`**
    * **Causa:** Hay un error en la lógica de tu código Python dentro de la ruta que estás intentando acceder.
    * **Solución:** La **consola donde ejecutaste `python app.py` es tu mejor amiga**. Flask, especialmente en modo debug, imprimirá un "traceback" detallado del error, mostrando exactamente en qué línea de tu código Python ocurrió el problema y por qué. Lee este traceback cuidadosamente para diagnosticar y corregir el error.

* **Power BI no puede conectarse a la URL de la API o no muestra datos**
    * **Causa 1:** La API Flask no está en ejecución o no es accesible desde la máquina donde corre Power BI.
        * **Solución:** Asegúrate de que `python app.py` esté corriendo sin errores y que puedas acceder a la URL del endpoint desde un navegador en la misma máquina que Power BI.
    * **Causa 2:** La URL del endpoint en Power BI es incorrecta o tiene un error tipográfico.
        * **Solución:** Copia y pega la URL directamente desde una prueba exitosa en el navegador o Postman.
    * **Causa 3:** La API no está devolviendo JSON o Power BI no lo está interpretando correctamente.
        * **Solución:** Verifica que tus endpoints de Flask usen `jsonify()` para devolver datos. En Power BI, asegúrate de seguir los pasos para "Convertir en tabla" y "Expandir" las columnas de registros JSON.

---

## 👨‍💻 Autor(es) del Proyecto

* **<TU_NOMBRE_COMPLETO_AQUI>**
    * Email: `<TU_CORREO_ELECTRONICO_AQUI (opcional)>`
    * GitHub: `<TU_USUARIO_DE_GITHUB_AQUI (opcional)>`

*(Por favor, reemplaza los placeholders `<...>` con tu información personal).*

---
