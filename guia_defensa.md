# Guía para la presentación y la defensa · JR Parking

## Guion de 9 minutos para 6 integrantes (~1.5 min cada uno)
| Min | Integrante | Qué mostrar | Qué decir |
|---|---|---|---|
| 0:00–1:30 | **Valeria** | Dashboard, encabezado | Qué es JR Parking (cajas Limonera y Nailea para el sector agrícola, Juárez N.L.), que los datos son la base simulada de la Unidad 1 y la pregunta de negocio: cuántas cajas producir para no tener faltantes ni excedentes. |
| 1:30–3:00 | **Yesenia** | Notebook, sección 2 | Limpieza: importes venían como texto con "$" y ",", fecha en día/mes/año, se revisaron duplicados, faltantes, meses faltantes y la aritmética (subtotal, IVA, total). No hubo errores; los totales coinciden con la Unidad 1. No hay devoluciones ni meses sin venta. |
| 3:00–4:30 | **Fernando** | Pestaña **Ventas históricas**; **mover filtros en vivo** | Crecimiento +5 % y +6 % en piezas, +9.7 % en pesos por el aumento de precio. Estacionalidad: junio máximo, diciembre mínimo. Demostrar el filtro: Caja Limonera, ene-2024 a dic-2025 → $21.5 M y +9.2 %. Explicar que cada mes tiene un solo producto. |
| 4:30–6:00 | **Alexa** | Notebook sección 4–5 y pestaña **Evaluación** | Por qué Holt-Winters (tendencia + estacionalidad). Entrenamiento ene-2023 a sep-2025, prueba oct–dic 2025. MAE 79 vs 22,225 piezas. Advertir que el error es casi cero porque los datos simulados son muy regulares. |
| 6:00–7:30 | **Gerardo** | Pestaña **Pronóstico total** | 268,937 piezas para ene–mar 2026 (+5.2 %), ≈ $4.03 M sin IVA a $15. Rango de planeación ±5 %. Es **pronóstico total**: los filtros no lo cambian. Supuestos. |
| 7:30–9:00 | **Raul** | Pestaña **Conclusiones** | Conclusiones, las 3 recomendaciones (producción anticipada, compra de materia prima, promociones en temporada baja) y limitaciones. |

**Antes de la clase:** correr `streamlit run dashboard/app.py` en la computadora que se proyectará y tener el notebook abierto en Colab ya ejecutado. **Todos** deben poder responder cualquiera de las preguntas de abajo.

---

## Respuestas a las preguntas de la defensa

**1. ¿Qué problema del negocio resuelve su análisis?**
JR Parking tiene una demanda muy estacional: en junio vende casi el doble que en diciembre. Si no anticipa la producción, le faltan cajas en temporada alta y le sobra inventario en temporada baja. El pronóstico le dice cuántas cajas producir y cuánto plástico comprar para enero–marzo 2026, justo cuando empieza a subir la demanda.

**2. ¿Qué registros corrigieron y por qué?**
La base no tenía registros erróneos, y eso también se comprobó con código. Lo que se corrigió fue el **formato**:
* Cantidades e importes venían como texto ("$1,020,362.00") y se convirtieron a número para poder sumarlos.
* La fecha venía como día/mes/año. Se indicó el formato para que "01/02/2023" se leyera como febrero y no como 2 de enero.
* Se renombraron las columnas para simplificar el código.

Se revisó y no se encontró: duplicados, faltantes, meses faltantes, cantidades negativas, ni errores en subtotal/IVA/total. **Devoluciones:** la base es un resumen mensual y no las registra, así que se analizan las ventas registradas (es una limitación). **Periodos sin venta:** no hay, son 36 meses consecutivos. Además, los totales anuales coinciden con la Unidad 1.

**3. ¿Por qué eligieron ese método de pronóstico?**
El análisis mostró dos cosas: **tendencia creciente** (+5 % y +6 % anual) y **estacionalidad anual** (pico en junio, mínimo en diciembre, igual cada año). Holt-Winters está hecho justo para eso: estima un nivel, una tendencia y un factor para cada mes. Se usó estacionalidad multiplicativa porque los picos crecen proporcionalmente con las ventas.

**4. ¿Cómo evitaron utilizar información futura al evaluar el modelo?**
Dividimos por tiempo, no al azar. El modelo se entrenó solo con enero 2023 a septiembre 2025, y octubre, noviembre y diciembre 2025 se guardaron como prueba. Un `assert` en el código comprueba que el último mes de entrenamiento es anterior al primero de prueba. Si dividiéramos al azar, el modelo "vería" meses posteriores a los que predice, cosa imposible en la vida real.

**5. ¿Cuál fue el MAE y qué significa para el negocio?**
* Holt-Winters: **79 piezas** por mes (≈ $1,185; 0.1 % de la venta mensual).
* Ingenuo: **22,225 piezas** por mes (≈ $333 mil; 31 %). El ingenuo supuso que de octubre a diciembre se vendería lo mismo que en septiembre, cuando en realidad las ventas caen.

Para el negocio, usar el ingenuo habría llevado a producir unas 22 mil cajas de más cada mes de fin de año. **Hay que aclarar** que el error de Holt-Winters es tan bajo porque los datos simulados son perfectamente regulares. Con ventas reales sería mayor, por eso se usa un rango de planeación de ±5 %.

**6. ¿Qué cambiaría si apareciera una promoción o un cambio de precios?**
* **Cambio de precio:** el pronóstico principal está en **piezas**, así que no cambia. Solo cambia el importe: a $15.00 son ≈ $4.03 M; si sube a $15.50, como cada enero, serían ≈ $4.17 M. Ya pasó en la base: las ventas en pesos crecieron 9.7 % en 2025, pero las piezas solo 6 %.
* **Promoción:** el modelo no la conoce. Una promoción aumentaría las piezas de esos meses por encima del pronóstico y podría "adelantar" compras de meses posteriores. Habría que ajustar el pronóstico manualmente con el efecto esperado, reentrenar cuando haya datos nuevos o usar un modelo que incluya una variable de promoción.

**7. ¿Qué parte del código fue apoyada por IA y cómo la verificaron?**
*(Respondan con lo que realmente hicieron; ver `bitacora_IA.md`.)* El código lo propuso Claude a partir de nuestra base. Lo verificamos con:
* Los `assert` de calidad y la comparación de totales con la Unidad 1.
* Recalcular a mano el MAE.
* Comparar los totales del dashboard con los del notebook.

---

## Conceptos que deben poder explicar
* **Subtotal vs venta total:** se analiza el subtotal (sin IVA) porque el IVA es un impuesto, no ingreso.
* **MAE** = promedio de |real − estimado|, en piezas. Menor es mejor.
* **Pronóstico ingenuo:** repetir la última venta. Si un modelo no le gana, no sirve.
* **Holt-Winters (α, β, γ):** cuánto peso se da a los datos recientes en nivel, tendencia y estacionalidad. Salió α = 0.95 (el nivel sigue de cerca al último dato) y β, γ ≈ 0 (tendencia y estacionalidad estables). Se eligen con búsqueda en rejilla dentro del entrenamiento.
* **Evaluación vs proyección:** la evaluación compara contra meses que ya pasaron (oct–dic 2025). La proyección usa los 36 meses y estima meses que no han ocurrido (ene–mar 2026).
* **Limitación de producto:** cada mes de la base tiene un solo producto, por eso no se pronostica por producto.
