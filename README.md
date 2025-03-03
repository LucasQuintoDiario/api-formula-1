
# API Fórmula 1

Este proyecto es una API basada en **FastAPI** que responde a preguntas sobre **Fórmula 1**. Utiliza la API de **Cohere** para generar respuestas a partir de las preguntas de los usuarios. Además, la información de las interacciones se guarda en una base de datos MySQL alojada en AWS.

## Estructura del Proyecto

Este repositorio contiene los siguientes archivos:

- **`app_streamlit.py`**: Aplicación de **Streamlit** que se conecta a la API para visualizar la información de manera interactiva.
- **`create_DB.py`**: Script que crea la base de datos MySQL en el servidor especificado en las variables de entorno.
- **`Dockerfile`**: Archivo que define la configuración del contenedor Docker, incluyendo los pasos para instalar dependencias, ejecutar el script `create_DB.py` y ejecutar tanto la API como la aplicación de Streamlit.
- **`my_app.py`**: Archivo que contiene la implementación de la API utilizando **FastAPI**.
- **`requirements.txt`**: Archivo con las dependencias necesarias para ejecutar el proyecto.
- **`.env`**: Archivo de configuración de variables de entorno, que incluye claves de la API de Cohere y las credenciales de la base de datos.
- **`README.md`**: Este archivo con la documentación del proyecto.
- **`.dockerignore`**: Archivo para especificar qué archivos y carpetas deben ser ignorados al construir la imagen de Docker (como los archivos sensibles y no necesarios).

## Variables de Entorno

El proyecto requiere algunas variables de entorno que debes configurar en tu entorno o en un archivo `.env` para que funcione correctamente:

- **`API_COHERE`**: Tu clave de API de Cohere para generar respuestas automáticas.
- **`BBDD_PASSWORD`**: La contraseña para acceder a la base de datos MySQL.
- **`BBDD_HOST`**: La dirección IP o el nombre del host del servidor de base de datos.
- **`BBDD_USERNAME`**: El nombre de usuario para acceder a la base de datos MySQL.
- **`BBDD_NAME`**: El nombre de la base de datos que será utilizada por la API.

### Ejemplo de archivo `.env`:

```env
API_COHERE=tu_clave_api_cohere
BBDD_PASSWORD=tu_contraseña
BBDD_HOST=tu_host
BBDD_USERNAME=tu_usuario
BBDD_NAME=tu_base_de_datos
```



## Instrucciones para Probar el Proyecto

### 1. Clonar el repositorio

Primero, clona el repositorio en tu máquina local:

```bash
git clone https://github.com/tu_usuario/API_F1.git
cd API_F1
```

### 2. Crear las variables de entorno

Crea un archivo `.env` en la raíz del proyecto y agrega las variables de entorno necesarias para que el proyecto funcione correctamente.

```bash
touch .env
```

Luego, agrega las variables de entorno en el archivo `.env`:

```env
API_COHERE=tu_clave_api_cohere
BBDD_PASSWORD=tu_contraseña
BBDD_HOST=tu_host
BBDD_USERNAME=tu_usuario
BBDD_NAME=tu_base_de_datos
```

### 3. Construir la imagen de Docker

Asegúrate de tener Docker instalado en tu máquina. Luego, construye la imagen de Docker con el siguiente comando:

```bash
docker build -t lucasquintodiario/f1-api:latest .
```

### 4. Ejecutar el contenedor de Docker

Una vez construida la imagen, puedes ejecutar el contenedor. Asegúrate de que Docker esté corriendo en tu sistema, y luego ejecuta:

```bash
docker run --env-file .env -p 8000:8000 -p 8501:8501 lucasquintodiario/f1-api:latest
```

Esto expondrá la API en el puerto 8000 y la aplicación de **Streamlit** en el puerto 8501. Las variables de entorno se cargarán desde el archivo `.env`.

### 5. Acceder a la API

Una vez que el contenedor esté corriendo, podrás interactuar con la API en:

- **API**: `http://localhost:8000/`
- **Streamlit App**: `http://localhost:8501/`

### 6. Consultar la API

Para interactuar con la API, puedes enviar preguntas como:

```json
{
  "prompt": "¿Quién ganó el campeonato de F1 en 2023?"
}
```

La API devolverá una respuesta generada por **Cohere** basada en la pregunta enviada.

### 7. Detener el contenedor

Para detener el contenedor una vez que hayas terminado, puedes usar:

```bash
docker stop <container_id>
```

---

## Endpoints de la API

### 1. **`GET /`**

Este endpoint muestra una página de bienvenida con un mensaje sobre la API de F1 y muestra el ID de sesión único generado para el usuario.

**Respuesta:**
```html
<html>
    <head>
        <title>Bienvenido a la API de F1</title>
        ...
    </head>
    <body>
        <div class="container">
            <h1>¡Bienvenido a la API de F1!</h1>
            <p>¿Cuál es tu duda sobre F1?</p>
            <p>Tu ID de sesión único es: <span class="session-id">{session_id}</span></p>
            <p>Utiliza este ID para consultar o eliminar tu historial de conversaciones cuando lo desees.</p>
        </div>
    </body>
</html>
```

### 2. **`POST /question/`**

Este endpoint recibe una pregunta sobre Fórmula 1 y genera una respuesta utilizando la API de Cohere. Además, guarda la pregunta, la respuesta generada y el ID de sesión en la base de datos.

**Entrada:**
```json
{
  "prompt": "¿Quién ganó el campeonato de F1 en 2023?"
}
```

**Respuesta:**
```json
"Max Verstappen ganó el campeonato de F1 en 2023."
```

### 3. **`GET /getid/`**

Este endpoint devuelve el ID de sesión único que puede ser utilizado para consultar o eliminar el historial de conversaciones del usuario.

**Respuesta:**
```json
"12345-67890"
```

### 4. **`POST /consult/`**

Este endpoint recibe un ID de sesión y devuelve el historial de interacciones (preguntas y respuestas) almacenado para ese ID en la base de datos.

**Entrada:**
```json
{
  "id": "12345-67890"
}
```

**Respuesta:**
```json
[
  {
    "question": "¿Quién ganó el campeonato de F1 en 2023?",
    "response": "Max Verstappen ganó el campeonato de F1 en 2023.",
    "session_id": "12345-67890",
    "timestamp": "2023-03-01 12:34:56"
  }
]
```

### 5. **`DELETE /delete_history/`**

Este endpoint permite eliminar el historial de interacciones asociado a un ID de sesión. Si no se encuentra historial para el ID proporcionado, se devuelve un error.

**Entrada:**
```json
{
  "id": "12345-67890"
}
```

**Respuesta:**
```json
{
  "message": "Historial eliminado correctamente"
}
```

## Licencia

Este proyecto está licenciado bajo la **MIT License**. Puedes ver más detalles en el archivo `LICENSE`.
