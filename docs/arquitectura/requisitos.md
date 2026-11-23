# Requisitos del sistema de lavadoras compartidas

Estos requisitos organizan el diseño y las pruebas de integración del sistema.

| ID | Requisito | Cómo se verifica |
|---|---|---|
| R-L01 | Autorizar una sesión solo después de confirmar un pago **de prueba** | Repetir solicitud y comprobar una sola autorización válida |
| R-L02 | Detectar inicio y fin de un ciclo mediante medición de corriente | Simular patrones de consumo y comprobar cambios de estado |
| R-L03 | Relacionar cada pago de prueba con un ciclo y evitar duplicados | Reenviar `event_id` y comprobar que la base guarda una sola fila |
| R-L04 | Informar cuando el nodo se desconecta | Cortar conexión y comprobar Last Will / edad del último estado |
| R-L05 | Hacer demostración sin tensión de red doméstica | Usar LED, motor o carga de **baja tensión** y mantener la lavadora real fuera del montaje |

**Control de cambios:** si el grupo modifica un requisito durante el desarrollo, se actualizan los diagramas, los flujos y los ADR relacionados.
