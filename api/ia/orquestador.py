from api.ia.constructor_prompt import construir_prompt_conversion

class OrquestadorIA:
    def __init__(self, cliente_ia):
        # Aquí inyectamos el servicio de Gemini
        self.cliente = cliente_ia

    def convertir_codigo(self, codigo_fuente, lenguaje="vb6"):
        # 1. Llamamos a la herramienta de prompt
        prompt = construir_prompt_conversion(codigo_fuente, lenguaje)
        
        # 2. Usamos el servicio guardado en self
        respuesta = self.cliente.generar(prompt)
        
        # 3. Devolvemos la estructura de datos
        return {
            "codigo_original": codigo_fuente,
            "codigo_convertido": respuesta
        }