
from cairo_kernel.repl import Repl

my_repl = Repl()


my_repl.run("%builtins output")

my_repl.run(
"""
func add1(x : felt) -> (x : felt): 
    return (x=x+1) 
    end
"""
)
my_repl.run("add1(10)")

my_repl.run("serialize_word(1234)")
my_repl.run(
"""
func serialize_word{output_ptr : felt*}(word):
    assert [output_ptr] = word
    let output_ptr = output_ptr + 1
    return ()
end
"""
)
my_repl.run("serialize_word(1234)")