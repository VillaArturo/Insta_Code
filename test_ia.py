# 1. Importas las piezas
from api.Servicios.cliente_gemini import ClienteGemini
from api.ia.orquestador import OrquestadorIA

# 2. Creas el servicio (La conexión a internet)
servicio_ia = ClienteGemini()

# 3. Creas el orquestador y LE PASAS el servicio (Inyección de dependencia)
# Así el orquestador tiene el 'self.cliente' listo para usar
orquestador = OrquestadorIA(servicio_ia)

# 4. Ejecutas la acción
resultado = orquestador.convertir_codigo("Esto es una preuba, dar un 'afirmativo' si recibes este mensaje")

print(resultado)