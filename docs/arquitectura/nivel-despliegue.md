# Nivel de despliegue del sistema

Se utiliza el **nivel 2 de Bahga y Madisetti** como referencia de arquitectura. Un ESP32 mide la actividad y controla el estado local de la lavadora, mientras que la VM Ubuntu reúne el broker MQTT, la API, la base de datos y el panel de consulta. Esta separación permite mantener el control del dispositivo y, al mismo tiempo, consultar el historial desde una aplicación web.

En la Fase I los servicios se organizan en la VM del grupo. La distribución se muestra en la vista de despliegue.
