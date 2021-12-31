from cairo_kernel.repl import Repl

my_repl = Repl()
func = """
func add2(x : felt) -> (x : felt): 
    return (x=x+2) 
    end
"""
my_repl.run(func)

multiple_imports = """
from starkware.cairo.common.uint256 import (
    Uint256, uint256_add, uint256_sub, uint256_lt, uint256_check
)
"""
my_repl.run(multiple_imports)

import_struct = """
struct Location:
    member row : felt
    member col : felt
end"""

my_repl.run(import_struct)