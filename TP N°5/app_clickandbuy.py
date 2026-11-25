import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Configuración de página y cacheo
st.set_page_config(
    page_title="Click&Buy Analytics App",
    layout="wide",
    page_icon="🛒",
)

st.title("🛒 Click&Buy — Portal Web de Analítica Comercial")
st.markdown("Herramienta interactiva para exploración de órdenes y métricas logísticas.")


@st.cache_data
def load_data():
    df = pd.read_csv("unidad5-click-and-buy-streamlit-app.csv")
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    return df


df_raw = load_data()

# 2. Filtros dinámicos en la barra lateral (st.sidebar)
st.sidebar.header("🔍 Filtros de Exploración")

regions = sorted(df_raw["Region"].dropna().unique())
selected_regions = st.sidebar.multiselect(
    "Seleccionar Región:",
    regions,
    default=regions,
)

categories = ["Todas"] + sorted(df_raw["Categoria"].dropna().unique().tolist())
selected_cat = st.sidebar.selectbox("Seleccionar Categoría:", categories)

min_monto = float(df_raw["Monto_USD"].min())
max_monto = float(df_raw["Monto_USD"].max())
selected_monto = st.sidebar.slider(
    "Rango de Monto (USD):",
    min_monto,
    max_monto,
    (min_monto, max_monto),
)

# Aplicar filtros
df = df_raw[df_raw["Region"].isin(selected_regions)]
if selected_cat != "Todas":
    df = df[df["Categoria"] == selected_cat]
df = df[(df["Monto_USD"] >= selected_monto[0]) & (df["Monto_USD"] <= selected_monto[1])]

# 3. Tarjetas KPI (st.metric)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Órdenes Filtradas", f"{len(df):,}")
c2.metric("Facturación Total", f"${df['Monto_USD'].sum():,.2f} USD")
c3.metric("Ticket Promedio", f"${df['Monto_USD'].mean():,.2f} USD" if len(df) > 0 else "$0.00 USD")
c4.metric(
    "Satisfacción Promedio",
    f"⭐ {df['Satisfaccion_Stars'].mean():.2f} / 5" if len(df) > 0 else "⭐ 0.00 / 5",
)

st.divider()

# 4. Gráficos interactivos con Plotly
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Órdenes por Segmento de Cliente")
    fig_seg = px.histogram(
        df,
        x="Segmento_Cliente",
        color="Segmento_Cliente",
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    st.plotly_chart(fig_seg, use_container_width=True)

with col_right:
    st.subheader("Distribución por Estado de Envío")
    fig_pie = px.pie(
        df,
        names="Estado_Envio",
        values="Monto_USD",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Darkmint,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# 5. Tabla interactiva y descarga CSV
st.subheader("📋 Registro Detallado de Órdenes")
st.dataframe(df, use_container_width=True)

csv_data = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Descargar Datos Filtrados (CSV)",
    data=csv_data,
    file_name="click_and_buy_filtrado.csv",
    mime="text/csv",
)