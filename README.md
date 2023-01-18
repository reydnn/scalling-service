# Scalling Service

## Backend Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.

## Локальная разработка

* Запуск проекта при помощи Docker Compose:
```shell
make up
```

* Просмотр логов:
```shell
make logs
```

* Запуск тестов run:
```shell
make test
```

### Pre-commit:

Для включения прекоммита:

```bash
make pre-commit-enable
```
После этого любой коммит будет обрабатываться прекоммитом

Для выключения:

```bash
make pre-commit-disable
```
