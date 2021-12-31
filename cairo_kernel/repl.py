#!/usr/bin/env python3
from typing import List, Union

from starkware.cairo.lang.compiler.assembler import assemble
from starkware.cairo.lang.compiler.ast.cairo_types import TypePointer, TypeStruct, TypeFelt
from starkware.cairo.lang.compiler.ast.code_elements import (
    CodeElement,
    CodeElementFunction,
    CodeElementImport,
    CodeElementScoped,
)

from starkware.cairo.lang.compiler.ast.expr import Expression
from starkware.cairo.lang.compiler.ast.expr_func_call import ExprFuncCall
from starkware.cairo.lang.compiler.ast.module import CairoModule
from starkware.cairo.lang.compiler.ast.node import AstNode
from starkware.cairo.lang.compiler.cairo_compile import get_module_reader
from starkware.cairo.lang.compiler.constants import MAIN_SCOPE
from starkware.cairo.lang.compiler.error_handling import LocationError
from starkware.cairo.lang.compiler.expression_evaluator import ExpressionEvaluator
from starkware.cairo.lang.compiler.identifier_definition import (
    FutureIdentifierDefinition,
    ReferenceDefinition,
)
from starkware.cairo.lang.compiler.identifier_manager import IdentifierManager
from starkware.cairo.lang.compiler.import_loader import (
    DirectDependenciesCollector,
    ImportsCollector,
)
from starkware.cairo.lang.compiler.instruction import Register
from starkware.cairo.lang.compiler.parser import ParserError, parse
from starkware.cairo.lang.compiler.preprocessor.identifier_collector import IdentifierCollector
from starkware.cairo.lang.compiler.preprocessor.preprocessor import Preprocessor, ReferenceState
from starkware.cairo.lang.compiler.preprocessor.struct_collector import StructCollector
from starkware.cairo.lang.compiler.preprocessor.unique_labels import UniqueLabelCreator
from starkware.cairo.lang.compiler.program import StrippedProgram
from starkware.cairo.lang.compiler.scoped_name import ScopedName
from .syntax_highlighting import CairoLexer
from starkware.cairo.lang.vm.cairo_runner import CairoRunner

PRIME = 2 ** 251 + 17 * 2 ** 192 + 1

INPUT_FILENAME = "<input>"
CAIRO_BUILTIN_SCOPE = ScopedName.from_string("starkware.cairo.common.cairo_builtins")


class Repl:
    def __init__(self):
        self.identifiers = IdentifierManager()
        self.struct_collector = StructCollector(identifiers=self.identifiers)
        # TODO(lior, 01/10/2021): Get prime as an argument.
        self.preprocessor = Preprocessor(prime=PRIME, identifiers=self.identifiers)
        self.identifier_collector = IdentifierCollector()
        self.unique_label_creator = UniqueLabelCreator()
        # TODO(lior, 01/10/2021): Get path as an argument.
        path = ["src"]
        self.module_reader = get_module_reader(path)

        builtins = ["output", "pedersen", "range_check", "ecdsa"]
        layout = "small"
        program = StrippedProgram(prime=PRIME, data=[], builtins=builtins, main=0)
        self.runner = CairoRunner(program=program, layout=layout, proof_mode=False)
        self.runner.initialize_segments()
        self.runner.initialize_main_entrypoint()
        self.runner.initialize_vm(hint_locals={})

        for offset, builtin in enumerate(builtins, -2 - len(builtins)):
            builtin_name = MAIN_SCOPE + f"{builtin}_ptr"
            self.preprocessor.add_future_definition(
                name=builtin_name,
                future_definition=FutureIdentifierDefinition(identifier_type=ReferenceDefinition),
            )
            if builtin == "output":
                self.preprocessor.add_simple_reference(
                    name=builtin_name,
                    reg=Register.FP,
                    cairo_type=TypePointer(
                        pointee=TypeFelt(),
                    ),
                    offset=offset,
                    location=None,
            )
            else:
                self.preprocessor.add_simple_reference(
                    name=builtin_name,
                    reg=Register.FP,
                    cairo_type=TypePointer(
                        pointee=TypeStruct(
                            scope=CAIRO_BUILTIN_SCOPE + "HashBuiltin",
                            is_fully_resolved=True,
                        ),
                    ),
                    offset=offset,
                    location=None,
                )
            self.preprocessor.reference_states[builtin_name] = ReferenceState.ALLOW_IMPLICIT

    def parse(self, code: str) -> Union[CodeElement, Expression]:
        try:
            first_parse = parse(
                filename=INPUT_FILENAME,
                code=code,
                code_type="expr",
                expected_type=Expression,
            )
            if isinstance(first_parse, ExprFuncCall):
                return parse(
                    filename=INPUT_FILENAME,
                    code=code,
                    code_type="code_element",
                    expected_type=CodeElement,
                )
            else:
                return first_parse
        except ParserError:
            return parse(
                filename=INPUT_FILENAME,
                code=code,
                code_type="code_element",
                expected_type=CodeElement,
            )

    def preprocess_parser(self, code: str):

        code = code.split('\n')
        # Comments will be ignored
        code = [line.split('#')[0] for line in code]

        # Supports extra new lines
        code = [line for line in code if line != '']
        return '\n'.join(code)

    def is_func_def(self, code:str):
        return code.strip().startswith('func ')

    # List of instructions that generate and end statement
    triggers_end = ['if']

    def func_def_ends_index(self, list_instructions):
        count = 0
        i = 0
        while i <= len(list_instructions):
            if list_instructions[i].strip().startswith('end'):
                if count == 0:
                    return i
                else:
                    count -= 1
            if list_instructions[i].strip().startswith(tuple(self.triggers_end)):
                count += 1
            i += 1

    def is_struct_def(self, code:str):
        return code.strip().startswith('struct ')

    def struct_def_ends_index(self, list_instructions):
        i = 0
        while i <= len(list_instructions):
            if list_instructions[i].strip().startswith('end'):
                return i
            i += 1

    def is_multiple_imports(self, code:str):
        return code.strip().endswith('import (')

    def multiple_imports_end_index(self, list_instructions):
        i = 0
        while i <= len(list_instructions):
            if ')' in list_instructions[i]:
                return i
            else:
                i += 1

    def get_instructions(self, code:str):
        list_instructions = code.split('\n')
        output_instructions = []
        i = 0
        while i < len(list_instructions):
            current = list_instructions[i]

            if not self.is_func_def(current) \
                    and not self.is_multiple_imports(current)\
                    and not self.is_struct_def(current):
                output_instructions.append(current)
                i += 1
            else:
                if self.is_func_def(current):
                    end_index = self.func_def_ends_index(list_instructions[i:])
                elif self.is_struct_def(current):
                    end_index = self.struct_def_ends_index(list_instructions[i:])
                else:
                    end_index = self.multiple_imports_end_index(list_instructions[i:])
                list_instructions = [instruction.strip() for instruction in list_instructions]
                output_instructions.append('\n'.join(list_instructions[i: i + end_index + 1]))
                i += end_index + 1

        return output_instructions

    def run(self, code: str):
        code = self.preprocess_parser(code)
        list_instructions = self.get_instructions(code)
        for instruction in list_instructions:
            obj = self.parse(instruction)

            if isinstance(obj, CodeElement):
                self.exec(obj)
            elif isinstance(obj, Expression):
                value = self.eval(obj)
                return value
            else:
                raise NotImplementedError(f"Unsupported type: {type(obj).__name__}")

    def exec(self, code_element: CodeElement):
        # If the code element is an import statement or a function, we don't need to run
        # the corresponding generated instructions.
        skip_execution = isinstance(code_element, (CodeElementImport, CodeElementFunction))

        # Replace code_element with a scoped version.
        code_element = CodeElementScoped(scope=MAIN_SCOPE, code_elements=[code_element])

        # Find used modules (due to imports).
        direct_dependencies_collector = DirectDependenciesCollector()
        direct_dependencies_collector.visit(code_element)

        import_collector = ImportsCollector(self.module_reader.read)
        for pkg_name, location in direct_dependencies_collector.packages:
            import_collector.collect(pkg_name, location=location)

        # Create a list of code elements.
        elements: List[AstNode] = []
        for module_name, ast in import_collector.collected_data.items():
            scope = ScopedName.from_string(module_name)
            elements.append(CairoModule(cairo_file=ast, module_name=scope))
        elements.append(code_element)

        elements = list(map(self.unique_label_creator.visit, elements))

        # Collect identifiers and update the preprocessor with the new identifiers.
        for element in elements:
            self.identifier_collector.visit(element)

        new_identifiers = self.identifier_collector.identifiers

        # Filter out identifiers that were already defined.
        new_identifiers = new_identifiers.exclude(self.identifiers)
        self.preprocessor.update_identifiers(new_identifiers)

        # Store the flow_tracking data before calling the preprocessor.
        old_flow_tracking = self.preprocessor.flow_tracking.data

        for element in elements:
            self.struct_collector.visit(element)

        # Invoke the preprocessor.
        for element in elements:
            self.preprocessor.visit(element)

        self.preprocessor.resolve_labels()

        preprocessed_program = self.preprocessor.get_program()
        # TODO(lior, 01/10/2021): Consider assembling only the new instructions that were added.
        program = assemble(
            preprocessed_program=preprocessed_program, main_scope=MAIN_SCOPE, add_debug_info=True
        )
        for i, value in enumerate(program.data):
            self.runner.memory[self.runner.program_base + i] = value
        self.runner.vm.load_hints(program=program, program_base=self.runner.program_base)

        new_pc = len(program.data)
        try:
            if skip_execution:
                self.preprocessor.flow_tracking.data = old_flow_tracking
            else:
                self.runner.run_until_pc(self.runner.program_base + new_pc)
        finally:
            # Move pc to the end, even if there has been a runtime error.
            self.runner.vm.run_context.pc = self.runner.program_base + new_pc

    def eval(self, expr: Expression):
        with self.preprocessor.scoped(new_scope=MAIN_SCOPE, parent=None):
            expr = self.preprocessor.simplify_expr_as_felt(expr)
            return ExpressionEvaluator(
                prime=PRIME,
                ap=self.runner.vm.run_context.ap,
                fp=self.runner.vm.run_context.fp,
                # TODO(lior, 01/10/2021): Replace memory with a proxy that handles auto-deduction.
                memory=self.runner.vm.run_context.memory,
                identifiers=self.identifiers,
            ).eval(expr)

    def is_repl_line_complete(self, code: str) -> bool:
        """
        Returns True if the given code is complete and does not require additional code lines.
        For example: "1 + 2" is complete, while "func foo():" is not.
        """
        if len(code.strip()) == 0:
            return True
        try:
            self.parse(code=code)
        except LocationError as exc:
            if "Unexpected end-of-input" in str(exc):
                return False
        return True
