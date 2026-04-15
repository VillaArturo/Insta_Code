from google import genai
from google.genai import types
import os

API_KEY = "AQ.Ab8RN6L5lr1mcLdmpOAFy4ulqrjrEpTpua9cgv90s7SLR1OiDQ"
client = genai.Client(api_key=API_KEY)


response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Estoy mandando esta solicitud por API, quiero saber cuales son las limitantes que poseo con relacion a la cuota gratuita de API gemini. Es el modelo gemini-2.5-flash"
)

print(response.text)