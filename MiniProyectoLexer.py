import ply.lex as lex

# Lista de tokens 
tokens = (
    'LBRACE',      # {
    'RBRACE',      # }
    'LBRACKET',    # [
    'RBRACKET',    # ]
    'COLON',       # :
    'COMMA',       # ,
    'STRING',      # "texto"
    'NUMBER',      # 123, 45.67
)

# Tokens simples 
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COLON = r':'
t_COMMA = r','

# Ignorar espacios en blanco, tabs y saltos de línea
t_ignore = ' \t\n\r'

# String - expresión regular para cadenas entre comillas dobles
# Permite cualquier carácter excepto comillas o backslash sin escapar
def t_STRING(t):
    r'"([^"\\]|\\["\\/bfnrt]|\\u[0-9a-fA-F]{4})*"'
    t.value = t.value[1:-1]  # Remover las comillas
    return t

# Número - expresión regular para enteros y decimales (positivos y negativos)
def t_NUMBER(t):
    r'-?([0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?)'
    if '.' in t.value or 'e' in t.value or 'E' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# Manejo de errores léxicos
def t_error(t):
    print(f"Carácter ilegal: '{t.value[0]}' en posición {t.lexpos}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()
