
#Preparracion del prompt para la llamada con la IA
def construir_prompt_conversion(codigo_fuente, lenguaje):

    prompt_sistema = """
You are a senior software engineer specialized in legacy system migration.

Convert legacy code into modern C++ (C++17+).

Rules:
- Preserve logic
- Return only code
"""

    return f"""
{prompt_sistema}

Source language: {lenguaje}

Code:
{codigo_fuente}
"""