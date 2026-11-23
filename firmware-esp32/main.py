"""Plantilla educativa de la máquina de estados; SIN hardware ni MQTT.

Este archivo NO acciona relés ni autoriza lavadoras reales.
"""

ESTADOS = ("BLOQUEADA", "HABILITADA", "LAVANDO", "FINALIZADA")
estado = "BLOQUEADA"
ultimo_cmd_id = None


def autorizar(cmd_id, autorizado):
    global estado, ultimo_cmd_id
    if not autorizado or estado != "BLOQUEADA" or cmd_id == ultimo_cmd_id:
        return False
    ultimo_cmd_id = cmd_id
    estado = "HABILITADA"
    return True


def actualizar_ciclo(actividad_detectada, fin_validado=False):
    global estado
    if estado == "HABILITADA" and actividad_detectada:
        estado = "LAVANDO"
    elif estado == "LAVANDO" and fin_validado:
        estado = "FINALIZADA"
    return estado


def bloquear():
    global estado
    estado = "BLOQUEADA"


# Demostración en consola: sustituir por pruebas y hardware seguro.
print("Estado inicial:", estado)
print("Autorización de ejemplo:", autorizar("CMD-DEMO-01", True))
print("Estado:", estado)
print("Inicio simulado:", actualizar_ciclo(True))
print("Final simulado:", actualizar_ciclo(False, fin_validado=True))
print("Nota: sin conexión MQTT ni control eléctrico")
