# Servidor y base de datos

Esta carpeta reúne la organización de la parte del servidor. Su función es recibir las solicitudes de los estudiantes, guardar los pagos de prueba y relacionarlos con cada ciclo de lavado.

El archivo `api.yaml` describe las rutas de comunicación que usará la aplicación web. Es la definición de la API, no un servidor que ya esté en ejecución.

## Funciones del servidor

- Registrar la solicitud de uso de una lavadora.
- Comprobar una autorización de pago de prueba.
- Enviar una orden MQTT al ESP32 cuando el uso está autorizado.
- Guardar los eventos de inicio y fin de cada ciclo, sin duplicarlos.
- Permitir la consulta del estado y del historial desde la aplicación web.

Para conectar estas funciones se utiliza la arquitectura documentada en [la tabla de flujos](../docs/arquitectura/flujos.md). La simulación MQTT que ya realizamos se encuentra en [Wokwi](https://wokwi.com/projects/481853051628154881).
