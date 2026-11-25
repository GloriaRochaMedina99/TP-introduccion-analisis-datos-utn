import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")

# ==========================================================
# PRÁCTICA 1: MÉTRICAS DESCRIPTIVAS Y ASIMETRÍA (VENTAS)
# ==========================================================
print("==========================================================")
print("PRÁCTICA 1: DISTRIBUCIÓN Y ASIMETRÍA DE MONTO_VENTA")
print("==========================================================")
df_sales = pd.read_csv('unidad4-click-and-buy-eda-sales.csv')
print("Dimensiones (filas, columnas):", df_sales.shape)

media_venta = df_sales['Monto_Venta'].mean()
mediana_venta = df_sales['Monto_Venta'].median()
std_venta = df_sales['Monto_Venta'].std()
cv_venta = (std_venta / media_venta) * 100
q1_venta = df_sales['Monto_Venta'].quantile(0.25)
q3_venta = df_sales['Monto_Venta'].quantile(0.75)
iqr_venta = q3_venta - q1_venta
skew_venta = df_sales['Monto_Venta'].skew()

print(f"Media: ${media_venta:.2f}")
print(f"Mediana: ${mediana_venta:.2f}")
print(f"Desviación Estándar: ${std_venta:.2f}")
print(f"Coeficiente de Variación (CV): {cv_venta:.2f}%")
print(f"IQR: ${iqr_venta:.2f} (Q1: ${q1_venta:.2f} | Q3: ${q3_venta:.2f})")
print(f"Asimetría (Skewness): {skew_venta:.2f} -> Sesgo positivo a la derecha")

plt.figure(figsize=(8, 4))
sns.histplot(df_sales['Monto_Venta'], kde=True, bins=30)
plt.title('Distribución de Monto de Venta (Sesgo Positivo)')
plt.xlabel('Monto_Venta (USD)')
plt.ylabel('Frecuencia')
plt.tight_layout()
plt.savefig('p1_hist_monto_venta.png')
plt.show()


# ==========================================================
# PRÁCTICA 2: CATEGORÍAS, CORRELACIONES Y REGRESIÓN
# ==========================================================
print("\n==========================================================")
print("PRÁCTICA 2: CATEGORÍAS, CORRELACIONES Y REGRESIÓN")
print("==========================================================")
df_cust = pd.read_csv('unidad4-click-and-buy-customer-metrics.csv')

stats_cat = df_sales.groupby('Categoria')['Monto_Venta'].agg(['count', 'mean', 'median', 'std'])
stats_cat['CV_%'] = (stats_cat['std'] / stats_cat['mean']) * 100
print("\nEstadísticos de Monto_Venta por Categoría:")
print(stats_cat.round(2))

plt.figure(figsize=(9, 4))
sns.boxplot(x='Categoria', y='Monto_Venta', data=df_sales)
plt.title('Boxplot de Monto de Venta por Categoría')
plt.xlabel('Categoría')
plt.ylabel('Monto_Venta (USD)')
plt.tight_layout()
plt.savefig('p2_boxplot_categoria.png')
plt.show()

cols_corr = ['Ingreso_Anual_kUSD', 'Total_Compras', 'Ticket_Promedio', 'Puntaje_Fidelidad']
corr_matrix = df_cust[cols_corr].corr()
print("\nMatriz de correlación (Clientes):")
print(corr_matrix.round(4))

plt.figure(figsize=(7, 5))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f')
plt.title('Mapa de Calor de Correlaciones de Clientes')
plt.tight_layout()
plt.savefig('p2_heatmap_clientes.png')
plt.show()

r_entrega_sat = df_sales['Dias_Entrega'].corr(df_sales['Satisfaccion_Cliente'])
print(f"\nCorrelación de Pearson (Dias_Entrega vs Satisfaccion_Cliente): r = {r_entrega_sat:.2f}")

plt.figure(figsize=(7, 4))
sns.regplot(x='Dias_Entrega', y='Satisfaccion_Cliente', data=df_sales)
plt.title('Regresión Bivariada: Días de Entrega vs Satisfacción del Cliente')
plt.xlabel('Días de Entrega')
plt.ylabel('Satisfacción del Cliente')
plt.tight_layout()
plt.savefig('p2_regplot_entrega_satisfaccion.png')
plt.show()


# ==========================================================
# PRÁCTICA 3: EDAD, RANGO ETARIO Y SCATTER PLOT
# ==========================================================
print("\n==========================================================")
print("PRÁCTICA 3: EDAD, SEGMENTACIÓN ETARIA Y FIDELIDAD")
print("==========================================================")
edad = df_cust['Edad']
print(
    f"Edad -> Media: {edad.mean():.2f} | Mediana: {edad.median():.2f} | "
    f"Std: {edad.std():.2f} | Mín: {edad.min()} | Máx: {edad.max()} | "
    f"Skew: {edad.skew():.2f}"
)

def clasificar_edad(valor):
    if pd.isna(valor):
        return np.nan
    if valor < 30:
        return 'Joven'
    elif valor <= 50:
        return 'Adulto'
    else:
        return 'Senior'

df_cust['Rango_Etario'] = df_cust['Edad'].apply(clasificar_edad)

resumen_etario = df_cust.groupby('Rango_Etario').agg(
    Cantidad_Clientes=('Puntaje_Fidelidad', 'count'),
    Media_Puntaje_Fidelidad=('Puntaje_Fidelidad', 'mean'),
    Mediana_Ticket_Promedio=('Ticket_Promedio', 'median')
)
print("\nResumen por Rango_Etario:")
print(resumen_etario.round(2))

plt.figure(figsize=(8, 5))
sns.scatterplot(
    data=df_cust,
    x='Total_Compras',
    y='Puntaje_Fidelidad',
    hue='Categoria_Preferida',
    alpha=0.75
)
plt.title('Total de Compras vs Puntaje de Fidelidad por Categoría Preferida')
plt.xlabel('Total de Compras')
plt.ylabel('Puntaje de Fidelidad')
plt.tight_layout()
plt.savefig('p3_scatter_fidelidad.png')
plt.show()

conclusion_negocio = (
    "Conclusión de negocio: el segmento Adulto (30-50 años) concentra la mayor "
    "cantidad de clientes (616 de 1000, ~61.6%) con una fidelidad media de 78.69, "
    "mientras que Joven (<30) muestra la fidelidad promedio levemente más alta "
    "(79.60) y Senior (>50) la mediana de ticket más elevada ($150.65). "
    "Como Total_Compras y Puntaje_Fidelidad tienen correlación positiva fuerte "
    "(r = +0.76), fomentar la recurrencia de compra impulsa directamente la fidelidad."
)
print("\n" + conclusion_negocio)