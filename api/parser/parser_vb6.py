import re

def parsear_vb6(codigo):
    funciones = re.findall(
        r'(Function\s+\w+.*?End Function)',
        codigo,
        re.DOTALL | re.IGNORECASE
    )

    subs = re.findall(
        r'(Sub\s+\w+.*?End Sub)',
        codigo,
        re.DOTALL | re.IGNORECASE
    )

    return {
        "funciones": funciones,
        "subs": subs,
        "raw": codigo
    }