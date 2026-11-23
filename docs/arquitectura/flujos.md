# Tabla de flujos — GTA S4

**Criterio:** la flecha de red representa quién inicia la conexión. Para la integración se utiliza MQTT con TLS por el puerto 8883; las prácticas anteriores con el puerto 1883 sirvieron para conocer el broker y el protocolo.

| # | Origen → destino | Protocolo / puerto | Opciones de seguridad | Frecuencia | Si se cae: detección y respuesta |
|---|---|---|---|---|---|
| F0 | Sensor → ESP32 → salida | ADC / GPIO, sin puerto | Control local, estado seguro | Lectura periódica del sensor | Si el sensor falla, no confirmar el fin del ciclo. Si la salida falla, suspender nuevas autorizaciones y registrar incidencia. |
| F1 | Navegador → Nginx → API | HTTPS / TCP 443 | Sesión autorizada; validación de solicitud y pago de prueba | Al solicitar o confirmar uso | Si no responde la API: mostrar error; no generar comando. Reintentar usando el mismo ID de solicitud. |
| F2 | API → SQLite | Acceso local, sin puerto TCP | Transacción e IDs únicos; acceso del proceso | Por reserva, pago y ciclo | Si no se puede guardar, marcar operación pendiente y **no** publicar autorización. |
| F3 | Cliente API → Mosquitto | MQTTS / TCP 8883 | QoS 1; no retenido; TLS; ACL `/cmd`; `cmd_id` único y vigencia | Por autorización válida; incluye parámetros de configuración de esa sesión | Si cae el broker, dejar comando pendiente y no habilitar carga. Si se reenvía, conservar el mismo `cmd_id`. |
| F4 | Cliente ESP32 → Mosquitto | MQTTS / TCP 8883 | SUBSCRIBE `/cmd`, QoS 1; credencial de dispositivo, ACL | Al iniciar o reconectar | Si no hay conexión, no aceptar nuevas órdenes; seguir política de control local para sesiones ya iniciadas. |
| F5 | Cliente ESP32 → Mosquitto | MQTTS / TCP 8883 | PUBLISH `/evento`, QoS 1; `event_id`; sin retenido | Al iniciar/finalizar un ciclo | Ante red caída, conservar evento solo si existe cola persistente; reenviar sin cambiar `event_id`. Sin memoria persistente puede perderse. |
| F6 | Cliente ESP32 → Mosquitto | MQTTS / TCP 8883 | PUBLISH `/estado`, QoS 1, retenido y Last Will retenido | Conexión, cambios y desconexión abrupta | Broker detecta pérdida de sesión y publica Will cuando corresponde. Si broker cae, estado del panel puede quedar desactualizado. |
| F7 | Cliente worker API → Mosquitto | MQTTS / TCP 8883 | SUBSCRIBE `/evento`, QoS 1, TLS, ACL; deduplicar | Continuo; procesar al llegar evento | Si cae el worker, deja de registrar; al volver recuperar lo que permita la sesión/cola y marcar huecos no recuperables. |
| F8 | Cliente Node-RED → Mosquitto | MQTTS / TCP 8883 | SUBSCRIBE `/estado`, QoS 1, TLS, ACL de lectura | Continuo | Si no llega actualización, mostrar dato antiguo y hora; no afirmar que el nodo sigue conectado. |
| F9 | Navegador → Nginx → Node-RED | HTTPS / TCP 443 | Autenticación y acceso de solo lectura | Al consultar panel | Si falla panel o proxy, no hay visualización; el control local de un ciclo en curso no depende del navegador. |

## Temas MQTT del sistema

```text
loja/lavadora/casa01/lav01/cmd       # servidor publica; ESP32 se suscribe
loja/lavadora/casa01/lav01/evento    # ESP32 publica; backend se suscribe
loja/lavadora/casa01/lav01/estado    # ESP32 + Last Will publican; panel se suscribe
```

Los valores configurables de **una sesión** (por ejemplo `minutos_max`) pueden incluirse en F3. Los parámetros de cada autorización (por ejemplo, `minutos_max`) viajan con el comando F3. Los parámetros permanentes del equipo se documentarán en un flujo independiente cuando se incorporen.

## Criterios para las pruebas de integración

- QoS 1 no garantiza ejecución única: deduplicar `cmd_id` y `event_id` en la aplicación.
- Un mensaje retenido no reemplaza al historial de eventos de base de datos.
- Last Will depende de que el broker siga disponible y detecte la pérdida de conexión.
- La recuperación de eventos desconectados requiere memoria y manejo de colas reales en el nodo.
