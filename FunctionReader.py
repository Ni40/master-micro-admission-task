import re
import math
from typing import Callable, Optional


class FunctionReader:

    def __init__(self, func: str) -> None:
        """
        Parses a string and creates a function f(x) that can be used to evaluate the function for different values,\n
        f(x) is accesible via the method get_function()
        """
        self.error_msg = ""
        # Allow for whitespace and capital X
        func = func.replace(' ', '').lower()
        # regex for valid string input
        # [operand] is x or real decimal
        decimal = r'-?[0-9]+\.?[0-9]*'
        operand = rf'(x|{decimal})'
        # [operation] is - or + or * or / or ^
        operation = r'[-+*/^]'
        # [operand]([operation][operand])*
        pattern = re.compile(rf'{operand}({operation}{operand})*')
        # find if the string is equivalent to the regex
        self.valid = bool(pattern.fullmatch(func))
        if self.valid:
            # Add parenthesis around negative numbers
            func = re.sub(rf'(^|{operation})(-[0-9]+\.?[0-9]*)', r'\1(\2)', func)
            # Create latex-like string for display
            self.__function_string = '{{'
            self.__function_string += re.sub(rf'([^(])({operation})', r'\1}\2{', func)
            self.__function_string += '}}'
            self.__function_string = self.__function_string.replace('(', '').replace(')', '')
            # Replace ^ with its python equivalent
            func = func.replace('^', '**')
            self.__function = self.__create_function(func)
        else:
            self.error_msg = "Unsupported syntax or invalid input"
            if func.find('(') != -1 or func.find(')') != -1:
                self.error_msg += ",\n parenthesis aren't supported"

    def __create_function(self, func: str) -> Callable[[float], Optional[float]]:
        # Create function to be used
        def f(x: float) -> Optional[float]:
            # to avoid div by zero errors
            try:
                return eval(func)
            except:
                return math.nan
        return f

    def get_function(self) -> Optional[Callable[[float], Optional[float]]]:
        """
        Returns a function that can be used to compute f from x if f(x) exists, else numpy.nan\n
        returns None if the string used to generate function was invalid\n
        e.g:\n
        \tf = FunctionReader('x+3').get_function()\n
        \tprint(f(2)) # prints 5
        """
        return self.__function if self.valid else None

    def get_string(self) -> str:
        """
        Returns a latex-like function string for display
        """
        return self.__function_string

    def get_error(self) -> str:
        return self.error_msg
