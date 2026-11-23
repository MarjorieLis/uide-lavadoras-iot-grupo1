# Firmware ESP32 — plantilla de estados

`main.py` muestra de forma **sencilla** los estados de funcionamiento del ESP32. Las conexiones con el sensor, el relé y MQTT se incorporan en el desarrollo del firmware.

Componentes del firmware:

- Lectura y calibración del sensor de corriente (SCT-013 requiere acondicionamiento apropiado).
- Wi-Fi y MQTTS con certificado validado, credenciales seguras y ACL.
- Identificar comandos con `cmd_id` y rechazar duplicados/expirados.
- Publicar eventos con `event_id` estable; gestionar reconexión y Last Will.
- Validar el estado seguro de la salida al reiniciar.

Toda prueba de actuadores debe comenzar con **baja tensión**. No conectar la placa directamente a una lavadora de red.
