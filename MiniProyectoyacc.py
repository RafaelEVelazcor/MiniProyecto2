import ply.yacc as yacc
from MiniProyectoLexer import tokens

# Regla inicial - devuelve TODO concatenado en p[0]
def p_json(p):
    '''json : array_empleados'''
    p[0] = p[1]

# Regla para array de empleados
def p_array_empleados(p):
    '''array_empleados : LBRACKET empleados RBRACKET'''
    p[0] = p[2]

# Regla para empleados - puede ser uno o varios
def p_empleados_uno(p):
    '''empleados : empleado'''
    p[0] = p[1]

def p_empleados_varios(p):
    '''empleados : empleado COMMA empleados'''
    p[0] = p[1] + '\n' + p[3]

# Regla para un empleado
def p_empleado(p):
    '''empleado : LBRACE datos_empleado RBRACE'''
    p[0] = p[2]

# Regla para datos del empleado - concatena directamente en p[0]
def p_datos_empleado(p):
    '''datos_empleado : dato_id COMMA dato_nombre COMMA dato_departamento COMMA dato_salario COMMA dato_direccion'''
    p[0] = p[1] + '|' + p[3] + '|' + p[5] + '|' + p[7] + '|' + p[9]

# Extracción de campo: empleado_id
def p_dato_id(p):
    '''dato_id : STRING COLON STRING'''
    p[0] = p[3].strip('"')

# Extracción de campo: nombre
def p_dato_nombre(p):
    '''dato_nombre : STRING COLON STRING'''
    p[0] = p[3].strip('"')

# Extracción de campo: departamento
def p_dato_departamento(p):
    '''dato_departamento : STRING COLON STRING'''
    p[0] = p[3].strip('"')

# Extracción de campo: salario
def p_dato_salario(p):
    '''dato_salario : STRING COLON NUMBER'''
    p[0] = str(p[3])

# Extracción de campo: dirección (objeto anidado)
def p_dato_direccion(p):
    '''dato_direccion : STRING COLON objeto_direccion'''
    p[0] = p[3]

# Objeto dirección - concatena directamente en p[0]
def p_objeto_direccion(p):
    '''objeto_direccion : LBRACE campo_calle COMMA campo_ciudad RBRACE'''
    p[0] = p[2] + '|' + p[4]

# Campo calle
def p_campo_calle(p):
    '''campo_calle : STRING COLON STRING'''
    p[0] = p[3].strip('"')

# Campo ciudad
def p_campo_ciudad(p):
    '''campo_ciudad : STRING COLON STRING'''
    p[0] = p[3].strip('"')

# Manejo de errores
def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}'")
    else:
        print("Error de sintaxis: EOF inesperado")

parser = yacc.yacc(write_tables=False, debug=False)


# Función principal
if __name__ == "__main__":
    # Leer archivo JSON
    with open('MiniProyecto.json', 'r', encoding='utf-8') as file:
        input_string = file.read()
    
    # Parsear - p[0] de la regla inicial devuelve TODO concatenado
    resultado = parser.parse(input_string)
    
    if resultado:
        print("✓ JSON válido")
        
        # Contar líneas
        lineas = resultado.split('\n')
        print(f"✓ Se generaron {len(lineas)} registros TOON")
        
        # Escribir salida
        with open('salida.txt', 'w', encoding='utf-8') as output:
            output.write(resultado)
        
        print(f"✓ Archivo 'salida.txt' generado")
    else:
        print("Error al parsear JSON")
