
# Backend del Sistema de Control y Comunicaciones para el Derivador Oceánico

Este proyecto es la interfaz backend del sistema de control y comunicaciones para el derivador oceánico. Está desarrollado utilizando Python y hace uso de `FastAPI` para la gestión de solicitudes HTTP asíncronas. Además, se utiliza `Poetry` para la gestión de dependencias y `Uvicorn` como servidor ASGI.

## Requisitos

Antes de comenzar, asegúrate de tener instalados los siguientes requisitos:

- Python (v3.8 o superior)
- Poetry (v1.1.6 o superior)

## Instalación

1. Clona el repositorio a tu máquina local:
```bash
git clone [URL_DEL_REPOSITORIO]
cd [DIRECTORIO_DEL_REPOSITORIO]
```

2. Instala las dependencias utilizando Poetry:
```bash
poetry install
```

3. Activa el entorno virtual de Poetry:
```bash
poetry shell
```

## Ejecución del Proyecto

Para ejecutar el servidor de desarrollo, utiliza el siguiente comando:
```bash
uvicorn apps.rest_api.main:app --reload
```
Esto iniciará el servidor y podrás acceder a la API en `http://localhost:8000/`.

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

- **apps/**: Contiene la aplicación principal y sus módulos.
  - **rest_api/**: Contiene la lógica de la API REST.
    - **dependencies.py**: Definición de dependencias y configuración de la API.
    - **main.py**: Punto de entrada de la aplicación.
    - **tests.py**: Pruebas relacionadas con la API.
    - **v1/**: Contiene las versiones de la API.
    - **assets/**: Recursos estáticos y otros archivos necesarios.
- **core/**: Contiene la lógica central del sistema.
  - **communication_system/**: Lógica del sistema de comunicación.
    - **application/**: Casos de uso y lógica de aplicación.
    - **domain/**: Modelos de dominio.
    - **infrastructure/**: Implementaciones de infraestructura.
    - **tests/**: Pruebas.
  - **iclisten/**: Lógica relacionada con el sistema PAM.
    - **application/**: Casos de uso y lógica de aplicación.
    - **domain/**: Modelos de dominio.
    - **infrastructure/**: Implementaciones de infraestructura.
    - **tests/**: Pruebas.
  - **shared/**: Componentes compartidos entre los diferentes módulos.
    - **application/**: Casos de uso y lógica de aplicación compartida.
    - **domain/**: Modelos de dominio compartidos.
    - **infrastructure/**: Implementaciones de infraestructura compartida.
    - **tests/**: Pruebas compartidas.
  - **surface_fields/**: Lógica relacionada con los campos de superficie.
    - **application/**: Casos de uso y lógica de aplicación.
    - **domain/**: Modelos de dominio.
    - **infrastructure/**: Implementaciones de infraestructura.
    - **tests/**: Pruebas.
- **system.sqlite**: Base de datos del sistema.

## Configuración

La configuración del proyecto se gestiona mediante variables de entorno. Puedes definir estas variables en un archivo `.env` en la raíz del proyecto. A continuación, se muestra un ejemplo del contenido del archivo `.env`:
```env
IRIDIUM_USERNAME=usuario_rockblock
IRIDIUM_PASSWORD=contraseña_rockblock
LOCALIZER_IMEI=imei_localizer
LOCALIZER_SERIAL=serial_localizer
DRIFTER_IMEI=imei_drifter
DRIFTER_SERIAL=serial_drifter
```

## Despliegue

Para desplegar la aplicación en un entorno de producción, sigue estos pasos:

1. Asegúrate de tener todas las dependencias instaladas utilizando Poetry:
```bash
poetry install --no-dev
```

2. Ejecuta Uvicorn sin la opción `--reload`:
```bash
uvicorn apps.rest_api.main:app --host 0.0.0.0 --port 8000
```


## Pruebas

Para ejecutar las pruebas, utiliza el siguiente comando:
```bash
pytest
```

## Contacto
Para cualquier duda o consulta, por favor contacta a [antonio.aparicio101@alu.ulpgc.es](mailto:antonio.aparicio101@alu.ulpgc.es).

