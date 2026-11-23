# ADR-001 — Mensajería entre el servidor y el ESP32

- **Estado:** Definido para la Fase I; implementación en desarrollo.
- **Fecha de elaboración:** 22 de noviembre de 2026.
- **Requisitos relacionados:** R-L01, R-L02, R-L03 y R-L04 (ver `../arquitectura/requisitos.md`).

## Contexto

La plataforma deberá enviar autorizaciones y recibir los eventos de inicio y fin de lavado. No queremos que el ESP32 tenga que consultar constantemente al servidor. Además, debemos detectar desconexiones y proteger las credenciales.

## Alternativas consideradas

1. **HTTP periódico:** sencillo al principio, pero el dispositivo necesita consultar repetidamente si hay una orden.
2. **MQTT sin cifrado (1883):** ya se practicó en la VM, pero no protege el tráfico frente a observadores de la red.
3. **MQTT con TLS (8883), usuarios y ACL:** requiere configuración adicional, pero permite mensajería bidireccional y protección del canal.

## Decisión

Se utiliza **MQTTS por el puerto 8883** como protocolo elegido para la integración entre el ESP32, la API y Mosquitto. El servidor publicará `/cmd` con QoS 1, sin retención y con `cmd_id` único y vencimiento. El ESP32 publicará eventos en `/evento` con QoS 1 y un `event_id`. El tema `/estado` será retenido, y se configurará Last Will para informar una desconexión inesperada. Cada cliente tendrá permisos mínimos por tema.

## Consecuencias

- **A favor:** reduce las consultas repetidas; separa órdenes, eventos y estado; facilita detectar desconexiones.
- **En contra:** habrá que configurar certificados y ACL; el broker es una dependencia; QoS 1 puede entregar duplicados y por eso hace falta reconocer identificadores ya procesados.
- **Pruebas de integración:** conexión MQTTS desde el ESP32, control de mensajes repetidos, vencimiento de órdenes y recuperación tras una caída del broker.
