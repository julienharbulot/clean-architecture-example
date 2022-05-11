# Clean Architecture Example Project

This project was created as an example implementation of the Clean Architecture (as well as Hexagonal Architecture, Ports & Adapters Architecture) with an http controller.

Installation:

```commandline
pip install -r pip-requirements.txt
```

Running the http server:

```commandline
python -m src
```

Running the example script:

```commandline
python demo_http_queries.py
```

Running the unit tests:

```commandline
./scripts/tests.sh
```

# Design

### General overview

- Project configuration and entrypoint happens in `__main__.App`
- The controller is implemented in `http_controller.py`, it builds the request model object and forwards it to the use case
- Each use case is implemented in its own package: `create_user`, `activate_user`, `get_user`

![General Overview](https://github.com/julienharbulot/clean-architecture-example/raw/master/docs/diagrams/general-overview.png)

### Use-case overview

![Use-case Overview](https://github.com/julienharbulot/clean-architecture-example/raw/master/docs/diagrams/use-case-overview.png)
