<!-- markdownlint-disable -->

#

<img alt="Starlite logo" src="./images/SVG/starlite-banner.svg" width="100%" height="auto">

<center>
![PyPI - License](https://img.shields.io/pypi/l/starlite?color=blue)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/starlite)

![PyPI - License](https://img.shields.io/pypi/l/starlite?color=blue)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/starlite)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=starlite-api_starlite&metric=coverage)](https://sonarcloud.io/summary/new_code?id=starlite-api_starlite)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=starlite-api_starlite&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=starlite-api_starlite)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=starlite-api_starlite&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=starlite-api_starlite)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=starlite-api_starlite&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=starlite-api_starlite)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=starlite-api_starlite&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=starlite-api_starlite)

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/starlite-api/starlite.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/starlite-api/starlite/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/starlite-api/starlite.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/starlite-api/starlite/alerts/)

[![Discord](https://img.shields.io/discord/919193495116337154?color=blue&label=chat%20on%20discord&logo=discord)](https://discord.gg/X3FJqy8d2j)
[![Matrix](https://img.shields.io/badge/%5Bm%5D%20chat%20on%20Matrix-bridged-blue)](https://matrix.to/#/#starlitespace:matrix.org)

[![Medium](https://img.shields.io/badge/Medium-12100E?style=flat&logo=medium&logoColor=white)](https://itnext.io/introducing-starlite-3928adaa19ae)

</center>
<!-- markdownlint-restore -->

Starlite is a light, opinionated and flexible ASGI API framework built on top
of **[pydantic](https://github.com/samuelcolvin/pydantic)** and **[Starlette](https://github.com/encode/starlette)**.

The Starlite framework supports **[plugins](usage/10-plugins/0-plugins-intro.md)**, ships
with **[dependency injection](usage/6-dependency-injection/0-dependency-injection-intro.md)**, **[authentication](usage/8-authentication.md)**
, **[OpenAPI specifications-generation](usage/12-openapi.md)** – among other common API-framework components such
as **[middleware](usage/7-middleware/0-middleware-intro.md)** and **[guards](usage/9-guards.md)**.

## Installation

```shell
pip install starlite
```

### Extras

To install the extras required for the built-in [Testing](./usage/14-testing.md) helpers:

```shell
pip install starlite[testing]
```

To install the extras required for logging with [Picologging](./usage/0-the-starlite-app/4-logging.md#picologging-integration):

```shell
pip install starlite[picologging]
```

To install the extras required for using the [Brotli Compression Middleware](usage/7-middleware/0-middleware-intro.md#brotli):

```shell
pip install starlite[brotli]
```

And to install all of the above:

```shell
pip install starlite[full]
```

## Minimal Example

**Define your data model** using pydantic or any library based on it (for example ormar, beanie, SQLModel):

```python title="my_app/models/user.py"
from pydantic import BaseModel, UUID4


class User(BaseModel):
    first_name: str
    last_name: str
    id: UUID4
```

Alternatively, you can **use a dataclass** – either from dataclasses or from pydantic:

```python title="my_app/models/user.py"
from uuid import UUID

# from pydantic.dataclasses import dataclass
from dataclasses import dataclass


@dataclass
class User:
    first_name: str
    last_name: str
    id: UUID
```

**Define a Controller** for your data model:

```python title="my_app/controllers/user.py"
from typing import List, NoReturn

from pydantic import UUID4
from starlite import Controller, Partial, get, post, put, patch, delete

from my_app.models import User


class UserController(Controller):
    path = "/users"

    @post()
    async def create_user(self, data: User) -> User:
        ...

    @get()
    async def list_users(self) -> List[User]:
        ...

    @patch(path="/{user_id:uuid}")
    async def partial_update_user(self, user_id: UUID4, data: Partial[User]) -> User:
        ...

    @put(path="/{user_id:uuid}")
    async def update_user(self, user_id: UUID4, data: User) -> User:
        ...

    @get(path="/{user_id:uuid}")
    async def get_user(self, user_id: UUID4) -> User:
        ...

    @delete(path="/{user_id:uuid}")
    async def delete_user(self, user_id: UUID4) -> NoReturn:
        ...
```

When **instantiating** your app, **import your controller** into your application's entry-point and pass it to Starlite:

```python title="my_app/main.py"
from starlite import Starlite

from my_app.controllers.user import UserController

app = Starlite(route_handlers=[UserController])
```

To **run your application**, use an ASGI server such as [uvicorn](https://www.uvicorn.org/):

```shell
uvicorn my_app.main:app --reload
```

## About the Starlite Project

This project builds on top the **Starlette ASGI toolkit** and **pydantic modelling** to create a higher-order
opinionated
framework. The idea to use these two libraries as a basis is of course not new - it was first done in FastAPI, which in
this regard (and some others) was a source of inspiration for this framework. Nonetheless, **Starlite is not FastAPI** -
it
has a different design, different project goals and a completely different codebase.

1. The **goal** of this project is to become a **community-driven** project. That is, not to have a single "owner" but
   rather a
   core team of maintainers that leads the project, as well as community contributors.
2. Starlite draws **inspiration from NestJS** - a contemporary TypeScript framework - which places opinions and patterns
   at
   its core. As such, the design of the API **breaks from the Starlette design** and instead offers an opinionated
   alternative.
3. Finally, **Python OOP** is extremely powerful and versatile. While still allowing for **function-based endpoints**,
   Starlite
   seeks to build on this by placing **class-based controllers** at its core.

## Example Applications

- [starlite-pg-redis-docker](https://github.com/starlite-api/starlite-pg-redis-docker): In addition to Starlite, this
  demonstrates a pattern of application modularity, SQLAlchemy 2.0 ORM, Redis cache connectivity, and more. Like all
  Starlite projects, this application is open to contributions, big and small.
- [starlite-hello-world](https://github.com/starlite-api/starlite-hello-world): A bare-minimum application setup. Great
  for testing and POC work.
