from ipykernel.kernelbase import Kernel
from prompt_toolkit.lexers import PygmentsLexer
from syntax_highlighting import CairoLexer
from starkware.cairo.lang.compiler.error_handling import LocationError
from repl import Repl
import traceback
import sys


class CairoKernel(Kernel):
    implementation = "Cairo"
    implementation_version = "0.0.1"
    language = "cairo"
    language_version = "0.4.2"
    language_info = {
        "name": "Cairo",
        "mimetype": "text/plain",
        "file_extension": ".cairo",
        # TODO(add lexer)"
        # "pygments_lexer": PygmentsLexer(CairoLexer),
    }
    banner = "Cairo Kernel - scale dApps using STARKs"
    repl = Repl()

    def do_execute(
        self, code, silent, store_history=True, user_expressions=None, allow_stdin=False
    ):
        if not silent:
            value = self.repl.run(code)
            if value is not None:
                stream_content = {"name": "stdout", "text": str(value)}
            else:
                stream_content = {"name": "stdout", "text": value}
            
            self.send_response(self.iopub_socket, "stream", stream_content)
            
        # TODO(exception handling)"
        """
        try:
            self.run(code)
        except LocationError as exc:
            print(exc, file=sys.stderr)
        except Exception:
            traceback.print_exc()
        """
        return {
                "status": "ok",
                # The base class increments the execution count
                "execution_count": self.execution_count,
                "payload": [],
                "user_expressions": {},
            }     


if __name__ == "__main__":
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=CairoKernel)
