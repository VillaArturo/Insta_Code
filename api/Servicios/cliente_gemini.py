import os
from google import genai
from dotenv import load_dotenv

class ClienteGemini:
    def __init__(self):
        # Carga las variables del archivo .env en el sistema
        load_dotenv()
        
        # Busca la variable por su nombre
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("❌ No se encontró GEMINI_API_KEY en el archivo .env")
            
        self.cliente = genai.Client(api_key=self.api_key)
        print("DEBUG: Cliente inicializado con llave protegida.")

    def generar(self, prompt):
        # Tu lógica de generación se mantiene igual...
        try:
            respuesta = self.cliente.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return respuesta.text
        except Exception as e:
            return f"Error en Gemini: {str(e)}"