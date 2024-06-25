"""
__author__ = "Jieung Kim"
__copyright__ = "Copyright 2023, Jieung Kim"
__credits__ = ["Jieung Kim"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Jieung Kim"
__email__ = "jieungkim@inha.ac.kr"
"""
# This file implements a lexer for ToyPL, which is described in our README file.
import ply.lex as lex
import sys

# Reserved keywords and token definitions. You should not touch them.
reserved = {
    "namespace" : "NAMESPACE",
    "const"     : "CONST",
    "var"       : "VAR",
    "func"      : "FUNC",
    "begin"     : "BEGIN",
    "end"       : "END",
    "skip"      : "SKIP",
    "read"      : "READ",
    "print"     : "PRINT",
    "call"      : "CALL",
    "if"        : "IF",
    "then"      : "THEN",
    "else"      : "ELSE",
    "while"     : "WHILE",
    "do"        : "DO",
    "return"    : "RETURN"
}

tokens = [
    # separators
    "COMMA",     # ,
    "COLON",     # :
    "SEMICOLON", # ;
    "PERIOD",    # .
    "LPAR",      # (
    "RPAR",      # )
    "LBRC",      # {
    "RBRC",      # }
    # arithmetic operators
    "PLUS",      # +
    "MINUS",     # -
    "MUL",       # *
    "DIV",       # /
    "MOD",       # %
    # comparison operators
    "EQ",        # ==
    "NE",        # /=
    "LT",        # <
    "LE",        # <=
    "GT",        # >
    "GE",        # >=
    # boolean operators
    "OR",        # ||
    "AND",       # &&
    # assignments
    "DEFINE",    # :=
    "ASSIGN",    # <-
    # tokens that has to be defined with action functions
    "NIDENT",
    "LIDENT",
    "NUMBER",
] + list(reserved.values())

################################################################
# HW1 part start
# MODIFY THE FOLLOWING PARTS AND FILL OUT WITH YOUR OWN DEFINITIONS
################################################################
t_COMMA = r"\,"
t_COLON = r"\:"
t_SEMICOLON = r"\;"
t_PERIOD = r"."
t_LPAR = r"\("
t_RPAR = r"\)"
t_LBRC = r"\{"
t_RBRC = r"\}"
t_PLUS = r"\+"
t_MINUS = r"\-"
t_MUL = r"\*"
t_DIV = r"\/"
t_MOD = r"\%"
t_EQ = r"\=="
t_NE = r"\/="
t_LT = r"\<"
t_LE = r"\<="
t_GT = r"\>"
t_GE = r"\>="
t_OR = r"\|\|"
t_AND = r"&&"
t_DEFINE = r"\:="
t_ASSIGN = r"\<-"
t_NIDENT = r'[A-Z][a-zA-Z_0-9]*'
t_LIDENT = r'[a-z_][a-zA-Z_0-9]*'
t_ignore = " \t"

def t_RESERVED(t):
    r'[a-z_][a-zA-Z_0-9]*' # Identifiers can't start with a digit
    t.type = reserved.get(t.value, 'LIDENT')  # Check for reserved word
    return t

def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_comment(t):
    r'\#.*' # Check comment line
    pass


################################################################
# HW1 part end"
################################################################

# Do not touch after this line
# Create a lexer
lexer = lex.lex()


def lex_str(s):
    lexer.input(s)
    lexer.lineno = 1
    ts = []
    while True:
        t = lexer.token()
        if t:
            ts.append(t)
        else:
            lexer.lineno = 1
            return ts


def main(filename):
    file_obj = open(filename, "r")
    inputs = file_obj.read()
    file_obj.close()
    tok_list = lex_str(inputs)
    print(tok_list)


if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
