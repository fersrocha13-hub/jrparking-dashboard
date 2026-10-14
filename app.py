"""
Dashboard de ventas y pronóstico · JR Parking (DATOS SIMULADOS con fines académicos)
IA Aplicada a los Negocios · Unidad 2

Ejecutar desde la carpeta raíz del proyecto:
    pip install -r codigo/requirements.txt
    streamlit run dashboard/app.py

Usa los archivos que genera el notebook codigo/analisis_pronostico_jrparking.ipynb:
    datos/ventas_jrparking_depurada.csv y datos/resultados/*.csv
"""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Configuración y carga de datos
# ---------------------------------------------------------------------------
st.set_page_config(page_title="JR Parking · Ventas y pronóstico", page_icon="📦", layout="wide")
RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "datos"
RES = DATOS / "resultados"
AZUL, NARANJA, GRIS = "#1f5f8b", "#e67e22", "#8c8c8c"
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def mes_txt(f):                         # 2026-01-01 -> "ene-2026"
    f = pd.Timestamp(f)
    return f"{MESES[f.month - 1]}-{f.year}"


def mxn(x):
    return f"${x:,.0f}"


def mxn_md(x):                          # "$" escapado: en markdown dos "$" se leen como fórmula
    return "\\$" + f"{x:,.0f}"


def ejes_meses(fig, fechas, cada=3):
    """Etiquetas del eje X en español."""
    f = sorted(pd.to_datetime(pd.Series(fechas).unique()))[::cada]
    fig.update_xaxes(tickvals=f, ticktext=[mes_txt(x) for x in f])
    return fig


@st.cache_data
def cargar():
    ventas = pd.read_csv(DATOS / "ventas_jrparking_depurada.csv", parse_dates=["fecha"])
    evaluacion = pd.read_csv(RES / "evaluacion_prueba.csv", parse_dates=["mes"])
    mae = pd.read_csv(RES / "metricas_mae.csv")
    pron = pd.read_csv(RES / "pronostico_futuro.csv", parse_dates=["mes"])
    return ventas, evaluacion, mae, pron


try:
    df, evaluacion, mae, pron = cargar()
except FileNotFoundError as e:
    st.error(f"Falta un archivo: {e.filename}. Ejecuta primero el notebook de la carpeta codigo/.")
    st.stop()

# ---------------------------------------------------------------------------
# Barra lateral: filtros
# ---------------------------------------------------------------------------
st.sidebar.header("Filtros")
meses = list(df["fecha"])
ini, fin = st.sidebar.select_slider("Periodo (mes inicial – mes final)", options=meses,
                                    value=(meses[0], meses[-1]), format_func=mes_txt)
ini, fin = pd.Timestamp(ini), pd.Timestamp(fin)
prods = sorted(df["producto"].unique())
sel_prod = st.sidebar.multiselect("Producto", prods, default=prods)
canales = sorted(df["canal"].unique())
sel_canal = st.sidebar.multiselect("Canal", canales, default=canales)
st.sidebar.caption("En la base, **cada mes registra un solo producto y un solo canal**. Al filtrar por "
                   "producto o canal, los meses que no corresponden aparecen en cero.")
st.sidebar.caption("El **pronóstico es TOTAL** (ambos productos y canales) y **no cambia con los filtros**.")


def filtrar(desde, hasta):
    return df[df["fecha"].between(desde, hasta) & df["producto"].isin(sel_prod) & df["canal"].isin(sel_canal)]


f = filtrar(ini, fin)

# ---------------------------------------------------------------------------
# Encabezado e indicadores
# ---------------------------------------------------------------------------
st.title("📦 JR Parking · Ventas y pronóstico de demanda")
st.caption(f"Cajas de plástico para el sector agrícola · Juárez, N.L. · ⚠️ Datos SIMULADOS con fines académicos · "
           f"Ventas en pesos mexicanos (MXN) **sin IVA** · Periodo seleccionado: **{mes_txt(ini)} a {mes_txt(fin)}**")

if f.empty:
    st.warning("No hay ventas con los filtros seleccionados.")
    st.stop()

ini_ant, fin_ant = ini - pd.DateOffset(years=1), fin - pd.DateOffset(years=1)
hay_base = ini_ant >= df["fecha"].min()
f_ant = filtrar(ini_ant, fin_ant) if hay_base else None

k1, k2, k3, k4 = st.columns(4)
k1.metric("Ventas (MXN sin IVA)", mxn(f["subtotal"].sum()),
          help=f"Con IVA: {mxn(f['venta_total'].sum())}")
k2.metric("Piezas vendidas", f"{f['cantidad'].sum():,.0f}")
if hay_base and f_ant["subtotal"].sum() > 0:
    k3.metric("Variación vs año anterior",
              f"{f['subtotal'].sum() / f_ant['subtotal'].sum() - 1:+.1%}",
              help=f"Ventas {mes_txt(ini_ant)} a {mes_txt(fin_ant)}: {mxn(f_ant['subtotal'].sum())}. "
                   f"En piezas: {f['cantidad'].sum() / f_ant['cantidad'].sum() - 1:+.1%}")
else:
    k3.metric("Variación vs año anterior", "No aplica",
              help="No existen datos del mismo periodo del año anterior (la base inicia en ene-2023). "
                   "Selecciona un periodo a partir de ene-2024.")
k4.metric("Precio promedio por pieza", f"${f['subtotal'].sum() / f['cantidad'].sum():,.2f}")

t1, t2, t3, t4 = st.tabs(["📈 Ventas históricas", "🔮 Pronóstico total", "🧪 Evaluación del modelo", "✅ Conclusiones"])

# ---------------------------------------------------------------------------
# 1. Ventas históricas
# ---------------------------------------------------------------------------
with t1:
    medida = st.radio("Mostrar en", ["Piezas", "Pesos (MXN sin IVA)"], horizontal=True)
    col = "cantidad" if medida == "Piezas" else "subtotal"
    fmt = ",.0f" if col == "cantidad" else "$,.0f"
    # Se completa con ceros para que los meses filtrados se vean como meses sin venta
    todos = pd.DataFrame({"fecha": df.loc[df["fecha"].between(ini, fin), "fecha"]})
    mensual = todos.merge(f[["fecha", col]], on="fecha", how="left").fillna(0)
    fig = px.line(mensual, x="fecha", y=col, markers=True, title=f"{medida} por mes · según filtros",
                  labels={"fecha": "Mes", col: medida})
    fig.update_traces(line_color=AZUL)
    fig.update_layout(yaxis_tickformat=fmt, hovermode="x unified")
    ejes_meses(fig, mensual["fecha"])
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    por_prod = f.groupby("producto", as_index=False)[col].sum()
    fig = px.bar(por_prod, x="producto", y=col, text_auto=fmt.replace(",.0f", ",.3s"), color="producto",
                 color_discrete_sequence=[AZUL, NARANJA], title=f"{medida} por producto",
                 labels={"producto": "", col: medida})
    fig.update_layout(yaxis_tickformat=fmt, showlegend=False)
    c1.plotly_chart(fig, use_container_width=True)
    por_canal = f.groupby("canal", as_index=False)[col].sum()
    fig = px.pie(por_canal, names="canal", values=col, hole=.5, title=f"{medida} por canal",
                 color_discrete_sequence=[AZUL, NARANJA])
    c2.plotly_chart(fig, use_container_width=True)

    anio = f.assign(anio=f["fecha"].dt.year.astype(str), mes=f["fecha"].dt.month)
    fig = px.line(anio, x="mes", y=col, color="anio", markers=True, title=f"{medida}: comparación entre años",
                  labels={"mes": "Mes", col: medida, "anio": "Año"},
                  color_discrete_sequence=["#9ecae1", "#4292c6", "#08306b"])
    fig.update_xaxes(tickvals=list(range(1, 13)), ticktext=MESES)
    fig.update_layout(yaxis_tickformat=fmt)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# 2. Pronóstico total
# ---------------------------------------------------------------------------
with t2:
    st.info("**Pronóstico TOTAL de la empresa** (Caja Limonera + Caja Nailea, todos los canales) en **piezas**. "
            "El modelo no calcula pronósticos por producto, por eso esta sección **no cambia con los filtros**.")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["fecha"], y=df["cantidad"], name="Piezas reales", mode="lines+markers",
                             line=dict(color=AZUL)))
    fig.add_trace(go.Scatter(x=pd.concat([pron["mes"], pron["mes"][::-1]]),
                             y=pd.concat([pron["maximo_piezas_+5%"], pron["minimo_piezas_-5%"][::-1]]),
                             fill="toself", fillcolor="rgba(230,126,34,.2)", line=dict(width=0), mode="lines",
                             name="Rango de planeación ±5 %", hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=pd.concat([df["fecha"].tail(1), pron["mes"]]),
                             y=pd.concat([df["cantidad"].tail(1), pron["pronostico_piezas"]]),
                             name="Pronóstico (Holt-Winters)", mode="lines+markers",
                             line=dict(color=NARANJA, dash="dash"), marker=dict(symbol="square")))
    fig.add_vline(x=df["fecha"].max() + pd.Timedelta(days=15), line_dash="dot", line_color=GRIS)
    fig.update_layout(title="Piezas históricas y pronóstico enero–marzo 2026", yaxis_tickformat=",.0f",
                      hovermode="x unified", legend=dict(orientation="h", y=-0.15))
    ejes_meses(fig, pd.concat([df["fecha"], pron["mes"]]))
    st.plotly_chart(fig, use_container_width=True)

    tabla = pron.assign(Mes=pron["mes"].map(mes_txt))[
        ["Mes", "pronostico_piezas", "minimo_piezas_-5%", "maximo_piezas_+5%", "real_mismo_mes_2025",
         "variacion_vs_2025_%", "importe_estimado_MXN_precio_15"]].rename(columns={
            "pronostico_piezas": "Pronóstico (piezas)", "minimo_piezas_-5%": "Mínimo (−5 %)",
            "maximo_piezas_+5%": "Máximo (+5 %)", "real_mismo_mes_2025": "Real mismo mes 2025",
            "variacion_vs_2025_%": "Variación vs 2025", "importe_estimado_MXN_precio_15": "Importe estimado (MXN, $15)"})
    st.dataframe(tabla.style.format({c: "{:,.0f}" for c in tabla.columns[1:5]}
                                    | {"Variación vs 2025": "{:+.1f}%", "Importe estimado (MXN, $15)": "${:,.0f}"}),
                 hide_index=True, use_container_width=True)
    tot_p, tot_25 = pron["pronostico_piezas"].sum(), pron["real_mismo_mes_2025"].sum()
    m1, m2, m3 = st.columns(3)
    m1.metric("Total pronosticado ene–mar 2026", f"{tot_p:,.0f} piezas", f"{tot_p / tot_25 - 1:+.1%} vs ene–mar 2025")
    m2.metric("Importe estimado (precio $15.00)", mxn(pron["importe_estimado_MXN_precio_15"].sum()),
              help="Sin IVA. Si el precio sube a $15.50 como en años anteriores: " + mxn(tot_p * 15.5))
    m3.metric("Rango de planeación", f"{tot_p * .95:,.0f} – {tot_p * 1.05:,.0f}")
    st.caption("Supuestos: continúan la tendencia y la estacionalidad de 2023–2025; precio de $15.00. "
               "El rango ±5 % es un margen de planeación (similar a la variación del crecimiento anual), no un intervalo "
               "estadístico. Un pronóstico no garantiza las ventas futuras.")

# ---------------------------------------------------------------------------
# 3. Evaluación
# ---------------------------------------------------------------------------
with t3:
    st.markdown("**Evaluación histórica (no es el pronóstico futuro).** Se entrenó con ene-2023 a sep-2025 "
                "y se probó con los últimos 3 meses reales (oct–dic 2025), que el modelo no vio.")
    ev = evaluacion.assign(Mes=evaluacion["mes"].map(mes_txt))
    fig = go.Figure()
    fig.add_bar(x=ev["Mes"], y=ev["real"], name="Real", marker_color=AZUL)
    fig.add_bar(x=ev["Mes"], y=ev["holt_winters"], name="Holt-Winters", marker_color=NARANJA)
    fig.add_bar(x=ev["Mes"], y=ev["ingenuo"], name="Ingenuo (última venta)", marker_color=GRIS)
    fig.update_layout(barmode="group", title="Piezas reales vs estimadas en el periodo de prueba",
                      yaxis_tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True)
    tabla_ev = ev[["Mes", "real", "holt_winters", "error_abs_hw", "ingenuo", "error_abs_ingenuo"]].rename(
        columns={"real": "Real", "holt_winters": "Estimado Holt-Winters", "error_abs_hw": "Error abs. HW",
                 "ingenuo": "Estimado ingenuo", "error_abs_ingenuo": "Error abs. ingenuo"})
    st.dataframe(tabla_ev.style.format({c: "{:,.0f}" for c in tabla_ev.columns[1:]}),
                 hide_index=True, use_container_width=True)
    a, b = st.columns(2)
    a.metric("MAE Holt-Winters", f"{mae.loc[0, 'MAE_piezas']:,.0f} piezas")
    a.caption(f"≈ {mxn(mae.loc[0, 'MAE_MXN'])} MXN · {mae.loc[0, 'MAE_%_venta_promedio']:.2f} % de la venta mensual")
    b.metric("MAE Ingenuo (última venta)", f"{mae.loc[1, 'MAE_piezas']:,.0f} piezas")
    b.caption(f"≈ {mxn(mae.loc[1, 'MAE_MXN'])} MXN · {mae.loc[1, 'MAE_%_venta_promedio']:.1f} % de la venta mensual")
    st.success("Holt-Winters tiene el menor MAE, por eso es el método seleccionado. MAE = error absoluto medio: "
               "cuántas piezas se equivoca el modelo, en promedio, cada mes.")
    st.warning("El error de Holt-Winters es casi cero porque los datos son simulados con un patrón perfectamente "
               "regular (cada año = año anterior × 1.05 o × 1.06). Con ventas reales el error sería mayor.")

# ---------------------------------------------------------------------------
# 4. Conclusiones
# ---------------------------------------------------------------------------
with t4:
    an = df.groupby(df["fecha"].dt.year).agg(p=("cantidad", "sum"), v=("subtotal", "sum"))
    st.markdown(f"""
#### Conclusiones
1. **Crecimiento:** las piezas crecieron **{an.p[2024] / an.p[2023] - 1:+.1%}** en 2024 y **{an.p[2025] / an.p[2024] - 1:+.1%}** en 2025; las ventas en pesos crecieron **{an.v[2025] / an.v[2024] - 1:+.1%}** en 2025, en parte por el aumento de precio a \\$15.00.
2. **Estacionalidad:** la demanda llega a su máximo en **junio** y a su mínimo en **diciembre**; junio vende casi el doble que diciembre, y el patrón se repite cada año.
3. **Producto y canal:** la Caja Limonera y la venta directa concentran cerca de dos tercios de las ventas.
4. **Pronóstico:** Holt-Winters (MAE {mae.loc[0, 'MAE_piezas']:,.0f} piezas) supera al ingenuo ({mae.loc[1, 'MAE_piezas']:,.0f}). Para ene–mar 2026 se esperan **{pron['pronostico_piezas'].sum():,.0f} piezas** (≈ {mxn_md(pron['importe_estimado_MXN_precio_15'].sum())} sin IVA).

#### Recomendaciones
1. **Producción:** usar diciembre–enero, de baja demanda, para producir por adelantado y llegar a marzo con inventario para la temporada alta (abril–agosto).
2. **Materia prima:** negociar la compra de plástico reciclado del primer semestre antes de enero, con base en el pronóstico, y reducir compras en octubre–diciembre.
3. **Temporada baja:** promociones por volumen o preventa en noviembre–diciembre y más impulso a la venta en línea para suavizar la caída.
""")
    st.caption("Limitaciones: datos simulados y muy regulares; solo 3 ciclos anuales; un producto y un canal por mes; "
               "sin devoluciones ni costos (no se calcula utilidad).")
