# Simulación en Wokwi: lavadora compartida

Archivos:

- `main.py`: MicroPython para ESP32 con Wi-Fi, MQTT, JSON y Last Will.
- `diagram.json`: ESP32, botón de autorización de prueba, potenciómetro (simula corriente) y LED (simula carga).

**Para usarlo:** abre https://wokwi.com/projects/new/micropython-esp32, pega el contenido de ambos archivos en sus pestañas correspondientes y pulsa **Start Simulation**.

El broker de prueba es `broker.emqx.io:1883`. Desde Ubuntu escucha:

```bash
mosquitto_sub -h broker.emqx.io -p 1883 -t 'uide/g1/marjorielis/lavadora01/#' -v
```

Cuando detengas Wokwi, el Last Will enviará `desconectado` al tema de estado. Consulta la guía completa en [`docs/pruebas/GUIA_GTA_S5.md`](../../docs/pruebas/GUIA_GTA_S5.md).

**Proyecto guardado en Wokwi:** https://wokwi.com/projects/481853051628154881
