# Simulaciones y pruebas — planificación

Se propone simular la lógica del nodo en **Wokwi** y después comunicarla con el broker Mosquitto del laboratorio. Esta carpeta no afirma que la integración ya esté construida.

- `escenarios.csv`: casos que deberán demostrar los tres integrantes.
- `payloads-ejemplo.json`: mensajes de prueba orientativos.

## Evidencia sugerida para más adelante

1. Inicio del nodo y estado BLOQUEADA.
2. Autorización válida de prueba y transición a HABILITADA.
3. Inicio y fin del ciclo con datos simulados.
4. Reenvío del mismo comando sin nueva habilitación.
5. Desconexión del ESP32 e indicación de estado antiguo en el panel.

**Simulación:** el código y las pruebas del ESP32 se organizan en esta carpeta. Añadir el enlace del proyecto Wokwi al incorporarlo al repositorio.
