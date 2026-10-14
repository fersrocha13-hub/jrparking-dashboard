# Diccionario de datos · JR Parking

## Identificación de la fuente
| Concepto | Descripción |
|---|---|
| **Fuente** | Base de ventas presentada en el **Proyecto de la Unidad 1** (hoja "JR PARKING – Base de datos de ventas (36 meses)"). **Datos simulados con fines académicos**: se tomó como base 998,400 piezas anuales en 2023 y se aplicó crecimiento moderado (+5 % en 2024, +6 % en 2025) y estacionalidad del mercado agrícola. |
| **Negocio** | JR Parking: reciclaje e inyección de plástico, fabricación de cajas para el sector agrícola. Juárez, Nuevo León. |
| **Periodo** | Enero 2023 a diciembre 2025 (36 meses consecutivos) |
| **Moneda** | Pesos mexicanos (MXN) |
| **Qué representa cada fila** | Las **ventas de un mes**: piezas vendidas, precio e importes, con el producto y canal registrados para ese mes |
| **Datos personales** | Ninguno. El segmento de cliente es genérico ("Agrícola"); no hay nombres, teléfonos ni datos de clientes. |
| **Costos / utilidad** | La base no incluye costos, por lo que **no se calcula utilidad**. |

## Archivos
| Archivo | Filas | Descripción |
|---|---|---|
| `ventas_jrparking_original.csv` | 36 | Base original de la Unidad 1, tal como aparece en Excel (importes como texto con "$" y ",", fecha dd/mm/aaaa) |
| `ventas_jrparking_depurada.csv` | 36 | Base depurada por el notebook: tipos numéricos, fecha convertida, columnas renombradas, año y mes |
| `resultados/ventas_mensuales.csv` | 36 | Piezas, subtotal y venta total por mes |
| `resultados/evaluacion_prueba.csv` | 3 | Real vs estimado (oct–dic 2025) de ambos métodos |
| `resultados/metricas_mae.csv` | 2 | MAE de cada método (piezas y MXN) |
| `resultados/pronostico_futuro.csv` | 3 | Pronóstico ene–mar 2026 con rango de planeación ±5 % e importe estimado |
| `resultados/indice_estacional.csv` | 12 | Índice estacional promedio por mes |

## Campos de la base original
| Campo original | Campo depurado | Tipo | Descripción | Ejemplo |
|---|---|---|---|---|
| Fecha | `fecha` | fecha | Primer día del mes de venta, formato **dd/mm/aaaa** | 01/02/2023 = febrero 2023 |
| Mes | `mes_texto` | texto | Nombre del mes (redundante con la fecha; se valida que coincidan) | Febrero |
| Producto/servicio | `producto` | texto | Caja Limonera o Caja Nailea | Caja Nailea |
| Categoría | `categoria` | texto | Proceso de fabricación (única: Inyección de plástico) | Inyección de plástico |
| Cantidad | `cantidad` | entero | **Piezas (cajas) vendidas** en el mes | 74,880 |
| Precio unitario | `precio_unitario` | decimal | Precio por caja sin IVA: $14.00 (2023), $14.50 (2024), $15.00 (2025) | 14.00 |
| Subtotal | `subtotal` | decimal | **Venta antes de IVA = Cantidad × Precio unitario**. Es la variable de ventas que se analiza | 1,048,320.00 |
| IVA | `iva` | decimal | 16 % del subtotal | 167,731.20 |
| Venta total | `venta_total` | decimal | Subtotal + IVA | 1,216,051.20 |
| Cliente/segmento | `segmento` | texto | Tipo de cliente (único: Agrícola) | Agrícola |
| Zona/sucursal | `zona` | texto | Ubicación (única: Juárez, Nuevo León) | Juárez, Nuevo León |
| Vendedor/canal | `canal` | texto | Venta directa o Venta en línea | Venta directa |
| — | `anio`, `mes` | entero | Año y número de mes (agregados en la limpieza) | 2023, 2 |

**Nota de estructura:** cada mes tiene un solo renglón con un solo producto y un solo canal. La Caja Limonera aparece en 24 meses y la Caja Nailea en 12; la venta en línea aparece en marzo, junio, septiembre y diciembre. Por eso los totales por producto o canal reflejan la asignación mensual y el pronóstico se hace del **total**.
