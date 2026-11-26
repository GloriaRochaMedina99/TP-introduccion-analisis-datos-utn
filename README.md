# Introducción al Análisis de Datos — Trabajos Prácticos (UTN - FRT)

Repositorio con la resolución práctica y el material de estudio de la asignatura **Introducción al Análisis de Datos** (Tecnicatura Universitaria en Programación - Plan 2024, UTN Facultad Regional Tucumán), trabajado sobre los datasets del caso de negocio **Click&Buy**.

**Autora:** Gloria Rocha Medina

---

## Estructura del Repositorio

* **`TP N°1/` — Fundamentos, Calidad de Datos y Análisis Diagnóstico (`tp1.py`)**
  * Inspección estructural y detección de nulos en transacciones (`click-and-buy-transactions.csv`).
  * Depuración de logs web, modelado de embudo de conversión (*funnel*) y análisis de latencia, tasa de fallo y pérdidas económicas por pasarela de pago (`click-and-buy-web-logs.csv`).
  * Análisis cualitativo de reseñas de clientes, búsqueda de palabras clave en quejas y cruce relacional con transacciones fallidas (`click-and-buy-crm-reviews.csv`).
* **`TP N°2/` — Recolección, Carga e Inspección Inicial (`tp2.py`)**
  * Diagnóstico estructural de inventario, tipos de datos, nulos y SKUs duplicados (`unidad2-click-and-buy-inventory-raw.csv`).
  * Auditoría de sesiones web, detección de anomalías (`99999s` y duraciones negativas) y comparación de media vs. mediana antes y después del filtrado (`unidad2-click-and-buy-sessions.csv`).
  * Limpieza de precios con formato moneda, detección de stock negativo y filtrado por categoría.
* **`TP N°3/` — Limpieza y Preparación de Datos / Data Wrangling (`tp3.py`)**
  * Deduplicación por clave primaria, conversión de cadenas monetarias a `float` e imputación de edad por mediana (`unidad3-click-and-buy-dirty-customers.csv`).
  * Filtrado de montos negativos, detección de *outliers* mediante criterio IQR, *One-Hot Encoding* de métodos de pago y auditoría de órdenes huérfanas con `Left Join` (`unidad3-click-and-buy-dirty-orders.csv`).
  * Normalización de texto, parseo de fechas heterogéneas (`pd.to_datetime`), *Ordinal Encoding* de nivel educativo y segmentación por ingresos.
* **`TP N°4/` — Análisis Exploratorio de Datos (EDA) y Visualización (`tp4.py`)**
  * Medidas de tendencia central, dispersión (desviación estándar, CV, IQR), asimetría (*skewness*) e histograma con KDE (`unidad4-click-and-buy-eda-sales.csv`).
  * Boxplots por categoría, matriz de correlación (*Heatmap*) y regresión lineal bivariada entre días de entrega y satisfacción (`unidad4-click-and-buy-customer-metrics.csv`).
  * Segmentación por rango etario y análisis de fidelidad mediante *Scatter Plot*.
* **`TP N°5/` — Visualización Avanzada, Storytelling y Web App (`app_clickandbuy.py`)**
  * Medidas DAX, diseño de tablero ejecutivo e informe narrativo (*Contexto - Conflicto - Resolución*) (`tp5_1_Data_Storytelling_y_Dax.txt`, `unidad5-click-and-buy-kpi-dashboard.csv`).
  * Aplicación web interactiva desarrollada con **Streamlit** y **Plotly** con filtros dinámicos, tarjetas KPI, gráficos interactivos y descarga CSV (`unidad5-click-and-buy-streamlit-app.csv`).
* **`TP POWER BI/` — Prácticas Complementarias de Business Intelligence**
  * Datasets, guías y formulaciones DAX / diagnóstico CRM (`resumen_dax_y_diagnostico.txt`) para tableros comercial, logístico y de clientes en Power BI Desktop.

---

## Requisitos y Ejecución

1. Instalar las dependencias necesarias en Python:
   ```bash
   py -m pip install pandas numpy matplotlib seaborn streamlit plotly