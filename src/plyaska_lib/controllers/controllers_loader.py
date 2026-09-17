import importlib
import pkgutil


def load_fastapi_routers(package_name: str):
    package = importlib.import_module(package_name)
    models = []

    for _, module_name, _ in pkgutil.iter_modules(
        package.__path__, package.__name__ + "."
    ):
        module = importlib.import_module(module_name)
        value = getattr(module, "router", None)
        if value is not None:
            models.append(value)
    return models
