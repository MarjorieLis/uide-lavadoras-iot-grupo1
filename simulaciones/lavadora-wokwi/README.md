# Lavadora compartida en Wokwi

En esta carpeta se encuentran los dos archivos que utiliza el circuito:

- `diagram.json`: conexiones del ESP32, el botón verde, la perilla y el LED azul.
- `main.py`: programa de MicroPython que controla los estados y envía datos por MQTT.

**[Abrir el proyecto guardado en Wokwi](https://wokwi.com/projects/481853051628154881)**

## Cómo hacer la prueba

1. Abre el enlace y presiona **Start Simulation**.
2. Comprueba en la consola que el ESP32 se conectó a Wi-Fi y al broker MQTT.
3. Presiona el botón verde para autorizar un lavado de prueba. Se encenderá el LED.
4. Gira la perilla hacia la derecha para simular consumo. El sistema cambiará a `LAVANDO`.
5. Gira la perilla hacia la izquierda para terminar el ciclo.
6. Detén la simulación con **Stop** para comprobar el aviso de desconexión (*Last Will*) en Ubuntu.

## Ver los mensajes en Ubuntu

```bash
date
mosquitto_sub -h broker.emqx.io -p 1883 -t 'uide/g1/marjorielis/lavadora01/#' -v
```

Los mensajes salen por los temas `estado`, `evento` y `telemetria`. Cada uno incluye el identificador `g1-marjorielis-lav01`.

Esta es una simulación de clase: usa un broker público y un LED de baja tensión, sin cobros reales ni conexión eléctrica a una lavadora doméstica. Consulta la [guía completa de la GTA S5](../../docs/pruebas/GUIA_GTA_S5.md).
