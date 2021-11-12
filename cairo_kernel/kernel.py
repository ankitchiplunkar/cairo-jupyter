import sys
import traceback

from ipykernel.kernelbase import Kernel
from prompt_toolkit.lexers import PygmentsLexer
from .syntax_highlighting import CairoLexer
from starkware.cairo.lang.compiler.error_handling import LocationError
from .repl import Repl


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
            try:
                value = self.repl.run(code)
                stream_content = {"name": "stdout", "text": str(value) if value else value}
                self.send_response(self.iopub_socket, "stream", stream_content)
                return {
                    "status": "ok",
                    # The base class increments the execution count
                    "execution_count": self.execution_count,
                    "payload": [],
                    "user_expressions": {},
                }

            except LocationError as exc:
                error_msg = str(exc)
            except Exception:
                error_msg = str(traceback.print_exc())

            stream_content = {"name": "stdout", "text": error_msg}
            self.send_response(self.iopub_socket, "stream", stream_content)
            return {
                "status": "error",
                #TODO(arie): set right parameteres for status = error
                # "ename": "my_ename",
                # "evalue": "my_evalue",
                # "traceback": error_msg
            }



if __name__ == "__main__":
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=CairoKernel)
