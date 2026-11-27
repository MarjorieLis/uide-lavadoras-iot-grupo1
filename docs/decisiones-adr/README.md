# Decisiones técnicas del sistema

En esta carpeta explicamos por qué elegimos ciertas tecnologías y cómo afectan al funcionamiento de las lavadoras compartidas. Cada documento presenta el problema, las opciones revisadas, la decisión y sus ventajas y dificultades.

- [ADR-001 – Comunicación MQTT](ADR-001-mensajeria-mqtt.md): explica cómo intercambian mensajes el servidor y el ESP32.
- [ADR-002 – Control local](ADR-002-control-local.md): explica cómo se autoriza un uso y cómo se identifican el inicio y el fin de un ciclo.

Estos documentos ayudan a entender los diagramas y las pruebas de la [carpeta de arquitectura](../arquitectura/). La demostración de Wokwi utiliza MQTT sobre un broker público únicamente para las pruebas de clase.
