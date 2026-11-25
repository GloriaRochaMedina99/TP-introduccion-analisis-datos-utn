import numpy as np
import pandas as pd

# ==========================================================
# PRÁCTICA 1: INGESTA Y DIAGNÓSTICO DE INVENTARIOS
# ==========================================================
print("==========================================================")
print("PRÁCTICA 1: INVENTARIO - ESTRUCTURA, NULOS Y SKUs")
print("==========================================================")
df_inv = pd.read_csv('unidad2-click-and-buy-inventory-raw.csv')

print("Dimensiones (filas, columnas):", df_inv.shape)
print("\nPrimeras 5 filas:")
print(df_inv.head())

print("\nTipos de datos:")
print(df_inv.dtypes)

nulos_abs = df_inv.isnull().sum()
nulos_pct = (df_inv.isnull().mean() * 100).round(2)
df_nulos = pd.DataFrame({'Nulos_Absolutos': nulos_abs, 'Porcentaje %': nulos_pct})
print("\nDiagnóstico de nulos:")
print(df_nulos)

skus_unicos = df_inv['SKU'].nunique()
skus_duplicados = len(df_inv) - skus_unicos
print(f"\nSKUs Únicos: {skus_unicos} | SKUs Duplicados: {skus_duplicados}")


# ==========================================================
# PRÁCTICA 2: SESIONES, OUTLIERS Y COMPARACIÓN DE MÉTRICAS
# ==========================================================
print("\n==========================================================")
print("PRÁCTICA 2: SESIONES - FRECUENCIAS, OUTLIERS Y FILTRADO")
print("==========================================================")
df_sess = pd.read_csv('unidad2-click-and-buy-sessions.csv')

print("=== INFORMACIÓN TÉCNICA ===")
df_sess.info()

print("\nFrecuencias de Origen_Trafico:")
print(df_sess['Origen_Trafico'].value_counts())

print("\nFrecuencias de Dispositivo:")
print(df_sess['Dispositivo'].value_counts())

count_99999 = (df_sess['Duracion_Segundos'] == 99999).sum()
count_neg = (df_sess['Duracion_Segundos'] < 0).sum()
print(f"\nDuraciones 99999s: {count_99999} | Duraciones Negativas (<0): {count_neg}")

df_valid = df_sess[
    (df_sess['Duracion_Segundos'] >= 0) & (df_sess['Duracion_Segundos'] < 10000)
].copy()
print(f"Registros válidos retenidos (df_valid): {len(df_valid)}")

mean_raw = df_sess['Duracion_Segundos'].mean()
median_raw = df_sess['Duracion_Segundos'].median()
mean_valid = df_valid['Duracion_Segundos'].mean()
median_valid = df_valid['Duracion_Segundos'].median()

print(f"\nDATOS CRUDOS   -> Media: {mean_raw:.2f}s | Mediana: {median_raw:.2f}s")
print(f"DATOS FILTRADOS-> Media: {mean_valid:.2f}s | Mediana: {median_valid:.2f}s")
print(
    "Sesgo por outliers: los valores extremos de 99999s elevan fuertemente la "
    "media en los datos crudos, mientras que la mediana es robusta y refleja mejor "
    "la duración típica de sesión."
)


# ==========================================================
# PRÁCTICA 3: LIMPIEZA DE PRECIO, STOCK NEGATIVO Y FILTRO
# ==========================================================
print("\n==========================================================")
print("PRÁCTICA 3: LIMPIEZA DE PRECIO, STOCK Y ELECTRÓNICA > $500")
print("==========================================================")
def limpiar_precio(valor):
    if pd.isna(valor):
        return np.nan
    texto = str(valor).replace('$', '').replace(',', '').strip()
    return float(texto) if texto else np.nan

df_inv['Precio_Limpio'] = df_inv['Precio_Lista'].apply(limpiar_precio)

precio_promedio = df_inv['Precio_Limpio'].mean()
precio_mediana = df_inv['Precio_Limpio'].median()
print(f"Precio promedio limpio: ${precio_promedio:,.2f} USD")
print(f"Mediana de precios limpia: ${precio_mediana:,.2f} USD")

stock_negativos = (df_inv['Stock_Disponible'] < 0).sum()
pct_stock_negativos = (stock_negativos / len(df_inv)) * 100
print(f"Productos con Stock_Disponible < 0: {stock_negativos} ({pct_stock_negativos:.2f}%)")

electronica_cara = df_inv[
    (df_inv['Categoria'] == 'Electrónica') & (df_inv['Precio_Limpio'] > 500.0)
]
print(f"\nProductos en 'Electrónica' con Precio_Limpio > $500.00 USD: {len(electronica_cara)}")
print(electronica_cara[['SKU', 'Producto', 'Categoria', 'Precio_Limpio', 'Stock_Disponible']].head(15))