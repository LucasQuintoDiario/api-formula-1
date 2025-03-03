from fastapi import FastAPI, HTTPException
import cohere
import uvicorn
from fastapi.responses import HTMLResponse
import os
import pandas as pd
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
import pymysql
import uuid
import datetime



host = os.getenv("BBDD_HOST")
username = os.getenv("BBDD_USERNAME")
password= os.getenv("BBDD_PASSWORD")
database= os.getenv("BBDD_NAME")
api_key_cohere = os.getenv("API_COHERE")
session_id = str(uuid.uuid4())

app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str

class ConversationRequest(BaseModel):
    id: str


@app.get("/", response_class=HTMLResponse)
async def home():
    return f"""
    <html>
        <head>
            <title>Bienvenido a la API de F1</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }}
                .container {{
                    text-align: center;
                    background-color: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    color: #2c3e50;
                }}
                p {{
                    color: #7f8c8d;
                    font-size: 18px;
                }}
                .session-id {{
                    font-weight: bold;
                    color: #e74c3c;
                }}
            </style>
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
    """

@app.post("/question/")
async def preguntar(request: PromptRequest):
    try:
        co = cohere.ClientV2(api_key=api_key_cohere)
        response = co.chat(
            model="command-r-plus-08-2024",
            messages=[
                {"role": "system", "content": "Eres un experto en Fórmula 1 y explicas conceptos de forma clara, breve y sencilla para personas sin conocimientos previos. Usa un tono amigable y directo, evitando tecnicismos complejos. Responde en pocas frases, centrándote en lo esencial."},
                {"role": "user", "content": request.prompt}
            ],
        )


        db = pymysql.connect(host = host,
                     user = username,
                     password = password,
                     cursorclass = pymysql.cursors.DictCursor
)
        cursor = db.cursor()
        use_db = ''' USE formula_1'''
        cursor.execute(use_db)
        query = "INSERT INTO interactions (question, response, session_id, timestamp) VALUES (%s, %s, %s, %s)"
        current_timestamp = datetime.datetime.now()
        current_timestamp = current_timestamp.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(query, (request.prompt, response.message.content[0].text, session_id, current_timestamp))
        db.commit()
        cursor.close()
        db.close()

        return response.message.content[0].text
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=str("No se ha podido completar la consulta"))


@app.get("/getid/")
async def get_id():
    try:
        return session_id
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=str("No se ha podido generar el ID."))

@app.post("/consult/")
async def consulta(history: ConversationRequest):
    try:    
        history.id
        query = f"SELECT * FROM interactions WHERE session_id = '{history.id}'"
        db = pymysql.connect(host = host,
                        user = username,
                        password = password,
                        cursorclass = pymysql.cursors.DictCursor
    )
        cursor = db.cursor()
        use_db = ''' USE formula_1'''
        cursor.execute(use_db)
        cursor.execute(query)
        historial = cursor.fetchall()
        cursor.close()
        db.close()
        return historial
    
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Error al recuperar el historial")



@app.delete("/delete_history/")
async def delete_history(history: ConversationRequest):
    try:
        db = pymysql.connect(host=host,
                             user=username,
                             password=password,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        use_db = "USE formula_1"
        cursor.execute(use_db)
        
        query = f"DELETE FROM interactions WHERE session_id = '{history.id}'"
        cursor.execute(query)
        db.commit()
        
        rows_affected = cursor.rowcount
        cursor.close()
        db.close()
        
        if rows_affected == 0:
            raise HTTPException(status_code=404, detail="No se encontró historial para este ID de sesión")
        
        return {"message": "Historial eliminado correctamente"}
    
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Error al eliminar el historial")


if __name__ == "__main__":
    uvicorn.run("my_app:app", host="0.0.0.0", port=8000, reload=True)