def preparar_contexto(data):
    contexto = "VB6 Code Structure:\n\n"

    contexto += f"Funciones encontradas: {len(data['funciones'])}\n"
    contexto += f"Subs encontrados: {len(data['subs'])}\n\n"

    contexto += "Código:\n"
    contexto += data["raw"]

    return contexto