# ESP32 - nodo de lavadora (simulación)

El archivo `main.py` contiene la misma simulación que se utiliza en [`simulaciones/lavadora-wokwi/`](../simulaciones/lavadora-wokwi/).

### Pines de Wokwi

- **GPIO34:** perilla que simula el sensor de corriente.
- **GPIO4:** botón para autorizar el uso de prueba.
- **GPIO2:** LED que representa la habilitación de una carga de baja tensión.

### Estados

`BLOQUEADA → HABILITADA → LAVANDO → FINALIZADA → BLOQUEADA`

El nodo publica mensajes JSON con su identificador y diferencia telemetría, estado y eventos. Los mensajes de estado son retenidos y tienen **Last Will**, para mostrar `desconectado` si se detiene Wokwi de forma repentina.

Ver la [guía GTA S5](../docs/pruebas/GUIA_GTA_S5.md) para ejecutarlo y comprobarlo desde Ubuntu.

**No utilizar este código para controlar una lavadora real:** el ejemplo se conecta a un broker público de laboratorio sin autenticación y actúa exclusivamente sobre un LED.
