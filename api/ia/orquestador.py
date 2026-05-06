import re
from api.ia.constructor_prompt import construir_prompt_conversion


class OrquestadorIA:
    def __init__(self, cliente_ia):
        self.cliente = cliente_ia

    def _limpiar_respuesta(self, respuesta: str) -> str:
        # Quitar BOM y espacios extremos
        respuesta = respuesta.strip().lstrip('\ufeff')

        # Eliminar bloques markdown: ```cpp, ```c++, ``` etc.
        respuesta = re.sub(r'^```[^\n]*\n?', '', respuesta, flags=re.MULTILINE)
        respuesta = re.sub(r'\n?```\s*$', '', respuesta, flags=re.MULTILINE)

        # Convertir links markdown [texto](url) → solo el texto plano
        # Soluciona: [file.is](http://file.is)_open() → file.is_open()
        # Soluciona: [localhost](http://localhost) → localhost
        respuesta = re.sub(r'\[([^\]\n]+)\]\(http[^\)]+\)', r'\1', respuesta)

        # Soluciona: << "\n (salto real) " → << "\n"
        # El LLM a veces parte un string con un salto de línea literal adentro
        respuesta = re.sub(r'(?<=")\n(?=")', r'\\n', respuesta)

        # Quitar líneas introductorias típicas del LLM
        lineas = respuesta.split('\n')
        lineas_filtradas = [
            l for l in lineas
            if not l.strip().lower().startswith((
                "here is", "here's", "the following",
                "below is", "this is", "sure", "certainly"
            ))
        ]

        return '\n'.join(lineas_filtradas).strip()

    def _validar_cpp(self, codigo: str) -> bool:
        señales = ['#include', 'int main', 'std::', 'void ', 'return ']
        return any(s in codigo for s in señales)

    def convertir_codigo(self, codigo_fuente, lenguaje="vb6"):
        prompt = construir_prompt_conversion(codigo_fuente, lenguaje)
        respuesta = self.cliente.generar(prompt)
        respuesta_limpia = self._limpiar_respuesta(respuesta)

        if not self._validar_cpp(respuesta_limpia):
            raise ValueError(
                f"La IA no devolvió C++ válido. Output recibido:\n{respuesta_limpia[:300]}"
            )

        return {
            "codigo_original": codigo_fuente,
            "codigo_convertido": respuesta_limpia
        }