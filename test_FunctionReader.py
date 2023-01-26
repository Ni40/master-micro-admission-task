import re
import pytest
from FunctionReader import FunctionReader

# List of tuples (unparsed, parsed)
valid_functions = [
    ('X +  3.5 ', 'x+3.5'),
    ('x ^ 2-3 ', 'x**2-3'),
    ('2.3^x ', '2.3**x'),
    ('x*x ', 'x*x'),
    ('x/ 3 ', 'x/3'),
    ('x ^-3 ', 'x**(-3)'),
    ('x + -3 ', 'x+(-3)'),
    ('22 ', '22'),
    ('-2^x', '(-2)**x'),
]


@pytest.mark.parametrize('funcs', valid_functions)
def test_FunctionReader_valid_inputs(funcs):
    unparsed_function, parsed_function = funcs
    # Create function from unparsed string
    f_r_obj = FunctionReader(unparsed_function)
    f = f_r_obj.get_function()
    for i in range(-10, 11):
        x = i/10
        try:
            value = eval(parsed_function)
        except:
            value = None
        assert f(x) == value


invalid_functions = [
    '2^y',
    '1x',
    'x//3',
    'xx',
]


@pytest.mark.parametrize('funcs', invalid_functions)
def test_FunctionReader_invalid_inputs(funcs):
    f_r_obj = FunctionReader(funcs)
    f = f_r_obj.get_function()
    assert f is None
