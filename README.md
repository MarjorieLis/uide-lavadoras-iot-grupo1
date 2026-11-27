# Sistema IoT para la gestión de lavadoras compartidas

Proyecto de **Tecnologías Emergentes – UIDE Loja**, Grupo 1.  
**Integrantes:** Fabián Israel Campoverde Muñoz, Marjorie Lisseth Jiménez Jiménez y Cristina Lisbeth Orellana Esparza.

## ¿Qué problema aborda?

En viviendas de arriendo estudiantil una misma lavadora puede ser utilizada por varias personas. Nuestro sistema organiza las autorizaciones de uso y permite registrar los ciclos para que los estudiantes y el arrendador puedan consultar el estado y el historial.

## ¿Cómo funciona?

El estudiante solicita un uso desde la aplicación web. El servidor confirma un **pago de prueba** y envía una orden por MQTT al ESP32, que representa la habilitación de la lavadora con un LED de baja tensión. Un sensor simulado permite detectar el inicio y el fin de un ciclo. Los mensajes contienen un identificador del nodo.

> **Seguridad:** las pruebas usan un LED y una perilla, nunca una lavadora conectada a 110/120 V. No se procesan cobros reales.

## Organización

| Carpeta | Contenido |
|---|---|
| `docs/arquitectura/` | Diagramas Draw.io, flujos y requisitos |
| `docs/decisiones-adr/` | Decisiones de arquitectura |
| `docs/pruebas/` | Guía de la demostración MQTT y Last Will |
| `firmware-esp32/` | Código MicroPython del nodo de prueba |
| `simulaciones/lavadora-wokwi/` | Archivos `main.py` y `diagram.json` para Wokwi |
| `simulaciones/` | Escenarios y mensajes de ejemplo |
| `backend/` | Contrato inicial de API y documentación del servidor |
| `frontend/` | Página de referencia |

## Ejecutar el nodo en Wokwi (prueba GTA S5)

1. Abre el [proyecto guardado en Wokwi](https://wokwi.com/projects/481853051628154881).
2. Si necesitas reconstruirlo, copia el contenido de [`simulaciones/lavadora-wokwi/main.py`](simulaciones/lavadora-wokwi/main.py) y [`simulaciones/lavadora-wokwi/diagram.json`](simulaciones/lavadora-wokwi/diagram.json) en un nuevo ESP32 MicroPython.
3. Presiona **Start Simulation**. El ESP32 se conectará a `Wokwi-GUEST`, y después al broker de pruebas `broker.emqx.io`.
4. La consola mostrará mensajes JSON con el identificador `g1-marjorielis-lav01`.
5. El botón verde representa **confirmar un pago de prueba**; después puedes girar la perilla para simular el consumo del ciclo. El LED muestra la carga habilitada.

**Proyecto de lavadoras en Wokwi:** https://wokwi.com/projects/481853051628154881

### Ver los mensajes desde Ubuntu

En una terminal de la VM, ejecuta:

```bash
date
mosquitto_sub -h broker.emqx.io -p 1883 -t 'uide/g1/marjorielis/lavadora01/#' -v
```

Cuando ejecutes Wokwi verás `telemetria` cada 5 segundos, además de `estado` y `evento` cuando cambie la simulación.

### Probar una orden MQTT desde la VM

Con Wokwi ejecutándose, abre otra terminal y escribe:

```bash
date
mosquitto_pub -h broker.emqx.io -p 1883 \
  -t 'uide/g1/marjorielis/lavadora01/cmd' -q 1 \
  -m '{"accion":"habilitar","cmd_id":"CMD-PRUEBA-001"}'
```

Usa un `cmd_id` diferente si vas a repetir la prueba, por ejemplo `CMD-PRUEBA-002`. La orden no representa un cobro real ni controla un electrodoméstico.

### Demostrar el Last Will en vivo

1. Deja `mosquitto_sub` escuchando en Ubuntu y comprueba que el nodo publique JSON.
2. **Detén la simulación con Stop** en Wokwi, sin enviar `DISCONNECT` desde el firmware.
3. Tras detectar la pérdida de conexión, el broker enviará al tema `.../estado` este mensaje:

```json
{"nodo":"g1-marjorielis-lav01","estado":"desconectado"}
```

La publicación está configurada con **QoS 1** y como **retenida** (`retain=True`). Con `keepalive=15`, el broker suele detectar la pérdida en unos segundos o decenas de segundos; el tiempo exacto se debe medir en la VM.

**Importante:** el broker público de EMQX es solo para pruebas, sin autenticación ni privacidad. No subir contraseñas ni datos personales. Para la instalación real, la arquitectura del grupo usa Mosquitto con usuarios, ACL y TLS (puerto 8883).

La versión gratuita de Wokwi usa una puerta de enlace pública, que **no puede acceder directamente a la VM local**. Por eso, en esta demostración, la VM escucha el *mismo broker de pruebas* al que se conecta Wokwi, en lugar de usar `localhost`. [Documentación oficial de Wokwi](https://docs.wokwi.com/guides/esp32-wifi).

## Documentación de la Fase I

- [Vista de contexto](docs/arquitectura/01_contexto.drawio)
- [Vista de contenedores](docs/arquitectura/02_contenedores.drawio)
- [Vista de despliegue](docs/arquitectura/03_despliegue.drawio)
- [Flujos MQTT y HTTPS](docs/arquitectura/flujos.md)
- [Requisitos](docs/arquitectura/requisitos.md)
- [Decisiones ADR](docs/decisiones-adr/)
- [Guía de capturas y solución de problemas](docs/pruebas/GUIA_GTA_S5.md)

Los diagramas `.drawio` se abren gratis en https://app.diagrams.net/.

## Estado del proyecto

Fase I: documentación de requisitos, diagramas y decisiones técnicas. El ejemplo de Wokwi permite ensayar la mensajería MQTT y Last Will. La plataforma web, la base de datos y la conexión segura al servidor privado se desarrollan por separado y se integrarán en las siguientes semanas.
