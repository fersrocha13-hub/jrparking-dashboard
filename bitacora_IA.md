# Bitácora de uso de inteligencia artificial

**Herramienta:** Claude (Anthropic), vía claude.ai
**Fecha:** 12 de octubre de 2026
**Datos compartidos con la IA:** la guía del examen y la presentación del Proyecto de la Unidad 1 (contiene la base de ventas **simulada** con fines académicos). No se compartieron datos confidenciales ni personales de clientes.

> ⚠️ **Para el equipo:** esta bitácora refleja lo que realmente se pidió a la IA. Agreguen las consultas que hagan para entender el proyecto y marquen **solo** las validaciones que ustedes mismos hagan.

## Consultas realizadas

| # | Instrucción o consulta | Ayuda recibida | Corrección o validación |
|---|---|---|---|
| 1 | Se compartió el PDF de la guía del examen y se pidió desarrollar todo lo que solicita. | La IA preguntó qué datos, plataforma y tipo de negocio usar, y armó una primera versión completa con un negocio de ejemplo (una ferretería con datos simulados). | La IA ejecutó todo y corrigió sus propios errores (duplicados ocultos, textos que no coincidían con los números). |
| 2 | *"¿Hizo falta algo?"* | La IA revisó la guía punto por punto contra los entregables. | Encontró que había reportado mal el MAE de un modelo alternativo y que la bitácora necesitaba al menos 3 consultas. Lo corrigió. |
| 3 | Se compartió la presentación de la Unidad 1 con la instrucción: *"hazlo de esta presentación, que sea de los datos que hay ahí y también ahí están los nombres de los integrantes"*. | La IA transcribió la base de 36 meses de JR Parking y rehízo el notebook, el dashboard, el reporte y la guía de defensa con esos datos y los nombres del equipo. | Ver validaciones abajo. La IA señaló que la portada de la Unidad 1 dice "JK Parking" y el resto "JR Parking"; se usó **JR Parking**. |
| 4 | *(Completar: p. ej., "Explícame qué hace cada parámetro de Holt-Winters")* | | |
| 5 | *(Completar: p. ej., "¿Por qué no se pueden dividir los datos al azar?")* | | |

## Correcciones y validaciones hechas por la IA (comprobables en el notebook)
* **Transcripción de la base:** la tabla de la Unidad 1 venía como imagen. Se transcribió y se comprobó fila por fila que Subtotal = Cantidad × Precio, IVA = 16 % y Total = Subtotal + IVA (36 de 36 filas correctas).
* **Validación cruzada:** el notebook verifica con `assert` que los totales anuales (998,400 / 1,048,320 / 1,111,219 piezas y $13,977,600 / $15,200,640 / $16,668,285) coinciden con el diagnóstico de la Unidad 1.
* **Fechas:** se detectó que la fecha está en formato día/mes/año. Si se leyera como mes/día, "01/02/2023" se confundiría con el 2 de enero. Se convirtió con el formato explícito.
* **Error casi cero:** el MAE de Holt-Winters salió en 79 piezas. La IA verificó que se debe a que los datos simulados son perfectamente regulares (cada año = anterior × 1.05 o × 1.06), y lo documentó como limitación en lugar de presentarlo como precisión real.
* **Rango del pronóstico:** un intervalo estadístico salía casi de ancho cero por la misma razón. Se reemplazó por un **rango de planeación de ±5 %** y se explicó por qué.
* **Reproducibilidad:** los parámetros de Holt-Winters se eligen con búsqueda en rejilla, para que den el mismo resultado en Colab y en otra computadora.
* **Dashboard:** el total ($45,846,525 y 3,157,939 piezas) coincide con el notebook. El filtro Caja Limonera, ene-2024 a dic-2025 dio $21,511,527 y +9.2 %, y se recalculó por separado con pandas con el mismo resultado.

## Validaciones realizadas por el equipo (completar)
| Validación | ¿Hecha? | Resultado |
|---|---|---|
| Comparar la base transcrita (`ventas_jrparking_original.csv`) contra nuestro Excel original de la Unidad 1 | ☐ | |
| Ejecutar el notebook completo en Google Colab sin errores | ☐ | |
| Recalcular a mano el MAE de ambos métodos con la tabla de evaluación | ☐ | |
| Abrir el dashboard en la computadora de la presentación y probar los filtros | ☐ | |
| Leer y entender cada sección del notebook (cada integrante) | ☐ | |

## Qué parte fue apoyada por IA
El código (notebook y dashboard), los textos del reporte y la guía de defensa fueron propuestos por la IA a partir de nuestra base de la Unidad 1. El equipo es responsable de revisarlos, ejecutarlos, validarlos y explicarlos en la defensa.
