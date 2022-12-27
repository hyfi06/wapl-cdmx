# WiFi Access Point Location (wapl) API CDMX

Un desarrollador backend debe saber tomar decisiones de arquitectura para cada proyecto. Aquí explico mas que tomé a lo largo del desarrollo de este proyecto.

## Stack
El stack que decidí usar fue django, debido a su rapidez y sus múltiples herramientas que existen.

Además, el Cookiecutter de Django es muy completo. Implementa una arquitectura de micro servicios mediante contenedores de Docker.

## Arquitectura

Tenemos una aplicación monolítica, pero que se nutre de micros servicios
 - Una base de datos de Postgresql
 - El stack de Celery para realizar tareas asíncronas. El cual contiene a su vez los siguientes servicios
    - Redis como broker de mensajes
    - flowers
    - Celery beat
    - Celery worker

## Datos
Los datos son extraídos del [Portal de Datos Abiertos de la Ciudad de México](https://datos.cdmx.gob.mx/dataset/puntos-de-acceso-wifi-en-la-ciudad-de-mexico).

Estos datos son versionados y modificados a través del tiempo. Por lo que, decidí aprovechar el servicio de Celery para generar una tarea asíncrona que actualice los datos. Esta se realiza ingresando al portal y mediante XPATH se obtiene la liga a los datos más recientes. Posteriormente, procesar y se cargan o actualizan en la base de datos.

## REST API

Para generar el API REST, use el paquete `djangorestframework` (drf). Este framework proporciona una rápida implementación de un ViewSet para listar nuestros datos. Y junto con `django_filters`, podemos configurar en pocas líneas de código nuestros filtros.

Para la lógica de negocio fue indispensable modificar el `queryset` para listar los puntos de acceso wifi en orden de proximidad a una latitud y longitud dadas.

```python
queryset.annotate(
    distance=(Power(F('lat') - lat, 2) + Power(F('long') - long, 2))
).order_by('distance')
```

Realmente se usó la distancia al cuadrado. No es esencial calcular la raíz cuadrada, ya que es una función estrictamente creciente, es decir, va a preserva el orden.

La paginación la obtenemos directamente de una configuración de drf.

## GraphQL
Para implementar GraphQL se usaron los paquetes `graphene` y `graphene_django`

Para realizar la paginación se implementó Relay.

Para el resolve de `nearby_hotspots`, se realizó nuevamente el cálculo de la distancia al cuadrado.

Volver al [README.md](README.md)