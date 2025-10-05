<div style="background-color: #dbf5ffff;">

# <center> BASE DE DATOS TIENDA AURELION </center>

![Tienda Aurelion](https://www.leafio.ai/storage/common/attaches/00dae7ceacebaeca483ca84256ecb9d259cb5418.webp)

<div style="text-align: justify;">
La base de datos Aurelion está diseñada para gestionar la información de clientes, productos, ventas y detalles de ventas de manera eficiente. Especificamente esta base de datos gestiona un sistema comercial con 95 clientes de 6 ciudades, 100 productos en categorías de Alimentos y Limpieza, 120 transacciones de ventas registradas en 2024, y 343 líneas de detalle que capturan cantidades, precios e importes. Su estructura relacional permite análisis de clientes, productos, ventas temporales y métodos de pago para insights comerciales y machine learning.

A continuación, se presenta una descripción detallada de su estructura y características.
</div>

## 🏗️ ESTRUCTURA DE LA BASE DE DATOS

La base de datos Aurelion se compone de las siguientes tablas:

1. **Clientes**: Almacena información sobre los clientes, incluyendo datos demográficos y de contacto.
2. **Productos**: Contiene el catálogo de productos disponibles para la venta, con detalles como precios y descripciones.
3. **Ventas**: Registra las transacciones de venta, incluyendo información sobre el cliente, productos comprados y fecha de la venta.
4. **Detalles_Ventas**: Proporciona un desglose detallado de cada transacción de venta, incluyendo los productos específicos comprados y sus cantidades.

### Arquitectura General

```
AurelionDB
├── Clientes (100 registros)
├── Productos (100 registros)
├── Ventas (120 registros)
└── Detalles_Ventas (343 registros)
```

### Relaciones entre Tablas

```
Clientes (1) ←---→ (N) Ventas (1) ←---→ (N) Detalles_Ventas (N) ←---→ (1) Productos
```

## 📊 DETALLE ESTRUCTURAL POR TABLA

### 🏪 1. TABLA CLIENTES

- **Escala**: 95 clientes registrados (nombres únicos)
- **Cobertura temporal**: Enero 2023 - Abril 2023
- **Distribución geográfica**: 6 ciudades o municipios de Córdoba, Argentina

### 🏪 2. TABLA PRODUCTOS

- **Escala**: 100 productos registrados
- **Categorización**: 2 categorías principales (50 productos cada una)
- **Rango de precios**: Amplia variabilidad (valor mínimo = 272 y máximo = 4982)
- **Nota Importante**: Categorización inconsistente.Algunos productos como "Fernet", "Vino", "Cerveza" están categorizados como "Limpieza", lo cual parece incorrecto.

### 🏪 3. TABLA VENTAS

- **Escala**: 120 transacciones de venta
- **Período**: 6 meses (Enero 2024 - Junio 2024)
- **Medios de pago**: 4 tipos diferentes

### 🏪 4. TABLA DETALLES_VENTAS

- **Escala**: 343 líneas de detalle
- **Relacional**: Múltiples productos por venta (promedio: 2.86 productos/venta)
- **Integridad**: Campo importe calculado automáticamente

## 📈 ESCALA Y VOLUMEN DE DATOS

### Métricas Cuantitativas

| Métrica | Valor | Descripción |
|---|---|---|
| Total registros | 663 | Suma de todas las tablas |
| Clientes | 95 | Base de clientes completa |
| Productos | 100 | Catálogo completo |
| Transacciones | 120 | Ventas realizadas |
| Líneas de detalle | 343 | Items vendidos en total |
| Promedio productos/venta | 2.86 | Densidad de compra |

### Distribución Temporal

- **Clientes**: Registrados en 2023 (período de 4 meses)
- **Ventas**: Realizadas en 2024 (período de 6 meses)
- **Actualidad**: Datos hasta junio 2024

## 🔢 TIPOS DE DATOS Y DOMINIOS

### Dominios de Valores Identificados

- **Ciudades o municipios (6 valores distintos)**:

| Ciudad / Municipio | Ubicación (Departamento) | Notas de Ubicación |
| :--- | :--- | :--- |
| **Córdoba (Capital)** | Capital | Es la capital de la provincia y la ciudad más grande. Se ubica en el centro-norte de la provincia. |
| **Villa Carlos Paz** | Punilla | Famosa ciudad turística en el Valle de Punilla, a orillas del Lago San Roque, al oeste de la capital. |
| **Río Cuarto** | Río Cuarto | Es la segunda ciudad más grande de la provincia. Se ubica en el sur de Córdoba. |
| **Villa María** | General San Martín | Importante ciudad ubicada en el centro-este de la provincia. |
| **Alta Gracia** | Santa María | Ciudad con gran valor histórico y turístico, ubicada al suroeste de la capital, en el Valle de Paravachasca. |
| **Mendiolaza** | Colón | Forma parte del Gran Córdoba, ubicada al norte de la ciudad capital. |

- **Categorías de Productos (2 valores)**:
  - Alimentos
  - Limpieza

- **Medios de Pago (4 valores)**:
  - Tarjeta
  - Efectivo
  - Transferencia
  - QR

## 🎯 CARACTERÍSTICAS TÉCNICAS

### Complejidad Relacional

- Grado de relaciones: 3 relaciones directas
- Cardinalidades: Uno-a-Muchos en todas las relaciones
- Integridad referencial: No normalizada. Para ver normalización, revisar [Normalizacion Base de Datos Aurelion](https://drive.google.com/file/d/1QqqiQixGuYnMFjbb4t_1Dz8XzlW1vqKt/view?usp=sharing)

### Volumen de Datos

- Tamaño estimado: ≈ 50-100 KB (base pequeña-mediana)
- Registros/día: ≈ 0.67 ventas/día (promedio)
- Crecimiento: Datos históricos completos

### Patrones de Datos

- Consistencia: IDs con formato decimal (1.0, 2.0, etc.)
- Formato fechas: DATETIME con hora 00:00:00
- Nomenclatura: Nombres en español, emails válidos

### Diagrama Entidad-Relación (Normalizada)

![Diagrama ER](/static/Proyecto_Aurelion.png)

## 📊 POTENCIAL ANALÍTICO

### Nivel de Detalle Disponible

- Granularidad temporal: Hasta nivel de día
- Segmentación: Por cliente, producto, ciudad, categoría
- Métricas: Ventas, cantidades, ingresos, frecuencia

### Capacidades de Análisis

- Análisis RFM de clientes
- Análisis de canasta de compra
- Análisis de estacionalidad
- Segmentación geográfica
- Análisis de rentabilidad por producto

## 📋 PREGUNTAS CLAVE

### Estratégicas

- ¿Qué productos generan el 80% de los ingresos?
- ¿Qué ciudades son más rentables?
- ¿Qué medio de pago prefieren los clientes de alto valor?

### Operativas

- ¿Qué días de la semana tienen más ventas?
- ¿Cuál es el ticket promedio por ciudad?
- ¿Qué productos se venden mejor juntos?

### Comerciales

- ¿Quiénes son mis clientes más valiosos?
- ¿Qué clientes están en riesgo de fuga?
- ¿Qué segmentos de clientes son más rentables?

</div>
