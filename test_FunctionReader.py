import pytest
import math
from FunctionReader import FunctionReader

# List of tuples (unparsed, parsed)
valid_functions = [
    ('X +  3.5 ', 'x+3.5', '{{x}+{3.5}}'),
    ('x ^ 2-3 ', 'x**2-3', '{{x}^{2}-{3}}'),
    ('2.3^x ', '2.3**x', '{{2.3}^{x}}'),
    ('x*x ', 'x*x', '{{x}*{x}}'),
    ('x/ 3 ', 'x/3', '{{x}/{3}}'),
    ('x ^-3 ', 'x**(-3)', '{{x}^{-3}}'),
    ('x + -3 ', 'x+(-3)', '{{x}+{-3}}'),
    ('22 ', '22', '{{22}}'),
    ('-2^x', '(-2)**x', '{{-2}^{x}}'),
]


@pytest.mark.parametrize('funcs', valid_functions)
def test_FunctionReader_valid_inputs(funcs):
    unparsed_function, parsed_function, latex_literal = funcs
    # Create function from unparsed string
    f_r_obj = FunctionReader(unparsed_function)
    f = f_r_obj.get_function()
    # iterate over some values
    for i in range(-10, 11):
        x = i/10
        # for div by zero errors
        try:
            value = eval(parsed_function)
        except:
            value = math.nan
        assert f(x) == value or (math.isnan(f(x)) and math.isnan(value))
        assert f_r_obj.get_string() == latex_literal


invalid_functions = [
    '2^y',
    '1x',
    'x//3',
    'xx',
    'x*(x)'
]


@pytest.mark.parametrize('funcs', invalid_functions)
def test_FunctionReader_invalid_inputs(funcs):
    f_r_obj = FunctionReader(funcs)
    f = f_r_obj.get_function()
    assert f is None
    if funcs.find('(') == -1:
        assert f_r_obj.get_error() == "Unsupported syntax or invalid input"
    else:
        assert f_r_obj.get_error() == "Unsupported syntax or invalid input,\n parenthesis aren't supported"
