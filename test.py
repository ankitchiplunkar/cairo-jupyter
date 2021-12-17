from cairo_kernel.repl import Repl

repl = Repl()
print(repl.run("from starkware.cairo.common.serialize import serialize_word"))
function = "serialize_word(6)"
repl.run(function)