# Backend — planificación y contrato inicial

Esta carpeta contiene el **contrato de la API** para conectar la aplicación web con el servidor. La estructura de trabajo utiliza Python, FastAPI, SQLite y un cliente MQTT para comunicarse con Mosquitto.

## Funciones previstas

1. Crear solicitud de uso con `solicitud_id` único.
2. Confirmar **pago en modo de prueba** y guardar el resultado.
3. Publicar un comando MQTT solamente si el pago de prueba es válido y fue registrado.
4. Recibir eventos del ESP32 y evitar duplicados mediante `event_id`.
5. Permitir consultar estado e historial de ciclos.

Revisar `api.yaml` para las rutas de la API y `../docs/arquitectura/flujos.md` para F1, F2, F3 y F7.

**Desarrollo:** autenticación, datos, manejo de errores, conexión MQTT y pruebas de integración.
