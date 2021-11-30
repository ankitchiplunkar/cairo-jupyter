from cairo_kernel.repl import Repl

my_repl = Repl()
func = """
func add2(x : felt) -> (x : felt): 
    return (x=x+2) 
    end
"""
my_repl.run(func)
func2 = """
func add4(x : felt) -> (x : felt): 
    return (x=x+4) 
    end
"""
my_repl.run(func2)
my_repl.run("add4(2)")