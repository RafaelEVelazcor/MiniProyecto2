# Formato TOON - Token Object Oriented Notation

## Referencia
https://github.com/toon-format/toon

## Características del Formato TOON

TOON es un formato de notación compacta para representar objetos estructurados de manera legible y eficiente.

### Principios TOON Aplicados en Este Proyecto

#### 1. Valores Simples
Los valores primitivos se separan con comas:
```
empleado_id, nombre, departamento, salario
```

**Ejemplo**:
```
EMP001, Juan Pérez García, Ventas, 45000.5
```

#### 2. Objetos Anidados
Los objetos se representan con la sintaxis `nombre{campo1, campo2, ...}`:
```
direccion{calle, ciudad}
```

**Ejemplo completo**:
```
EMP001, Juan Pérez García, Ventas, 45000.5, direccion{Av. Reforma 123, CDMX}
```

#### 3. Encabezado de Esquema
La primera línea define la estructura:
```
empleado_id, nombre, departamento, salario, direccion{calle, ciudad}
```

#### 4. Compacidad
- Sin espacios innecesarios dentro de objetos
- Separación clara con comas
- Mantiene legibilidad

## Comparación JSON vs TOON

### JSON (formato original):
```json
{
  "empleado_id": "EMP001",
  "nombre": "Juan Pérez García",
  "departamento": "Ventas",
  "salario": 45000.5,
  "direccion": {
    "calle": "Av. Reforma 123",
    "ciudad": "CDMX"
  }
}
```

**Tamaño**: ~180 caracteres (con formato)

### TOON (formato convertido):
```
EMP001, Juan Pérez García, Ventas, 45000.5, direccion{Av. Reforma 123, CDMX}
```

**Tamaño**: ~78 caracteres

**Reducción**: ~57% más compacto

## Ventajas del Formato TOON

1. **Compacto**: Reduce significativamente el tamaño de los datos
2. **Legible**: Fácil de leer para humanos
3. **Estructurado**: Mantiene la jerarquía de objetos
4. **Eficiente**: Ideal para logs, exports y transferencias

## Estructura de Datos en Este Proyecto

### Esquema TOON Implementado:
```
empleado_id, nombre, departamento, salario, direccion{calle, ciudad}
```

### Tipos de Datos:
- `empleado_id`: String (identificador único)
- `nombre`: String
- `departamento`: String
- `salario`: Number (decimal)
- `direccion`: Object
  - `calle`: String
  - `ciudad`: String

### Manejo de Valores Vacíos:
Los campos faltantes se representan con espacios vacíos pero mantienen su posición:

```
EMP003, , Tecnología, , direccion{, Zapopan}
        ↑            ↑           ↑
      vacío       vacío       vacío
```

Esto asegura que la estructura del esquema se mantenga consistente.

## Ejemplos de Salida

### Registro Completo:
```
EMP001, Juan Pérez García, Ventas, 45000.5, direccion{Av. Reforma 123, CDMX}
```

### Registro con Campos Faltantes:
```
EMP002, María López Hernández, , 52000.0, direccion{Calle Juárez 456, }
```

### Múltiples Registros:
```
empleado_id, nombre, departamento, salario, direccion{calle, ciudad}
EMP001, Juan Pérez García, Ventas, 45000.5, direccion{Av. Reforma 123, CDMX}
EMP002, María López Hernández, Recursos Humanos, 52000.0, direccion{Calle Juárez 456, Guadalajara}
EMP003, Carlos Ramírez Torres, Tecnología, 68000.75, direccion{Blvd. Zapopan 789, Zapopan}
```

## Extensibilidad

El formato TOON puede extenderse para soportar:
- Arrays: `etiquetas[tag1, tag2, tag3]`
- Objetos anidados profundos: `persona{nombre, direccion{calle, ciudad}}`
- Múltiples objetos: `info{id, name}, metadata{created, modified}`

Este proyecto implementa el subconjunto básico de TOON necesario para representar la estructura de empleados con un nivel de anidación.
