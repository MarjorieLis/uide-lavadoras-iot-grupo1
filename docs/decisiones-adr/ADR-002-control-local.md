# ADR-002 — Control local y registro de ciclos

- **Estado:** Definido para la Fase I; implementación en desarrollo.
- **Fecha de elaboración:** 22 de noviembre de 2026.
- **Requisitos relacionados:** R-L01, R-L02, R-L03 y R-L05 (ver `../arquitectura/requisitos.md`).

## Contexto

El prototipo debe representar una lavadora que solo puede iniciar un uso autorizado y registrar comienzo y fin del ciclo. La red no debería decidir cada lectura del sensor, y una repetición de un mensaje no debe habilitar dos veces la carga.

## Alternativas consideradas

1. **Control totalmente desde el servidor:** el dispositivo dependería de la comunicación para interpretar cada cambio.
2. **Temporizador fijo:** fácil de simular, pero no verifica si una carga realmente se puso en marcha.
3. **Máquina de estados local con sensor:** requiere más pruebas, pero separa la seguridad básica y la detección del ciclo del estado de Internet.

## Decisión

El control del ESP32 se organiza mediante estos estados: **BLOQUEADA → HABILITADA → LAVANDO → FINALIZADA**. Para pasar a HABILITADA debe existir una autorización válida y no repetida. Una lectura de corriente acondicionada permitirá estimar inicio y fin del ciclo. Si el lavado no comienza dentro de **10 minutos**, la habilitación expira; el servidor deberá resolver el pago simulado como saldo a favor o solicitud sin consumir, sin registrar un lavado completado.

## Consecuencias

- **A favor:** el sensor y las reglas básicas siguen locales; permite pruebas de red con una carga de baja tensión; facilita relacionar un pago de prueba con un ciclo.
- **En contra:** los cambios de estado necesitan pruebas; pausas de consumo podrían confundirse con un fin de ciclo; reinicios pueden perder datos si no hay persistencia.
- **Pruebas de integración:** detección de inicio y fin del ciclo, respuesta ante reinicio, órdenes repetidas y recuperación de eventos tras desconexión.

**Seguridad física:** el montaje de demostración no incluye la conexión directa de un relé de práctica a una lavadora conectada a la red eléctrica. La demostración del grupo será de **baja tensión**.
