import importlib
import inspect
import pkgutil

from beanie import Document

from plyaska_lib.models.base_document import BaseDocument


def load_beanie_models(package_name: str):
    package = importlib.import_module(package_name)
    models = []

    for _, module_name, _ in pkgutil.iter_modules(
        package.__path__, package.__name__ + "."
    ):
        module = importlib.import_module(module_name)
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(obj, Document)
                and obj is not Document
                and obj is not BaseDocument
            ):
                if obj in models:
                    continue
                if not getattr(obj, "_excluded", False):
                    models.append(obj)
    return models
