# Lavadoras compartidas IoT — Grupo 1

**Universidad Internacional del Ecuador · Campus Loja · Tecnologías Emergentes**

**Integrantes:** Fabián Israel Campoverde Muñoz, Marjorie Lisseth Jiménez Jiménez y Cristina Lisbeth Orellana Esparza.

## ¿De qué trata nuestro proyecto?

En algunas viviendas estudiantiles, varias personas comparten una lavadora. Cuando no se lleva un registro de los usos, pueden surgir dudas sobre los turnos y los cobros. Estamos desarrollando un sistema IoT para autorizar cada lavado, identificar el inicio y el fin del ciclo y consultar esa información desde una plataforma web.

Para la demostración utilizamos un ESP32 simulado en Wokwi. El botón representa una autorización de pago de prueba, la perilla representa el consumo eléctrico y un LED indica que la carga está habilitada. No se realiza ningún cobro real ni se conecta una lavadora doméstica.

## ¿Qué hemos comprobado?

En la simulación de Wokwi y en la VM Ubuntu verificamos que:

- El ESP32 se conecta a Wi-Fi y al broker MQTT de pruebas.
- Envía datos JSON con un identificador de nodo.
- Pasa por los estados `BLOQUEADA`, `HABILITADA`, `LAVANDO` y `FINALIZADA`.
- Publica los eventos `autorizado`, `inicio` y `fin`.
- Cuando se detiene la simulación, el broker puede publicar `desconectado` mediante **Last Will**.

Estas pruebas corresponden al **nodo simulado**. La página web, la API y la base de datos se trabajan en sus carpetas como partes del sistema completo.

## Proyecto de Wokwi

**[Abrir la simulación de lavadoras compartidas](https://wokwi.com/projects/481853051628154881)**

Para ejecutarla, abre el enlace y presiona **Start Simulation**. Si deseas revisar el código, lo encontrarás en `simulaciones/lavadora-wokwi/main.py` y las conexiones en `simulaciones/lavadora-wokwi/diagram.json`.

### Cómo usar la simulación

1. Inicia Wokwi y comprueba que aparece `MQTT conectado` en la consola.
2. Presiona el botón verde **Pago de prueba**. El estado cambia a `HABILITADA` y se enciende el LED.
3. Gira la perilla hacia la derecha. Se simula consumo y aparece `LAVANDO`.
4. Gira la perilla hacia la izquierda. El sistema registra el fin y vuelve a `BLOQUEADA` después de unos segundos.
5. Para comprobar el **Last Will**, deja Ubuntu escuchando los mensajes y detén Wokwi mediante **Stop Simulation**.

### Ver los mensajes en Ubuntu

Con `mosquitto-clients` instalado, ejecuta:

```bash
date
mosquitto_sub -h broker.emqx.io -p 1883 -t 'uide/g1/marjorielis/lavadora01/#' -v
```

Aparecerán mensajes del estado de la lavadora, eventos y lecturas del sensor simulado. El identificador del dispositivo es `g1-marjorielis-lav01`.

También puedes enviar una autorización de prueba desde otra terminal mientras Wokwi esté funcionando y en estado `BLOQUEADA`:

```bash
mosquitto_pub -h broker.emqx.io -p 1883 \
  -t 'uide/g1/marjorielis/lavadora01/cmd' -q 1 \
  -m '{"accion":"habilitar","cmd_id":"CMD-G1-001"}'
```

Para repetir una autorización, cambia el `cmd_id` después de que el ciclo haya terminado.

**Nota sobre la conexión:** Wokwi y Ubuntu se conectan al mismo broker público `broker.emqx.io`. En esta prueba, el ESP32 **no se conecta directamente al Mosquitto local de la VM**.

## Archivos del repositorio

| Carpeta | Contenido |
|---|---|
| `docs/arquitectura/` | Diagramas editables, flujos y requisitos |
| `docs/decisiones-adr/` | Decisiones técnicas de la arquitectura |
| `docs/pruebas/` | Guía para repetir la demostración MQTT y Last Will |
| `simulaciones/lavadora-wokwi/` | Código y circuito de Wokwi |
| `firmware-esp32/` | Código MicroPython del nodo |
| `simulaciones/` | Casos de prueba y ejemplos de mensajes |
| `backend/` | Definición de las funciones y rutas del servidor |
| `frontend/` | Diseño de la pantalla web |

## Documentación útil

- [Contexto del sistema](docs/arquitectura/01_contexto.drawio)
- [Contenedores y comunicación](docs/arquitectura/02_contenedores.drawio)
- [Despliegue](docs/arquitectura/03_despliegue.drawio)
- [Flujos](docs/arquitectura/flujos.md)
- [Requisitos](docs/arquitectura/requisitos.md)
- [Decisiones de arquitectura](docs/decisiones-adr/)
- [Guía de pruebas GTA S5](docs/pruebas/GUIA_GTA_S5.md)

Los archivos `.drawio` pueden editarse gratis en [diagrams.net](https://app.diagrams.net/).

## Seguridad

El broker `broker.emqx.io:1883` es público y se utiliza **solo para las pruebas de clase**. No introducir contraseñas, datos personales ni información de pagos reales. En la arquitectura del sistema se contempla el uso de un Mosquitto propio con autenticación, permisos por tema y conexión cifrada. La demostración utiliza únicamente un LED de baja tensión: **no conectar el ESP32 directamente a una lavadora de 110/120 V**.
