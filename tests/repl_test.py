from cairo_kernel.repl import Repl
import pytest

my_repl = Repl()

func = """
func add2(x : felt) -> (x : felt): 
    return (x=x+2) 
    end
"""

multiple_imports = """
from starkware.cairo.common.uint256 import (
    Uint256, uint256_add, uint256_sub, uint256_lt, uint256_check
)
"""

import_struct = """
struct Location:
    member row : felt
    member col : felt
end"""


@pytest.mark.parametrize("func", [func, multiple_imports, import_struct])
def test_repl_run(func):
    my_repl.run(func)