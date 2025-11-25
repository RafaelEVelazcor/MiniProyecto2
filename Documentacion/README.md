# MiniProyecto 2 - Parser JSON a TOON

## Descripción del Proyecto

Este proyecto implementa un analizador léxico y sintáctico (parser) para archivos JSON que convierte registros a formato TOON (Token Object Oriented Notation). El parser está construido manualmente usando PLY (Python Lex-Yacc) sin utilizar librerías de lectura automática JSON.

**Característica clave**: Todas las reglas gramaticales utilizan **EXCLUSIVAMENTE p[0]** para concatenar valores, sin variables intermedias ni funciones universales.

## Características Implementadas

### 1. Base de Datos JSON
- **Archivo**: `MiniProyecto.json`
- **Registros**: 20 empleados
- **Campos normales**: 4 campos (empleado_id, nombre, departamento, salario)
- **Objeto anidado**: direccion{calle, ciudad}
- **Aplicación real**: Sistema de gestión de empleados con llaves compuestas (empleado_id como identificador único)

### 2. Análisis Léxico (MiniProyectoLexer.py)
Implementa tokens mediante expresiones regulares (ER):

- **STRING**: `r'"([^"\\]|\\["\\/bfnrt]|\\u[0-9a-fA-F]{4})*"'`
  - Reconoce cadenas con caracteres escapados y Unicode
  
- **NUMBER**: `r'-?([0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?)'`
  - Reconoce enteros, decimales y notación científica
  
- **Estructurales**: `{`, `}`, `[`, `]`, `:`, `,`

### 3. Análisis Sintáctico (MiniProyectoyacc.py)
Reglas gramaticales específicas con **concatenación SOLO en p[0]**:

**Regla inicial:**
```python
def p_json(p):
    '''json : array_empleados'''
    p[0] = p[1]  # ← Devuelve TODOS los registros TOON concatenados
```

**Reglas para empleados:**
```python
def p_empleados_uno(p):
    '''empleados : empleado'''
    p[0] = p[1]

def p_empleados_varios(p):
    '''empleados : empleado COMMA empleados'''
    p[0] = p[1] + '\n' + p[3]  # ← Concatena con salto de línea en p[0]
```

**Regla para datos:**
```python
def p_datos_empleado(p):
    '''datos_empleado : dato_id COMMA dato_nombre COMMA dato_departamento COMMA dato_salario COMMA dato_direccion'''
    p[0] = p[1] + '|' + p[3] + '|' + p[5] + '|' + p[7] + '|' + p[9]
    # ↑ SOLO concatena en p[0], sin variables intermedias
```

**Regla para objeto anidado:**
```python
def p_objeto_direccion(p):
    '''objeto_direccion : LBRACE campo_calle COMMA campo_ciudad RBRACE'''
    p[0] = p[2] + '|' + p[4]  # ← Concatena solo en p[0]
```

**Reglas simples (sin variables):**
```python
def p_dato_id(p):
    '''dato_id : STRING COLON STRING'''
    p[0] = p[3].strip('"')  # ← Solo asigna a p[0]

def p_dato_nombre(p):
    '''dato_nombre : STRING COLON STRING'''
    p[0] = p[3].strip('"')  # ← Solo asigna a p[0]

def p_dato_salario(p):
    '''dato_salario : STRING COLON NUMBER'''
    p[0] = str(p[3])  # ← Solo asigna a p[0]
```

**Principio de implementación**:
- ✅ Todas las asignaciones van a `p[0]`
- ✅ Lectura de valores desde `p[1]`, `p[2]`, `p[3]`, etc.
- ❌ NO se usan variables intermedias
- ❌ NO se usan funciones universales de conversión
- ❌ SOLO concatenación directa en `p[0]`

### 4. Validación de Estructura
- Maneja campos faltantes o vacíos
- Mantiene el espacio en el formato de salida (campos vacíos se representan como `''`)
- Valida objetos anidados correctamente
- Ejemplo de salida con campos faltantes:
  ```
  EMP003||Tecnología||direccion{|Zapopan}
  ```

### 5. Conversión a Formato TOON (Pipe-Separated)
Formato compacto pipe-separated:

```
EMP001|Juan Pérez García|Ventas|45000.5|Av. Reforma 123|CDMX
EMP002|María López Hernández|Recursos Humanos|52000.0|Calle Juárez 456|Guadalajara
```

Características:
- Valores simples separados por `|` (pipe)
- Objeto anidado también con `|`
- Formato plano y compacto
- Inspirado en TOON (https://github.com/toon-format/toon)

### 6. Exportación a Archivo
- **Archivo de salida**: `salida.txt`
- **Garantía**: Mismo número de registros TOON que registros JSON (20 registros)
- **Encoding**: UTF-8 para soportar caracteres especiales en español

## Estructura de Archivos

```
MiniProyecto2/
├── MiniProyecto.json          # Base de datos JSON (20 empleados)
├── MiniProyectoLexer.py       # Analizador léxico con ER
├── MiniProyectoyacc.py        # Parser y conversor a TOON
├── salida.txt                 # Archivo de salida en formato TOON
├── Documentacion/
│   ├── README.md              # Este archivo
│   ├── RESUMEN.md             # Resumen de cumplimiento
│   └── FORMATO_TOON.md        # Especificación del formato
└── __pycache__/               # Cache de Python
```

## Ejecución

### Conversión completa de la base de datos:
```bash
python MiniProyectoyacc.py
```

Salida esperada:
```
✓ JSON válido
✓ Se generaron 20 registros TOON
  Registro 1: EMP001|Juan Pérez García|Ventas|45000.5|Av. Reforma 123|CDMX
  Registro 2: EMP002|María López Hernández|Recursos Humanos|52000.0|Calle Juárez 456|Guadalajara
  Registro 3: EMP003|Carlos Ramírez Torres|Tecnología|68000.75|Blvd. Zapopan 789|Zapopan
  ... (14 registros más)
  Registro 19: EMP019|Héctor Ríos Domínguez|Tecnología|75000.5|Blvd. Belisario 846|Zapopan
  Registro 20: EMP020|Isabel Núñez Aguilar|Operaciones|56000.75|Calle Allende 951|Querétaro

✓ Archivo 'salida.txt' generado
```

## Requisitos Cumplidos

✅ **Archivo JSON**: Base de datos realista de empleados con 20 registros
✅ **Lectura manual**: Sin usar `json.load()` u otras librerías automáticas
✅ **Campos mínimos**: 4 campos normales + 1 objeto anidado con 2 campos
✅ **Tokens con ER**: Todas las expresiones regulares implementadas correctamente
✅ **Reglas gramaticales**: Específicas para JSON, usando SOLO `p[0]`
✅ **Concatenación**: EXCLUSIVAMENTE mediante `p[0]`, sin variables ni funciones
✅ **Validación**: Manejo de campos faltantes/vacíos
✅ **Formato TOON**: Conversión compacta pipe-separated
✅ **Exportación**: Archivo TXT con mismo número de registros (20)

## Árbol de Variables (Parse Tree)

### Flujo de p[] en la ejecución:

```
1. p_campo_calle: STRING COLON STRING
   p[0] = p[3].strip('"')  → "Av. Reforma 123"

2. p_campo_ciudad: STRING COLON STRING
   p[0] = p[3].strip('"')  → "CDMX"

3. p_objeto_direccion: LBRACE campo_calle COMMA campo_ciudad RBRACE
   p[0] = p[2] + '|' + p[4]  → "Av. Reforma 123|CDMX"

4. p_dato_id: STRING COLON STRING
   p[0] = p[3].strip('"')  → "EMP001"

5. p_dato_nombre: STRING COLON STRING
   p[0] = p[3].strip('"')  → "Juan Pérez García"

6. p_datos_empleado: dato_id COMMA ... dato_direccion
   p[0] = p[1]+'|'+p[3]+'|'+p[5]+'|'+p[7]+'|'+p[9]
   → "EMP001|Juan Pérez García|Ventas|45000.5|Av. Reforma 123|CDMX"

7. p_empleado: LBRACE datos_empleado RBRACE
   p[0] = p[2]
   → "EMP001|Juan Pérez García|Ventas|45000.5|Av. Reforma 123|CDMX"

8. p_empleados_varios: empleado COMMA empleados
   p[0] = p[1] + '\n' + p[3]
   → concatena con salto de línea

9. p_json: array_empleados
   p[0] = p[1]
   → DEVUELVE TODO EL TEXTO CONCATENADO
```

## Tecnologías

- **Python 3.x**
- **PLY (Python Lex-Yacc)**: Para análisis léxico y sintáctico
- **Expresiones Regulares**: Para identificación de tokens
- **Strings**: Manipulación de texto solo en `p[0]`
