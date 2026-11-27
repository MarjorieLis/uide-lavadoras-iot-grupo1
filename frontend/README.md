# Aplicación web

Esta carpeta contiene `index.html`, una pantalla sencilla que sirve para mostrar cómo se presentará el sistema al estudiante y al arrendador.

La pantalla permite observar la distribución visual de la información, pero todavía no está conectada a la API ni recibe datos MQTT. Por eso, el botón de solicitar uso no activa el ESP32 y no se realizan pagos reales.

En el sistema completo, la web permitirá solicitar un uso, consultar el estado de la lavadora y revisar los ciclos registrados. Los datos llegarán a través del servidor, según los [flujos de arquitectura](../docs/arquitectura/flujos.md).

Para ver la pantalla, abre `index.html` en un navegador. Para probar el nodo que sí publica por MQTT, utiliza [Wokwi](https://wokwi.com/projects/481853051628154881).
