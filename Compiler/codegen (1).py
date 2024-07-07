"""
__author__ = "Jieung Kim et al."
__copyright__ = "Copyright 2024, Jieung Kim et al."
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Jieung Kim"
__email__ = "jieungkim@inha.ac.kr"
"""

# This file is used to generate intermediate code for
# our ToyPL.It is divided into two parts: `CodeGenFunc`
# and `CodeGen`. While you are not required to maintain
# this structure, you must ensure that all test cases
# pass without modifying the top-level interface of
# this file.

# Our design includes two classes:
# 1. `CodeGenFunc`: This class creates intermediate code
#     for each function. The intermediate code for each
#     function is similar to our original ToyPL syntax,
#     but with the following main differences:
#     1) Using "jump" and "label" instead of while loops.
#     2) Using "absolute" paths instead of relative
#        paths within namespaces.
# 2. Iteratively apply `CodeGenFunc` to each function
#    in the file and print the generated result as a
#    string format.
#
# Here are a few examples of function-wise intermediate
# codes, which are the results of the generation in
# `example01`. Note that the intermediate code differs
# somewhat from the TAC (Three-Address Code) format in
# our lecture notes. The format used here simplifies
# the problem compared to the TAC format from our
# lecture notes.

# Input (next_prime function defined in Util namespace)
'''
namespace Util
  ...
  func next_prime(n)
  var p
  begin
    p <- 0;
    while (p == 0) do {
      n <- n + 1;
      p <- call is_prime(n);
    };
    return n
  end
end
'''
# Desired output
'''
func :Util.next_prime(n) {
	t0 <- 0
	p <- t0
L0:
	t1 <- 0
	t2 <- p == t1
	branch t2 L1 L2
L1:
	t3 <- 1
	t4 <- n + t3
	n <- t4
	p <- call :Util.is_prime(n)
	jump L0
L2:
	return n
}
'''

# Input (main function)
'''
func main()
var r, x, _
begin
  _ <- call Godel.init_put();
  x <- 1;
  print(Godel.code);
  _ <- call Godel.init_get();
  x <- 1
end
'''
# Desired output
'''
func :main() {
	_ <- call :Godel.init_put()
	t0 <- 1
	x <- t0
	print :Godel.code
	_ <- call :Godel.init_get()
	t1 <- 1
	x <- t1
}
'''


# TODO: Implement the following class
class CodeGenFunc:

    def __init__(self, constants, function_ast):
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0
        self.codegen_stmts(function_ast)

    def new_temp(self):
        temp_name = f't{self.temp_counter}'
        self.temp_counter += 1
        return temp_name

    def new_label(self):
        label_name = f'L{self.label_counter}'
        self.label_counter += 1
        return label_name

    def codegen_stmts(self, stmts):
        for stmt in stmts:
            match stmt:
                case ('assign', lvalue, expr):
                    temp_name = self.new_temp()
                    #temp_expr = self.codegen_expr(expr, temp_name)
                    self.code.append(('assign', lvalue, temp_name))
                case ('call', lvalue, func, args):
                    temp_args = [self.codegen_expr(arg) for arg in args]
                    self.code.append(('call', lvalue, func, temp_args))
                case ('return', expr):
                    temp_expr = self.codegen_expr(expr)
                    self.code.append(('return', temp_expr))
                case ('print', rvalue):
                    temp_name = self.new_temp()
                    self.codegen_expr(rvalue, temp_name)
                    self.code.append(('print', temp_name))
                case ('read', lvalue):
                    self.code.append(('read', lvalue))
                case ('if', cond, then_stmts, else_stmts):
                    self.codegen_if(cond, then_stmts, else_stmts)
                case ('while', cond, body):
                    self.codegen_while(cond, body)
                case ('skip', ):
                    self.code.append(('skip',))

    def codegen_expr(self, expr, temp_name):
        match expr:
            case ('number', value):
                self.code.append(('const', temp_name, value))
                self.new_temp()
                return value
            case ('var', name):
                return name
            case (op, left, right) if op in ['+', '-', '*', '/', '==', '<=', '>=', '<', '>']:
                left_temp = self.codegen_expr(left)
                right_temp = self.codegen_expr(right)
                temp = self.new_temp()
                self.code.append((op, temp, left_temp, right_temp))
                return temp
        return expr

    def codegen_temp_expr(self, value):
        temp = self.new_temp()
        self.code.append(('const', temp, value))
        return temp

    def codegen_if(self, cond, then_stmts, else_stmts):
        temp_cond = self.codegen_expr(cond)
        then_label = self.new_label()
        else_label = self.new_label()
        end_label = self.new_label()

        self.code.append(('branch', temp_cond, then_label, else_label))
        self.code.append(('label', then_label))
        self.codegen_stmts(then_stmts)
        self.code.append(('jump', end_label))
        self.code.append(('label', else_label))
        self.codegen_stmts(else_stmts)
        self.code.append(('label', end_label))

    def codegen_while(self, cond, body):
        start_label = self.new_label()
        cond_label = self.new_label()
        body_label = self.new_label()
        end_label = self.new_label()

        self.code.append(('jump', cond_label))
        self.code.append(('label', start_label))
        self.codegen_stmts(body)
        self.code.append(('label', cond_label))
        temp_cond = self.codegen_expr(cond)
        self.code.append(('branch', temp_cond, body_label, end_label))
        self.code.append(('label', body_label))
        self.codegen_stmts(body)
        self.code.append(('jump', cond_label))
        self.code.append(('label', end_label))

# End of TODO


# As discussed, `CodeGen` is designed to iteratively
# apply the previously defined `CodeGenFunc` to each
# function in the program.
#
# Please note that you do not need to strictly follow
# this class structure if you can implement the code
# generation using a different approach, as long as you
# maintain the top-level interface and correctly pass
# all test cases. However, adhering to this interface
# might be easier than defining all parts from scratch.
class CodeGen:

    def __init__(self, gvars, funcs):
        self.gvars = gvars
        self.codes = {}
        for (f, (parameters, constants, _, ast)) in funcs.items():
            code_gen_func = CodeGenFunc(constants, ast)
            self.codes[f] = (parameters, code_gen_func.code)

    def pretty_printer(self):
        lines = []

        for (variable, value) in self.gvars.items():
            lines.append(f'{variable} := {value}')
        lines.append('')

        for (f, (parameters, code)) in self.codes.items():
            pparams = ', '.join(parameters)
            lines.append(f'func {f}({pparams}) {{')
            for instructions in code:
                match instructions:
                    case ('const', lvalue, rvalue):
                        lines.append(f'\t{lvalue} <- {rvalue}')
                    case ('read', lvalue):
                        lines.append(f'\t{lvalue} <- read')
                    case ('print', rvalue):
                        lines.append(f'\tprint {rvalue}')
                    case ('assign', lvalue, rvalue):
                        lines.append(f'\t{lvalue} <- {rvalue}')
                    case ('call', lvalue, function_name, args):
                        pargs = ', '.join(args)
                        lines.append(
                            f'\t{lvalue} <- call {function_name}({pargs})')
                    case ('return', rvalue):
                        lines.append(f'\treturn {rvalue}')
                    case ('label', label_name):
                        lines.append(f'{label_name}:')
                    case ('branch', bexpr, label_name1, label_name2):
                        lines.append(
                            f'\tbranch {bexpr} {label_name1} {label_name2}')
                    case ('jump', label_name):
                        lines.append(f'\tjump {label_name}')
                    case (op, lvalue, rvalue1,
                          rvalue2) if op in ['+', '-', '*', '/', '%']:
                        lines.append(f'\t{lvalue} <- {rvalue1} {op} {rvalue2}')
                    case (op, lvalue, rvalue1, rvalue2) if op in ['or', 'and']:
                        lines.append(f'\t{lvalue} <- {rvalue1} {op} {rvalue2}')
                    case (op, lvalue, rvalue1,
                          rvalue2) if op in ['==', '/=', '<', '<=', '>', '>=']:
                        lines.append(f'\t{lvalue} <- {rvalue1} {op} {rvalue2}')
            lines.append('}')
            lines.append('')
        return '\n'.join(lines)


# Below is the code to run the `CodeGen`.
# Your implementation should work properly with the following interface.
import ply.lex as lex
import ply.yacc as yacc
import lexer
import parser
import resolver
import sys


def main(filename):
    file_obj = open(filename, "r")
    inputs = file_obj.read()
    file_obj.close()
    lexer.lexer.lineno = 1
    ast = parser.parser.parse(inputs)
    r = resolver.Resolver(ast)
    cg = CodeGen(r.gvars, r.funcs)
    print(cg.pretty_printer())


if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
