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

* Запуск тестов:
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

### Структура БД

БД имеет следующую структуру:

![image](https://user-images.githubusercontent.com/91143425/217019562-25e79eb6-d6f9-4958-aa8e-0f09db68d448.png)

Таблица Comment - таблица для партицирования. Всего 3 партиции. Ключ партицирования: `id`. 

**Hash функция:** остаток от деления `id` на кол-во партиций (3)
