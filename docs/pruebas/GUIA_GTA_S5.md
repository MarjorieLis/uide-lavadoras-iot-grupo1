# GTA S5 - Demostración MQTT y Last Will

## Objetivo

Mostrar en clase que un ESP32 simulado en Wokwi publica mensajes JSON con identificador de nodo y que la VM Ubuntu recibe su mensaje `desconectado` cuando la simulación se detiene de forma inesperada.

## Preparación

1. Entra al [proyecto de lavadoras compartidas en Wokwi](https://wokwi.com/projects/481853051628154881).
2. Verifica que estén el ESP32, la perilla, el botón de autorización y el LED.
3. En tu VM Ubuntu, comprueba que está instalado `mosquitto-clients` (`mosquitto_sub --help`).

## Prueba 1: recibir la telemetría (captura 1)

En la VM ejecuta:

```bash
date
mosquitto_sub -h broker.emqx.io -p 1883 -t 'uide/g1/marjorielis/lavadora01/#' -v
```

Luego inicia Wokwi. Espera a que aparezcan mensajes de los temas `telemetria` y `estado`. Toma una captura donde se vean **tu usuario@hostname, `date`, los temas y los JSON**. Toma otra de la consola Wokwi.

## Prueba 2: simular el lavado (captura 2)

Con Wokwi funcionando, presiona el botón verde. El LED se encenderá y se publicará `HABILITADA`. Gira la perilla hacia el valor alto: debe publicarse `inicio` y cambiar a `LAVANDO`. Luego baja la perilla para que se publique `fin` y pase a `FINALIZADA`.

En la VM aparecerán los eventos con `ciclo_id` y `event_id`. Toma una captura de ellos.

## Prueba 3: enviar una orden desde Ubuntu (captura 3)

Con la lavadora en `BLOQUEADA`, abre una segunda terminal y publica:

```bash
date
mosquitto_pub -h broker.emqx.io -p 1883 \
  -t 'uide/g1/marjorielis/lavadora01/cmd' -q 1 \
  -m '{"accion":"habilitar","cmd_id":"CMD-G1-001"}'
```

En la primera terminal debe aparecer el cambio a `HABILITADA`. Si repites **el mismo `cmd_id`**, la lógica del nodo lo rechazará. Para una nueva autorización, cambia el identificador después de que el ciclo haya regresado a `BLOQUEADA`.

## Prueba 4: Last Will con Wokwi detenido (captura 4)

1. Deja la VM escuchando el tema `uide/g1/marjorielis/lavadora01/estado`:

   ```bash
   date
   mosquitto_sub -h broker.emqx.io -p 1883 -t 'uide/g1/marjorielis/lavadora01/estado' -F '%I %t %p'
   ```

2. Inicia Wokwi y comprueba que el nodo ha publicado un estado.
3. En Wokwi pulsa **Stop Simulation**, **sin hacer una desconexión MQTT normal**.
4. Deja la terminal de Ubuntu abierta y observa cuándo aparece `desconectado`.
5. Anota la hora del último mensaje y la del `desconectado`. Esas horas permitirán describir el tiempo observado.

**Importante:** los tiempos de Last Will dependen del broker y de la conexión, por lo que no deben escribirse como un resultado fijo si no se han medido. Si no aparece `desconectado` inmediatamente, espera hasta que el broker detecte la pérdida de conexión. Con `keepalive=15`, el límite de referencia ronda 22,5 s en ausencia de tráfico, aunque en la práctica puede variar.

## Errores comunes

- **`Could not resolve host` en Ubuntu:** revisar conexión y DNS de la VM.
- **`Connection refused` al broker público:** revisar conectividad y que se permita la salida TCP al puerto 1883.
- **`ImportError: umqtt` en Wokwi:** utilizar el proyecto nuevo de MicroPython ESP32; la demostración oficial de Wokwi utiliza `from umqtt.simple import MQTTClient`.
- **No llegan mensajes a la VM:** confirmar que Wokwi y Ubuntu usan el mismo broker `broker.emqx.io` y el mismo prefijo de temas.
- **No aparece Last Will:** detener Wokwi desde Stop Simulation, no ejecutar `client.disconnect()`; comprobar que la consola muestra la conexión MQTT antes de detener.
- **El LED no cambia:** el LED se enciende únicamente cuando el estado es `HABILITADA` o `LAVANDO`. En `FINALIZADA` y `BLOQUEADA` se apaga.

## Seguridad

El broker utilizado para las pruebas (`broker.emqx.io:1883`) es público, no exige credenciales y no cifra el tráfico. No incluir datos personales, contraseñas, pagos reales ni controlar aparatos de corriente de red. La instalación real seguirá lo documentado en los ADR del grupo (Mosquitto propio, TLS, usuario y permisos por temas).

## Referencias técnicas

- Wokwi: https://docs.wokwi.com/guides/esp32-wifi
- Wokwi (proyecto de ejemplo MQTT): https://wokwi.com/projects/322577683855704658
- MicroPython MQTT: https://github.com/micropython/micropython-lib/tree/master/micropython/umqtt.simple
- Mosquitto sub: https://mosquitto.org/man/mosquitto_sub-1.html
- EMQX, broker público: https://www.emqx.com/en/mqtt/public-mqtt5-broker
