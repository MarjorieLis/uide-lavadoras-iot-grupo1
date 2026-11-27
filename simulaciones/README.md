# Simulaciones de las lavadoras compartidas

En esta carpeta guardamos las pruebas que utilizamos para comprobar el funcionamiento del nodo IoT.

**[Proyecto de lavadoras en Wokwi](https://wokwi.com/projects/481853051628154881)**

## Archivos

- [`lavadora-wokwi/`](lavadora-wokwi/): circuito y código que ejecutamos en Wokwi.
- `escenarios.csv`: lista de situaciones que sirven para revisar el comportamiento del sistema.
- `payloads-ejemplo.json`: ejemplos de mensajes JSON utilizados como referencia.

## ¿Qué probamos?

Con el ESP32 simulado comprobamos la publicación de JSON, la autorización mediante el botón, el inicio y fin de lavado con la perilla y el mensaje `desconectado` al detener la simulación.

Para recibir los mensajes en Ubuntu, ejecuta:

```bash
mosquitto_sub -h broker.emqx.io -p 1883 -t 'uide/g1/marjorielis/lavadora01/#' -v
```

Wokwi y Ubuntu utilizan el mismo broker público de pruebas. La [guía paso a paso](../docs/pruebas/GUIA_GTA_S5.md) incluye los comandos y las capturas recomendadas.
