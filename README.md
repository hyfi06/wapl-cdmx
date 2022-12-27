# WiFi Access Point Location (wapl) API CDMX

API Rest of WiFi access points location in the CDMX

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)


## Architecture
![Architecture diagram](diagram.svg)


## Endpoints



## Development

### First step

Build docker images:

```bash
cd wapl
docker-compose -f local.yml build
```

Up all servicies

```bash
docker-compose -f local.yml up
```

Create super user

```bash
docker-compose -f local.yml run --rm django python manage.py createsuperuser
```

## License

Copyright (c) 2022 Héctor Olvera Vital

Licensed under the [MIT License](LICENSE).
