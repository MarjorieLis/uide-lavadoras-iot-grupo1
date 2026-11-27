# Diagramas de arquitectura

Aquí guardamos los dibujos que explican cómo está organizado el sistema de lavadoras compartidas y cómo se comunican sus partes.

| Archivo | Qué representa |
|---|---|
| `01_contexto.drawio` | Estudiantes, arrendador, lavadora y sistema |
| `02_contenedores.drawio` | ESP32, broker MQTT, servidor, base de datos y aplicación web |
| `03_despliegue.drawio` | Equipos donde funciona cada parte y conexiones de red |

Los archivos `.drawio` se abren gratuitamente en [diagrams.net](https://app.diagrams.net/) o desde Visual Studio Code con una extensión para Draw.io. Las imágenes `.png` sirven para colocar los diagramas en el informe. Los `.mmd` son versiones de texto del diseño.

## Otros documentos

- [flujos.md](flujos.md): qué mensajes viajan, qué protocolo utilizan y qué ocurre si falla la comunicación.
- [nivel-despliegue.md](nivel-despliegue.md): dónde funcionan el ESP32 y los servicios.
- [requisitos.md](requisitos.md): qué debe cumplir el sistema y cómo se comprueba.

El ejemplo del nodo que ya se probó está en [Wokwi](https://wokwi.com/projects/481853051628154881). En esa demostración se usa un broker público de pruebas; el diseño de arquitectura contempla un Mosquitto propio para el sistema completo.
