#!/usr/bin/env python3
"""
Python test functions for breadcrumb detection validation
"""

import os
import sys
import json
from typing import Dict, List, Any
from datetime import datetime


def simple_function():
    """Basic function for testing"""
    return "test"


def function_with_params(param1: str, param2: int = 42) -> str:
    """Function with parameters and type hints"""
    return f"{param1}_{param2}"


def undocumented_function():
    """This function intentionally lacks breadcrumb documentation"""
    return "no breadcrumb"


async def async_function(data: Dict[str, Any]) -> List[str]:
    """Async function for testing"""
    return list(data.keys())


class TestClass:
    """Test class for method detection"""
    
    def documented_method(self, value: str) -> bool:
        """Method with proper documentation"""
        return bool(value)
    
    def undocumented_method(self):
        """Method without breadcrumb"""
        pass
    
    @staticmethod
    def static_method(x: int, y: int) -> int:
        """Static method with documentation"""
        return x + y
    
    @classmethod
    def class_method(cls, name: str) -> 'TestClass':
        """Class method with documentation"""
        return cls()


def complex_signature_function(*args, **kwargs) -> None:
    """Function with complex signature"""
    pass


def generator_function(items: List[str]):
    """Generator function for testing"""
    for item in items:
        yield item.upper()


def outer_function(data: str) -> str:
    """Function containing nested function"""
    
    def inner_function(x: str) -> str:
        return x.lower()
    
    return inner_function(data)


# Private function (should be excluded by underscore check)
def _private_function():
    """Private function that should be ignored"""
    return "private"


def closure_function(multiplier: int):
    """Function that returns a closure"""
    def multiply(x: int) -> int:
        return x * multiplier
    return multiply


if __name__ == "__main__":
    def main():
        """Main function for test execution"""
        print("Python function tests ready")
        return True
    
    main()