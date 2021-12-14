from cairo_kernel.repl import Repl

repl = Repl()
print(repl.run("from starkware.cairo.common.serialize import serialize_word"))
function = """
func main{output_ptr : felt*}():
    serialize_word(6 / 3)
    serialize_word(7 / 3)
    return ()
end
"""
repl.run(function)
repl.run("main()")