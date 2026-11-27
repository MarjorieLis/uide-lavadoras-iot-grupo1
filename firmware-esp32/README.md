# Código del ESP32

`main.py` contiene el programa de MicroPython que utilizamos en la simulación de lavadoras compartidas. También está guardado en [`simulaciones/lavadora-wokwi/main.py`](../simulaciones/lavadora-wokwi/main.py).

## ¿Qué hace el programa?

- Se conecta al Wi-Fi simulado de Wokwi y a un broker MQTT de pruebas.
- Publica datos JSON con el identificador del nodo.
- Recibe autorizaciones y controla los estados de la lavadora simulada.
- Publica eventos de inicio y fin de lavado.
- Configura el mensaje **Last Will** para avisar si se pierde la conexión.

## Componentes utilizados

| Elemento | Conexión | Uso |
|---|---|---|
| Potenciómetro | GPIO34 | Representa la lectura de corriente |
| Botón verde | GPIO4 | Simula un pago autorizado |
| LED azul | GPIO2 | Representa la carga habilitada |

Los estados son `BLOQUEADA → HABILITADA → LAVANDO → FINALIZADA → BLOQUEADA`.

**[Abrir la simulación en Wokwi](https://wokwi.com/projects/481853051628154881)** · [Ver instrucciones para la prueba](../docs/pruebas/GUIA_GTA_S5.md)

Este código es para una simulación con LED de baja tensión. No controla una lavadora real y utiliza un broker público sin autenticación.
