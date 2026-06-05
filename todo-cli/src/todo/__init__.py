"""A small, production-quality command-line Todo application.

The package is split into clear layers:

* :mod:`todo.models`    -- the :class:`~todo.models.Todo` domain entity.
* :mod:`todo.errors`    -- the exception hierarchy used across layers.
* :mod:`todo.storage`   -- JSON persistence (load/save, corruption handling).
* :mod:`todo.service`   -- domain logic operating on a store of todos.
* :mod:`todo.cli`       -- argument parsing and the process entry point.
"""

__all__ = ["__version__"]

__version__ = "1.0.0"
