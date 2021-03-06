#!/usr/bin/python

from __future__ import print_function
import scanner
import ply.yacc as yacc

tokens = scanner.tokens


precedence = (
    ('nonassoc', 'IF'),
    ('nonassoc', 'ELSE'),
    ('right', '=', 'PLUSASSIGN', 'MINUSASSIGN', 'TIMESASSIGN', 'DIVIDEASSIGN'),
    ('nonassoc', '<', '>', 'EQUAL', 'NOTEQUAL', 'GREATERTHANEQ', 'LESSTHANEQ'),
    ('left', '+', '-'),
    ('left', 'DOTPLUS', 'DOTMINUS'),
    ('left', '*', '/'),
    ('left', 'DOTTIMES', 'DOTDIVIDE'),
    ('right', 'UMINUS'),
    ('right', '\''),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")

# -------------------------
# Main productions
# -------------------------


def p_instructions(p):
    """instructions : instruction
                    | instruction instructions"""


def p_instruction(p):
    """instruction : block
                   | conditional
                   | loop
                   | statement ';'
                   | error ';'"""


def p_statement(p):
    """statement : assignment
                 | flow_keyword
                 | return
                 | print"""


def p_flow_keyword(p):
    """flow_keyword : BREAK
                    | CONTINUE"""


def p_expression(p):
    """expression : comparison_expression
                  | numeric_expression"""


def p_block(p):
    """block : '{' instructions '}'
             | '{' error '}'"""


def p_print(p):
    """print : PRINT print_body"""


def p_print_body(p):
    """print_body : string
                  | expression
                  | string ',' print_body
                  | expression ',' print_body"""


def p_return(p):
    """return : RETURN expression
              | RETURN"""


def p_string(p):
    """string : STRING"""

# -------------------------
# Matrices
# -------------------------


def p_vector(p):
    """vector : '[' vector_body ']'
              | '[' ']'"""


def p_vector_body(p):
    """vector_body : numeric_expression
                   | vector_body ',' numeric_expression"""


def p_matrix(p):
    """matrix : '[' matrix_body ']'
              | '[' ']'"""


def p_matrix_body(p):
    """matrix_body : vector
                   | matrix_body ',' vector"""


# -------------------------
# Arrays
# -------------------------

def p_array_range(p):
    """array_range : var '[' expression ',' expression ']'"""


# -------------------------
# Funs
# -------------------------

def p_fun(p):
    """fun : fun_name '(' numeric_expression ')'
           | fun_name '(' error ')'"""


def p_fun_name(p):
    """fun_name : ZEROS
                | ONES
                | EYE"""


# -------------------------
# Loops
# -------------------------

def p_loop(p):
    """loop : while
            | for"""


def p_while(p):
    """while : WHILE '(' expression ')' instruction"""


def p_for(p):
    """for : FOR ID '=' numeric_expression ':' numeric_expression instruction"""


# -------------------------
# If statements
# -------------------------

def p_conditional(p):
    """conditional : IF '(' expression ')' instruction %prec IF
                   | IF '(' expression ')' instruction ELSE instruction"""


# -------------------------
# Assignments
# -------------------------

def p_assignment_lhs(p):
    """assignment_lhs : var
                      | array_range"""


def p_assignment(p):
    """assignment : assignment_lhs assignment_operator expression
                  | assignment_lhs '=' string"""


def p_assignment_operator(p):
    """assignment_operator : '='
                           | PLUSASSIGN
                           | MINUSASSIGN
                           | TIMESASSIGN
                           | DIVIDEASSIGN"""


# -------------------------
# Numerics and variables
# -------------------------

def p_var(p):
    """var : ID
           | var '[' numeric_expression ']'"""


def p_num(p):
    """num : INTNUM
           | FLOATNUM
           | var"""


# -------------------------
# Numeric expressions
# -------------------------

def p_unary_op(p):
    """unary_op : negation
                | transposition"""


def p_neg(p):
    """negation : '-' numeric_expression %prec UMINUS"""


def p_transposition(p):
    r"""transposition : numeric_expression '\''"""


def p_numeric_expression(p):
    """numeric_expression : num
                          | matrix
                          | unary_op
                          | fun
                          | '(' numeric_expression ')'"""


def p_bin_numeric_expression(p):
    """numeric_expression : numeric_expression '+' numeric_expression
                          | numeric_expression '-' numeric_expression
                          | numeric_expression '*' numeric_expression
                          | numeric_expression '/' numeric_expression
                          | numeric_expression DOTPLUS numeric_expression
                          | numeric_expression DOTMINUS numeric_expression
                          | numeric_expression DOTTIMES numeric_expression
                          | numeric_expression DOTDIVIDE numeric_expression"""


# -------------------------
# Binary comparisons expressions
# -------------------------

def p_comparison_expression(p):
    """comparison_expression : numeric_expression '<' numeric_expression
           | numeric_expression '>' numeric_expression
           | numeric_expression EQUAL numeric_expression
           | numeric_expression NOTEQUAL numeric_expression
           | numeric_expression GREATERTHANEQ numeric_expression
           | numeric_expression LESSTHANEQ numeric_expression
           | '(' comparison_expression ')'"""


parser = yacc.yacc(debug=True)
