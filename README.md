# Sistema IoT para lavadoras compartidas

**UIDE, campus Loja · Proyecto integrador · Grupo 1**

**Integrantes:** Fabián Campoverde, Marjorie Jiménez y Cristina Orellana.

## ¿Qué buscamos resolver?

En residencias estudiantiles, varias personas pueden compartir una misma lavadora sin tener un registro claro de turnos y usos. Diseñamos un prototipo IoT que permita solicitar el uso desde una plataforma web, simular la confirmación de pago, habilitar una **carga de demostración de baja tensión** y registrar el inicio y fin del ciclo.

La arquitectura del sistema conecta un ESP32 con el servidor mediante MQTT. La API, la base de datos y el panel se organizan en una VM Ubuntu. El grupo trabaja en la **Fase I: diseño de arquitectura y desarrollo de los componentes**.

## Organización

| Carpeta | Contenido |
|---|---|
| `backend/` | Contrato inicial de la API y notas del servidor |
| `docs/arquitectura/` | Tres vistas editables en draw.io y Mermaid, tabla de flujos y requisitos |
| `docs/decisiones-adr/` | Dos registros de decisiones de arquitectura |
| `firmware-esp32/` | Base de lógica local, aún sin conectar al hardware |
| `frontend/` | Pantalla estática de referencia, sin API |
| `simulaciones/` | Casos de prueba y guía para Wokwi |

## Arquitectura — GTA S4

Abrir `docs/arquitectura/` para encontrar:

- `01_contexto.drawio`: personas, entorno y servicios externos.
- `02_contenedores.drawio`: contenedores y conexiones que inicia cada cliente.
- `03_despliegue.drawio`: dónde corre cada componente y fronteras de confianza.
- `flujos.md`: tabla F0–F9, opciones MQTT/HTTPS y respuesta ante fallos.

Los diagramas `.drawio` pueden abrirse y modificarse gratis en https://app.diagrams.net/. Los archivos `.mmd` se conservan como respaldo editable en texto.

## Etapas previstas

- **Fase I / GTA S4:** diagramas, requisitos y decisiones de arquitectura.
- **Desarrollo e integración:** firmware del ESP32, MQTTS, API, base de datos, panel y pruebas de comunicación.

## Seguridad y límites

- En el prototipo usar solo una **carga de baja tensión** para simular el lavado. No conectar ni intervenir una lavadora de 110/120 V en pruebas estudiantiles.
- No subir claves de MQTT, contraseñas, tokens ni datos personales al repositorio.
- Los pagos serán **simulados**; no hay pasarela de cobros real.

## Antes de entregar la GTA S4

1. Revisar con el grupo la arquitectura y la tabla de flujos.
2. Mantener `docs/arquitectura/requisitos.md` actualizado cuando cambie una decisión técnica.
3. Subir el repositorio a GitHub y pegar su enlace en el informe PDF.
4. Incorporar las observaciones del docente y firmar los aportes reales de cada integrante.
