import pandas as pd

# ==========================================
# PRÁCTICA 1: CALIDAD Y TICKET PROMEDIO
# ==========================================
df_trans = pd.read_csv('click-and-buy-transactions.csv')

filas, columnas = df_trans.shape
print(f"El conjunto de datos contiene {filas} transacciones y {columnas} columnas.")

nulos_cliente = df_trans['ID_Cliente'].isna().sum()
porcentaje_nulos = (nulos_cliente / filas) * 100
print(f"Transacciones sin ID_Cliente: {nulos_cliente} ({porcentaje_nulos:.2f}%)")

df_exitosas = df_trans[df_trans['Estado'] == 'Exitoso']
print(f"Transacciones exitosas: {df_exitosas.shape[0]} de {filas}")

ticket_promedio = df_exitosas['Monto_USD'].mean()
print(f"Ticket promedio de transacciones exitosas: ${ticket_promedio:.2f} USD")


# ==========================================
# PRÁCTICA 2: EMBUDO Y PASARELAS DE PAGO
# ==========================================
df_logs = pd.read_csv('click-and-buy-web-logs.csv')
duplicados = df_logs.duplicated().sum()
df_logs_limpio = df_logs.drop_duplicates()
print(f"\nEventos duplicados eliminados: {duplicados} | Registros limpios: {df_logs_limpio.shape[0]}")

etapas_embudo = ['home', 'product_page', 'add_to_cart', 'checkout_start', 'purchase_success']
print("--- Embudo de Conversión (Usuarios Únicos) ---")
for etapa in etapas_embudo:
    usuarios_unicos = df_logs_limpio[df_logs_limpio['Pagina'] == etapa]['ID_Usuario'].nunique()
    print(f"Etapa {etapa:<18} -> Usuarios Únicos: {usuarios_unicos}")

def tasa_fallo(estado_series):
    return ((estado_series == 'Fallido').sum() / len(estado_series)) * 100

resumen_pasarelas = df_trans.groupby('Pasarela').agg(
    Latencia_Promedio_Seg=('Latencia_Seg', 'mean'),
    Tasa_Fallo_Porcentaje=('Estado', tasa_fallo),
    Transacciones_Totales=('ID_Transaccion', 'count')
)
print("\n--- Resumen de Rendimiento de Pasarelas ---")
print(resumen_pasarelas.round(2))

trans_fallidas_a = df_trans[(df_trans['Pasarela'] == 'CardGate A') & (df_trans['Estado'] == 'Fallido')]
total_perdido_usd = trans_fallidas_a['Monto_USD'].sum()
print(f"Pérdidas financieras directas (CardGate A): ${total_perdido_usd:,.2f} USD")


# ==========================================
# PRÁCTICA 3: CRM Y CRUCE CON TRANSACCIONES
# ==========================================
df_crm = pd.read_csv('click-and-buy-crm-reviews.csv')

print(f"\nCalificación promedio global: {df_crm['Calificacion'].mean():.2f}")
print("Opiniones por nivel de estrellas:")
print(df_crm['Calificacion'].value_counts().sort_index())

negativas = df_crm[df_crm['Calificacion'].isin([1, 2])].copy()
print(f"\nOpiniones negativas (1 o 2 estrellas): {len(negativas)}")

palabras_clave = ['pago', 'error', 'tarjeta', 'lento', 'checkout']
patron = '|'.join(palabras_clave)
negativas['vinculada'] = negativas['Comentario'].str.contains(patron, case=False, na=False)
cant_vinc = negativas['vinculada'].sum()
print(f"Negativas con palabras clave: {cant_vinc}/{len(negativas)} ({(cant_vinc/len(negativas))*100:.2f}%)")

cruce_neg = pd.merge(negativas, df_trans, on='ID_Cliente', how='inner')
pct_fallido = (cruce_neg['Estado'] == 'Fallido').mean() * 100
print(f"Registros en cruce CRM negativo x Transacciones: {len(cruce_neg)}")
print(f"Porcentaje 'Fallido' en el cruce: {pct_fallido:.2f}%")
print("Pasarelas en el cruce:")
print(cruce_neg['Pasarela'].value_counts())
print("Pasarelas en transacciones 'Fallido' del cruce:")
print(cruce_neg[cruce_neg['Estado'] == 'Fallido']['Pasarela'].value_counts())