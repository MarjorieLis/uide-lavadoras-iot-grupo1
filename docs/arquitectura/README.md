# Arquitectura del sistema IoT de lavadoras compartidas

## Diagramas editables

| Archivo | Qué muestra |
|---|---|
| `01_contexto.drawio` | Usuarios, equipo físico y sistema de pago de prueba |
| `02_contenedores.drawio` | ESP32, broker, servidor, base de datos y aplicación |
| `03_despliegue.drawio` | Equipos, servicios y límites de la red |

Las imágenes `*_vista_previa.png` se utilizan para incluir las vistas en el informe. Los archivos `.drawio` se editan de manera gratuita en https://app.diagrams.net/ o con la extensión Draw.io Integration de Visual Studio Code.

Los `.mmd` se mantienen como una versión de texto editable de los diagramas. Para entregar basta con los `.drawio` y un enlace al repositorio.

## Documentación

- `flujos.md`: comunicación, seguridad y comportamiento ante fallas.
- `nivel-despliegue.md`: distribución de los componentes.
- `requisitos.md`: requisitos y forma de comprobarlos.

**Fase I:** diseño de arquitectura documentado y desarrollo de componentes en curso.
