from src.plyaska_lib import string

def test_pluralize_snake():
    assert string.pluralize_snake('test') == 'tests'


def test_camel_to_db_name():
    assert string.camel_to_db_name('Test') == 'tests'