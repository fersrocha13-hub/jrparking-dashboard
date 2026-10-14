# Unidad 2 · Análisis y pronóstico de ventas — JR Parking
IA Aplicada a los Negocios · Dr. José Antonio Sánchez Valdés
Ruta: **Google Colab + Streamlit** · Datos: base de la Unidad 1, **simulada con fines académicos** (ver `datos/diccionario_datos.md`)

**Equipo:** Valeria Nohemi Yañez Villarreal (22481232) · Yesenia Aguirre Moncada (22481216) · Fernando Salvador Rocha de la Garza (22480295) · Alexa Paola Rodriguez Sandoval (22480306) · Gerardo Osmar Esquivel Palacios (21480798) · Raul Alexis Carrizales Dana (23481198)

## Contenido de la carpeta
```
Unidad2_GRUPO_JRParking/
├── datos/
│   ├── ventas_jrparking_original.csv       base original (Unidad 1)
│   ├── ventas_jrparking_depurada.csv       base depurada (la genera el notebook)
│   ├── diccionario_datos.md                fuente, periodo, moneda y significado de cada campo
│   └── resultados/                         CSV que usa el dashboard (los genera el notebook)
├── codigo/
│   ├── analisis_pronostico_jrparking.ipynb limpieza, análisis, pronóstico y evaluación
│   └── requirements.txt                    librerías necesarias
├── dashboard/
│   └── app.py                              dashboard de Streamlit
└── reporte/
    ├── Reporte_Tecnico_Unidad2_JRParking.pdf  reporte técnico (portada + contenido)
    ├── bitacora_IA.md                      bitácora de uso de IA
    ├── guia_defensa.md                     guion de la exposición y respuestas a la defensa
    └── capturas/                           capturas del dashboard
```

## Cómo ejecutar
### 1. Notebook en Google Colab
1. Abrir https://colab.research.google.com → *Archivo → Subir notebook* → `codigo/analisis_pronostico_jrparking.ipynb`.
2. *Entorno de ejecución → Ejecutar todas*. Cuando lo pida, subir `datos/ventas_jrparking_original.csv`.

> Los resultados ya vienen generados en `datos/`, así que el dashboard funciona sin volver a correr el notebook.

### 1-b. Notebook local (opcional)
```bash
pip install -r codigo/requirements.txt
cd codigo
jupyter notebook analisis_pronostico_jrparking.ipynb      # Run All
```

### 2. Dashboard (en la computadora donde se va a proyectar)
```bash
pip install -r codigo/requirements.txt
streamlit run dashboard/app.py
```
Se abre en el navegador en `http://localhost:8501`. No requiere internet ni publicarse.

## Resultados principales
| Indicador | Valor |
|---|---|
| Ventas ene-2023 a dic-2025 | 3,157,939 piezas · $45,846,525 MXN sin IVA |
| Crecimiento en piezas | +5.0 % (2024) · +6.0 % (2025) |
| MAE Holt-Winters (prueba oct–dic 2025) | 79 piezas (0.11 % de la venta mensual) |
| MAE ingenuo (última venta) | 22,225 piezas (30.8 %) |
| Pronóstico total ene–mar 2026 | 268,937 piezas (+5.2 % vs 2025) · ≈ $4,034,055 MXN sin IVA a $15.00 |
