from cairo_kernel.repl import Repl
import pytest

my_repl = Repl()

def try_and_except(func):
    try:
        my_repl.run(func)
    except:
        pytest.fail()


func = """
func add2(x : felt) -> (x : felt): 
    return (x=x+2)
    end
"""
try_and_except(func)

multiple_imports = """
from starkware.cairo.common.uint256 import (
    Uint256, uint256_add, uint256_sub, uint256_lt, uint256_check
)
"""
try_and_except(multiple_imports)

import_struct = """
struct Location:
    member row : felt
    member col : felt
end"""

try_and_except(import_struct)