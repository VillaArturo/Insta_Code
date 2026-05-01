import re

def limpiar_codigo(codigo):
    # quitar comentarios
    codigo = re.sub(r"'.*", "", codigo)

    # quitar líneas vacías
    codigo = "\n".join(
        [line for line in codigo.splitlines() if line.strip() != ""]
    )

    return codigo