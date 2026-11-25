import numpy as np
import pandas as pd

# ==========================================================
# PRÁCTICA 1: NULOS, DEDUPLICACIÓN Y LIMPIEZA MONETARIA
# ==========================================================
print("==========================================================")
print("PRÁCTICA 1: CLIENTES - NULOS, DUPLICADOS Y MONEDA")
print("==========================================================")
df_cust = pd.read_csv('unidad3-click-and-buy-dirty-customers.csv')
print(f"Filas iniciales en clientes: {len(df_cust)}")

print("\nValores nulos iniciales (Email, Edad, Ingreso_Anual_USD):")
print(df_cust[['Email', 'Edad', 'Ingreso_Anual_USD']].isna().sum())

df_cust = df_cust.drop_duplicates(subset=['ID_Cliente'], keep='first').copy()
print(f"\nFilas tras deduplicar por ID_Cliente: {len(df_cust)}")

ingreso_limpio_str = (
    df_cust['Ingreso_Anual_USD']
    .astype(str)
    .str.replace('$', '', regex=False)
    .str.replace(',', '', regex=False)
    .str.strip()
)
ingreso_limpio_str = ingreso_limpio_str.replace({'nan': np.nan, 'None': np.nan, '': np.nan})
df_cust['Ingreso_Clean'] = pd.to_numeric(ingreso_limpio_str, errors='coerce')

mediana_edad = df_cust['Edad'].median()
df_cust['Edad'] = df_cust['Edad'].fillna(mediana_edad)
print(f"Mediana de Edad aplicada: {mediana_edad} años | Nulos restantes en Edad: {df_cust['Edad'].isna().sum()}")


# ==========================================================
# PRÁCTICA 2: OUTLIERS (IQR), ONE-HOT ENCODING Y LEFT JOIN
# ==========================================================
print("\n==========================================================")
print("PRÁCTICA 2: ÓRDENES - IQR, DUMMIES Y CLAVES HUÉRFANAS")
print("==========================================================")
df_cust_p2 = pd.read_csv('unidad3-click-and-buy-dirty-customers.csv').drop_duplicates(
    subset=['ID_Cliente'], keep='first'
).copy()
df_ord = pd.read_csv('unidad3-click-and-buy-dirty-orders.csv').drop_duplicates(
    subset=['ID_Orden'], keep='first'
).copy()

df_ord_valid = df_ord[df_ord['Monto_USD'] >= 0].copy()
Q1 = df_ord_valid['Monto_USD'].quantile(0.25)
Q3 = df_ord_valid['Monto_USD'].quantile(0.75)
IQR = Q3 - Q1
lim_sup = Q3 + 1.5 * IQR
outliers_iqr = df_ord_valid[df_ord_valid['Monto_USD'] > lim_sup]
print(f"Límite IQR Superior: ${lim_sup:.2f} USD | Outliers detectados: {len(outliers_iqr)}")

df_ord_encoded = pd.get_dummies(df_ord_valid, columns=['Metodo_Pago'], drop_first=False)
cols_dummies = [c for c in df_ord_encoded.columns if c.startswith('Metodo_Pago_')]
print(f"Columnas generadas por One-Hot Encoding ({len(cols_dummies)}): {cols_dummies}")

df_merged = pd.merge(df_ord_valid, df_cust_p2, on='ID_Cliente', how='left')
huerfanas = df_merged[df_merged['Nombre_Cliente'].isna()]
monto_huerfano = huerfanas['Monto_USD'].sum()
print(f"Órdenes huérfanas: {len(huerfanas)} | Monto total afectado: ${monto_huerfano:,.2f} USD")


# ==========================================================
# PRÁCTICA 3: TEXTO, FECHAS, ORDINAL ENCODING Y FILTRO
# ==========================================================
print("\n==========================================================")
print("PRÁCTICA 3: NORMALIZACIÓN, FECHAS, ORDINAL Y SEGMENTO")
print("==========================================================")
df_p3 = pd.read_csv('unidad3-click-and-buy-dirty-customers.csv').copy()

df_p3['Nombre_Cliente'] = df_p3['Nombre_Cliente'].astype(str).str.strip().str.title()
df_p3.loc[df_p3['Nombre_Cliente'].isin(['Nan', 'None']), 'Nombre_Cliente'] = np.nan

df_p3['Fecha_Registro_dt'] = pd.to_datetime(
    df_p3['Fecha_Registro'], format='mixed', errors='coerce'
)
cant_nat = df_p3['Fecha_Registro_dt'].isna().sum()
print(f"Registros con fechas no parseables (NaT): {cant_nat}")

nivel_norm = df_p3['Nivel_Educativo'].astype(str).str.strip().str.title()
nivel_norm = nivel_norm.replace({'Nan': np.nan, 'None': np.nan})

mapa_educ = {
    'Ninguno': 0,
    'Secundario': 1,
    'Grado': 2,
    'Universitario': 2,
    'Posgrado': 3,
}
df_p3['Nivel_Educativo_Num'] = nivel_norm.map(mapa_educ)

ing_p3_str = (
    df_p3['Ingreso_Anual_USD']
    .astype(str)
    .str.replace('$', '', regex=False)
    .str.replace(',', '', regex=False)
    .str.strip()
)
ing_p3_str = ing_p3_str.replace({'nan': np.nan, 'None': np.nan, '': np.nan})
df_p3['Ingreso_Clean'] = pd.to_numeric(ing_p3_str, errors='coerce')

segmento = df_p3[
    (df_p3['Nivel_Educativo_Num'] >= 2) & (df_p3['Ingreso_Clean'] > 50000)
]
print(f"Clientes con Nivel_Educativo_Num >= 2 e Ingreso > $50,000 USD: {len(segmento)}")
print(f"Ingreso promedio del segmento: ${segmento['Ingreso_Clean'].mean():,.2f} USD")