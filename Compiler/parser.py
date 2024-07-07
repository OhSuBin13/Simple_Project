"""
__author__ = "Jieung Kim et al."
__copyright__ = "Copyright 2024, Jieung Kim et al."
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Jieung Kim"
__email__ = "jieungkim@inha.ac.kr"
"""
# This file implements a parser for ToyPL, which is described in our README file.
import ply.yacc as yacc
import ply.lex as lex
from lexer import *
import sys

###############################################################
# Program
###############################################################
def p_program(p):
    # TODO(num: 1/37): modify and fill out the parsing rule for  
    # PROGRAM -> NAMESPACE_DECS CONST_DECS VAR_DECS FUNC_DECS
    """
    program : namespace_decs const_decs var_decs func_decs
    """
    # End of TODO(num: 1/23). Do not touch the remaining lines in this function.
    p[0] = ("program", p[1], p[2], p[3], p[4])

###############################################################
# Namespace
###############################################################
def p_namespace_decs(p):
    # TODO(num: 2/37): modify and fill out the parsing rule for
    # NAMESPACE_DECS -> E | NAMESPACE_DEC NAMESPACE_DECS
    """
    namespace_decs : empty
                   | namespace_dec namespace_decs
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[1], *p[2]]

def p_namespace_dec(p):
    # TODO(num: 3/37): modify and fill out the parsing rule for
    # NAMESPACE_DEC -> "namespace" NIDENT NAMESPACE_DECS CONST_DECS VAR_DECS FUNC_DECS "end"
    """
    namespace_dec : NAMESPACE NIDENT namespace_decs const_decs var_decs func_decs END
    """
    p[0] = ("namespace", p[2], p[3], p[4], p[5], p[6])

###############################################################
# Constants
###############################################################
def p_const_decs(p):
    # TODO(num: 4/37): modify and fill out the parsing rule for
    # CONST_DECS -> E | "const" CONSTS
    """
    const_decs : empty
               | CONST consts
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = p[2]

def p_consts(p):
    # TODO(num: 5/37): modify and fill out the parsing rule for
    # CONSTS -> LIDENT ":=" NUMBER | LIDENT ":=" NUMBER "," CONSTS
    """
    consts : LIDENT DEFINE NUMBER
            | LIDENT DEFINE NUMBER COMMA consts
    """
    if len(p) == 4:
        p[0] = [(p[1], p[3])]
    else:
        p[0] = [(p[1], p[3]), *p[5]]

###############################################################
# Variables
###############################################################
def p_var_decs(p):
    # TODO(num: 6/37): modify and fill out the parsing rule for
    # VAR_DECS -> E | "var" VARS
    """
    var_decs : empty
             | VAR vars
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = p[2]

def p_vars(p):
    # TODO(num: 7/37): modify and fill out the parsing rule for
    # VARS -> LIDENT | LIDENT "," VARS
    """
    vars : LIDENT
         | LIDENT COMMA vars
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1], *p[3]]

###############################################################
# Functions
###############################################################
def p_func_decs(p):
    # TODO(num: 8/37): modify and fill out the parsing rule for
    # FUNC_DECS -> E | FUNC_DEC FUNC_DECS
    """
    func_decs : empty
              | func_dec func_decs
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[1], *p[2]]

def p_func_dec(p):
    # TODO(num: 9/37): modify and fill out the parsing rule for
    # FUNC_DEC -> "func" LIDENT "(" PARAMS ")" CONST_DECS VAR_DECS "begin" STMTS "end"
    """
    func_dec : FUNC LIDENT LPAR params RPAR const_decs var_decs BEGIN stmts END
    """
    p[0] = ("func", p[2], p[4], p[6], p[7], p[9])

def p_params(p):
    # TODO(num: 10/37): modify and fill out the parsing rule for
    # PARAMS -> E | LIDENT PARAMS_TAIL
    """
    params : empty
           | LIDENT params_tail
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[1], *p[2]]

def p_params_tail(p):
    # TODO(num: 11/37): modify and fill out the parsing rule for
    # PARAMS_TAIL -> E | "," LIDENT PARAMS_TAIL
    """
    params_tail : empty
                | COMMA LIDENT params_tail
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[2], *p[3]]

###############################################################
# Statement definitions
###############################################################
def p_stmt_skip(p):
    # TODO(num: 12/37): modify and fill out the parsing rule for 
    # STMT -> "skip"
    """
    skip_stmt : SKIP
    """
    p[0] = ("skip",)

def p_stmt_read(p):
    # TODO(num: 13/37): modify and fill out the parsing rule for
    # STMT -> IDENT "<-" "read"
    """
    read_stmt : abs_ident ASSIGN READ
              | rel_ident ASSIGN READ
    """
    p[0] = ("read", p[1])

def p_stmt_print(p):
    # TODO(num: 14/37): modify and fill out the parsing rule for
    # STMT -> "print" "(" EXPR ")"
    """
    print_stmt : PRINT LPAR expr RPAR
    """
    p[0] = ("print", p[3])

def p_stmt_assign(p):
    # TODO(num: 15/37): modify and fill out the parsing rule for
    # STMT -> IDENT "<-" EXPR
    """
    ident_stmt : abs_ident ASSIGN expr
                | rel_ident ASSIGN expr
    """
    p[0] = ("assign", p[1], p[3])

def p_stmt_call(p):
    # TODO(num: 16/37): modify and fill out the parsing rule for
    # STMT -> IDENT "<-" "call" IDENT "(" ARGS ")"
    """
    call_stmt : abs_ident ASSIGN CALL abs_ident LPAR args RPAR
                | abs_ident ASSIGN CALL rel_ident LPAR args RPAR
                | rel_ident ASSIGN CALL abs_ident LPAR args RPAR
                | rel_ident ASSIGN CALL rel_ident LPAR args RPAR
    """
    p[0] = ("call", p[1], p[4], p[6])

def p_stmt_if(p):
    # TODO(num: 17/37): modify and fill out the parsing rule for
    # STMT -> "if" BEXPR "then" STMT "else" STMT
    """
    if_stmt : IF bexpr THEN skip_stmt ELSE skip_stmt
            | IF bexpr THEN skip_stmt ELSE read_stmt
            | IF bexpr THEN skip_stmt ELSE print_stmt
            | IF bexpr THEN skip_stmt ELSE ident_stmt
            | IF bexpr THEN skip_stmt ELSE call_stmt
            | IF bexpr THEN skip_stmt ELSE if_stmt
            | IF bexpr THEN skip_stmt ELSE while_stmt
            | IF bexpr THEN skip_stmt ELSE return_stmt
            | IF bexpr THEN skip_stmt ELSE stmt
            | IF bexpr THEN read_stmt ELSE skip_stmt
            | IF bexpr THEN read_stmt ELSE read_stmt
            | IF bexpr THEN read_stmt ELSE print_stmt
            | IF bexpr THEN read_stmt ELSE ident_stmt
            | IF bexpr THEN read_stmt ELSE call_stmt
            | IF bexpr THEN read_stmt ELSE if_stmt
            | IF bexpr THEN read_stmt ELSE while_stmt
            | IF bexpr THEN read_stmt ELSE return_stmt
            | IF bexpr THEN read_stmt ELSE stmt
            | IF bexpr THEN print_stmt ELSE skip_stmt
            | IF bexpr THEN print_stmt ELSE read_stmt
            | IF bexpr THEN print_stmt ELSE print_stmt
            | IF bexpr THEN print_stmt ELSE ident_stmt
            | IF bexpr THEN print_stmt ELSE call_stmt
            | IF bexpr THEN print_stmt ELSE if_stmt
            | IF bexpr THEN print_stmt ELSE while_stmt
            | IF bexpr THEN print_stmt ELSE return_stmt
            | IF bexpr THEN print_stmt ELSE stmt
            | IF bexpr THEN ident_stmt ELSE skip_stmt
            | IF bexpr THEN ident_stmt ELSE read_stmt
            | IF bexpr THEN ident_stmt ELSE print_stmt
            | IF bexpr THEN ident_stmt ELSE ident_stmt
            | IF bexpr THEN ident_stmt ELSE call_stmt
            | IF bexpr THEN ident_stmt ELSE if_stmt
            | IF bexpr THEN ident_stmt ELSE while_stmt
            | IF bexpr THEN ident_stmt ELSE return_stmt
            | IF bexpr THEN ident_stmt ELSE stmt
            | IF bexpr THEN call_stmt ELSE skip_stmt
            | IF bexpr THEN call_stmt ELSE read_stmt
            | IF bexpr THEN call_stmt ELSE print_stmt
            | IF bexpr THEN call_stmt ELSE ident_stmt
            | IF bexpr THEN call_stmt ELSE call_stmt
            | IF bexpr THEN call_stmt ELSE if_stmt
            | IF bexpr THEN call_stmt ELSE while_stmt
            | IF bexpr THEN call_stmt ELSE return_stmt
            | IF bexpr THEN call_stmt ELSE stmt
            | IF bexpr THEN if_stmt ELSE skip_stmt
            | IF bexpr THEN if_stmt ELSE read_stmt
            | IF bexpr THEN if_stmt ELSE print_stmt
            | IF bexpr THEN if_stmt ELSE ident_stmt
            | IF bexpr THEN if_stmt ELSE call_stmt
            | IF bexpr THEN if_stmt ELSE if_stmt
            | IF bexpr THEN if_stmt ELSE while_stmt
            | IF bexpr THEN if_stmt ELSE return_stmt
            | IF bexpr THEN if_stmt ELSE stmt
            | IF bexpr THEN while_stmt ELSE skip_stmt
            | IF bexpr THEN while_stmt ELSE read_stmt
            | IF bexpr THEN while_stmt ELSE print_stmt
            | IF bexpr THEN while_stmt ELSE ident_stmt
            | IF bexpr THEN while_stmt ELSE call_stmt
            | IF bexpr THEN while_stmt ELSE if_stmt
            | IF bexpr THEN while_stmt ELSE while_stmt
            | IF bexpr THEN while_stmt ELSE return_stmt
            | IF bexpr THEN while_stmt ELSE stmt
            | IF bexpr THEN return_stmt ELSE skip_stmt
            | IF bexpr THEN return_stmt ELSE read_stmt
            | IF bexpr THEN return_stmt ELSE print_stmt
            | IF bexpr THEN return_stmt ELSE ident_stmt
            | IF bexpr THEN return_stmt ELSE call_stmt
            | IF bexpr THEN return_stmt ELSE if_stmt
            | IF bexpr THEN return_stmt ELSE while_stmt
            | IF bexpr THEN return_stmt ELSE return_stmt
            | IF bexpr THEN return_stmt ELSE stmt
            | IF bexpr THEN stmt ELSE skip_stmt
            | IF bexpr THEN stmt ELSE read_stmt
            | IF bexpr THEN stmt ELSE print_stmt
            | IF bexpr THEN stmt ELSE ident_stmt
            | IF bexpr THEN stmt ELSE call_stmt
            | IF bexpr THEN stmt ELSE if_stmt
            | IF bexpr THEN stmt ELSE while_stmt
            | IF bexpr THEN stmt ELSE return_stmt
            | IF bexpr THEN stmt ELSE stmt
    """
    p[0] = ("if", p[2], p[4], p[6])

def p_stmt_while(p):
    # TODO(num: 18/37): modify and fill out the parsing rule for
    # STMT -> "while" BEXPR "do" STMT
    """
    while_stmt : WHILE bexpr DO skip_stmt
                | WHILE bexpr DO read_stmt
                | WHILE bexpr DO print_stmt
                | WHILE bexpr DO ident_stmt
                | WHILE bexpr DO call_stmt
                | WHILE bexpr DO if_stmt
                | WHILE bexpr DO while_stmt
                | WHILE bexpr DO return_stmt
                | WHILE bexpr DO stmt
    """
    p[0] = ("while", p[2], p[4])

def p_stmt_return(p):
    # TODO(num: 19/37): modify and fill out the parsing rule for
    # STMT -> "return" EXPR
    """
    return_stmt : RETURN expr
    """
    p[0] = ("return", p[2])

def p_stmt_stmts(p):
    # TODO(num: 20/37): modify and fill out the parsing rule for
    # STMT -> "{" STMTS "}"
    """
    stmt : LBRC stmts RBRC
    """
    p[0] = ("stmts", p[2])

def p_stmts(p):
    # TODO(num: 21/37): modify and fill out the parsing rule for
    # STMTS -> STMT | STMT ";" | STMT ";" STMTS
    """
    stmts :  skip_stmt
            | skip_stmt SEMICOLON
            | skip_stmt SEMICOLON stmts
            | read_stmt
            | read_stmt SEMICOLON
            | read_stmt SEMICOLON stmts
            | print_stmt
            | print_stmt SEMICOLON
            | print_stmt SEMICOLON stmts
            | ident_stmt
            | ident_stmt SEMICOLON
            | ident_stmt SEMICOLON stmts
            | call_stmt
            | call_stmt SEMICOLON
            | call_stmt SEMICOLON stmts
            | if_stmt
            | if_stmt SEMICOLON
            | if_stmt SEMICOLON stmts
            | while_stmt
            | while_stmt SEMICOLON
            | while_stmt SEMICOLON stmts
            | return_stmt
            | return_stmt SEMICOLON
            | return_stmt SEMICOLON stmts
            | stmt
            | stmt SEMICOLON
            | stmt SEMICOLON stmts
    """
    if len(p) == 2 or len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1], *p[3]]

def p_args(p):
    # TODO(num: 22/37): modify and fill out the parsing rule for
    # ARGS -> E | EXPR ARGS_TAIL
    """
    args : empty
        | expr args_tail
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[1], *p[2]]

def p_args_tail(p):
    # TODO(num: 23/37): modify and fill out the parsing rule for
    # ARGS_TAIL -> E | "," EXPR ARGS
    """
    args_tail : empty
            | COMMA expr args
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[2], *p[3]]

###############################################################
# Boolean expressions
###############################################################
def p_cmp_op(p):
    # TODO(num: 24/37): modify and fill out the parsing rule for
    # CMP_OP -> "==" | "/=" | "<" | "<=" | ">" | ">="
    """
    cmp_op : EQ
        | NE
        | LT
        | LE
        | GT
        | GE
    """
    p[0] = p[1]

def p_bexpr(p):
    # TODO(num: 25/37): modify and fill out the parsing rule for
    # BEXPR -> BTERM | BEXPR "||" BTERM
    """
    bexpr : bterm
        | bexpr OR bterm
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ("or", p[1], p[3])

def p_bterm(p):
    # TODO(num: 26/37): modify and fill out the parsing rule for
    # BTERM -> BFACTOR | BTERM "&&" BFACTOR
    """
    bterm : cmp_bfactor
        | bterm AND cmp_bfactor
        | bexpr_bfactor
        | bterm AND bexpr_bfactor
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ("and", p[1], p[3])

def p_bfactor_cmp(p):
    # TODO(num: 27/37): modify and fill out the parsing rule for
    # BFACTOR -> EXPR CMP_OP EXPR
    """
    cmp_bfactor : expr cmp_op expr
    """
    p[0] = (p[2], p[1], p[3])

def p_bfactor_bexpr(p):
    # TODO(num: 28/37): modify and fill out the parsing rule for
    # BFACTOR -> "(" BEXPR ")"
    """
    bexpr_bfactor : LPAR bexpr RPAR
    """
    p[0] = p[2]

###############################################################
# Arithmetic expressions
###############################################################
def p_expr(p):
    # TODO(num: 29/37): modify and fill out the parsing rule for
    # EXPR -> TERM | EXPR "+" TERM | EXPR "-" TERM
    """
    expr : term
        | expr PLUS term
        | expr MINUS term
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_term(p):
    # TODO(num: 30/37): modify and fill out the parsing rule for
    # TERM -> FACTOR | TERM "*" FACTOR | TERM "/" FACTOR | TERM "%" FACTOR
    """
    term : ident_factor
        | term MUL ident_factor
        | term DIV ident_factor
        | term MOD ident_factor
        | number_factor
        | term MUL number_factor
        | term DIV number_factor
        | term MOD number_factor
        | expr_factor
        | term MUL expr_factor
        | term DIV expr_factor
        | term MOD expr_factor
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_factor_ident(p):
    # TODO(num: 31/37): modify and fill out the parsing rule for
    # FACTOR -> IDENT  
    """
    ident_factor : abs_ident
                  | rel_ident
    """
    p[0] = ("var", p[1])

def p_factor_number(p):
    # TODO(num: 32/37): modify and fill out the parsing rule for
    # FACTOR -> NUMBER   
    """
    number_factor : NUMBER
    """
    p[0] = ("number", p[1])

def p_factor_expr(p):
    # TODO(num: 33/37): modify and fill out the parsing rule for
    # FACTOR ->  "(" EXPR ")"
    """
    expr_factor : LPAR expr RPAR
    """
    p[0] = p[2]

###############################################################
# Identifiers
###############################################################
def p_ident_abs(p):
    # TODO(num: 34/37): modify and fill out the parsing rule for
    # IDENT -> ABS_PATH LIDENT 
    """
    abs_ident : abs_path LIDENT
    """
    p[0] = ("abs", p[1], p[2])

def p_ident_rel(p):
    # TODO(num: 35/37): modify and fill out the parsing rule for
    # IDENT -> REL_PATH LIDENT
    """
    rel_ident : rel_path LIDENT
    """
    p[0] = ("rel", p[1], p[2])

def p_abs_path(p):
    # TODO(num: 36/37): modify and fill out the parsing rule for
    # ABS_PATH -> ":" REL_PATH
    """
    abs_path : COLON rel_path
    """
    p[0] = p[2]

def p_rel_path(p):
    # TODO(num: 37/37): modify and fill out the parsing rule for
    # REL_PATH -> E | NIDENT "." REL_PATH
    """
    rel_path : empty
            | NIDENT PERIOD rel_path
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[1], *p[3]]


###############################################################
# NOTE: do not touch the remaining parts of this file.
###############################################################
###############################################################
# Empty and error rules
###############################################################
def p_empty(p):
    """
    empty :
    """

def p_error(p):
    print("Error in line {0}".format(p))

###############################################################
# Generate the parser and test it
###############################################################
parser = yacc.yacc()

def main(filename):
    file_obj = open(filename, "r")
    inputs = file_obj.read()
    file_obj.close()
    ast = parser.parse(inputs)
    print(ast)

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
