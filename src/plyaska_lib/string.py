from functools import cache

import inflect
from inflection import underscore


def pluralize_snake(name: str):
    parts = name.split("_")
    parts[-1] = inflect.engine().plural(text=parts[-1])
    return "_".join(parts)


@cache
def camel_to_db_name(name: str):
    return pluralize_snake(underscore(name))
