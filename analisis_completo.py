import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configuración de estilo
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


print("="*70)
print("CARGANDO Y EXPLORANDO EL DATASET")
print("="*70)

# Cargar el dataset
df = pd.read_csv('C:/Users/pauli/Downloads/Analisis extempo/ecommerce_dataset_examen.csv')

print(f"Dimensiones del dataset: {df.shape}")
print(f"\nPrimeras 5 filas:")
print(df.head())

print(f"\nInformación general del dataset:")
print(df.info())

print(f"\nTipos de datos:")
print(df.dtypes)

print("\n" + "="*70)
print("1.1 LIMPIEZA Y PREPARACIÓN DE DATOS")
print("="*70)

# Verificar valores nulos
print("Valores nulos por columna:")
print(df.isnull().sum())

# Verificar duplicados
print(f"\nRegistros duplicados: {df.duplicated().sum()}")

# Validar y corregir tipos de datos
print("\nConvertir purchase_date a datetime...")
df['purchase_date'] = pd.to_datetime(df['purchase_date'])

# Crear variables derivadas
print("Creando variables derivadas...")

# Variable: mes de compra
df['purchase_month'] = df['purchase_date'].dt.month
df['purchase_month_name'] = df['purchase_date'].dt.month_name()

# Variable: día de la semana
df['purchase_weekday'] = df['purchase_date'].dt.day_name()

# Variable: franja horaria
def classify_hour(hour):
    if 6 <= hour < 12:
        return 'Mañana'
    elif 12 <= hour < 18:
        return 'Tarde'
    elif 18 <= hour < 24:
        return 'Noche'
    else:
        return 'Madrugada'

df['time_period'] = df['purchase_hour'].apply(classify_hour)

# Variable: precio con descuento
df['discounted_price'] = df['product_price'] * (1 - df['discount_applied']/100)

# Variable: margen (precio - costo de envío)
df['margin'] = df['discounted_price'] - df['shipping_cost']

# Variable: grupo de edad
def age_group(age):
    if age < 25:
        return '18-24'
    elif age < 35:
        return '25-34'
    elif age < 45:
        return '35-44'
    elif age < 55:
        return '45-54'
    else:
        return '55+'

df['age_group'] = df['customer_age'].apply(age_group)

print("Variables derivadas creadas exitosamente!")

print("\n" + "="*70)
print("1.2 ESTADÍSTICAS DESCRIPTIVAS")
print("="*70)

# Estadísticas descriptivas para variables numéricas
print("Estadísticas descriptivas - Variables numéricas:")
numeric_columns = ['customer_age', 'product_price', 'quantity', 'total_amount',
                  'discount_applied', 'shipping_cost', 'delivery_days', 'customer_satisfaction']
print(df[numeric_columns].describe())

# Identificación de outliers usando IQR
print("\nIdentificación de outliers:")
for col in numeric_columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    print(f"{col}: {len(outliers)} outliers ({len(outliers)/len(df)*100:.1f}%)")

# Distribución de variables categóricas
print("\nDistribución de variables categóricas:")
categorical_columns = ['customer_gender', 'product_category', 'payment_method', 'return_flag']
for col in categorical_columns:
    print(f"\n{col}:")
    print(df[col].value_counts())

print("\n" + "="*70)
print("1.3 INSIGHTS PRELIMINARES")
print("="*70)

print("HALLAZGOS INICIALES:")
print("1. Análisis de ventas por categoría:")
ventas_categoria = df.groupby('product_category')['total_amount'].sum().sort_values(ascending=False)
print(ventas_categoria)

print(f"\n2. Satisfacción promedio del cliente: {df['customer_satisfaction'].mean():.2f}/5")
satisfaccion_categoria = df.groupby('product_category')['customer_satisfaction'].mean().sort_values(ascending=False)
print("Satisfacción por categoría:")
print(satisfaccion_categoria)

print(f"\n3. Tasa de devolución general: {(df['return_flag'] == 'Sí').sum() / len(df) * 100:.1f}%")
devolucion_categoria = df[df['return_flag'] == 'Sí'].groupby('product_category').size()
print("Devoluciones por categoría:")
print(devolucion_categoria)

print("\nHIPÓTESIS PARA ANÁLISIS POSTERIOR:")
print("1. Las categorías con mayor precio promedio tienen mayor margen pero menor volumen")
print("2. Los tiempos de entrega largos están correlacionados con mayor tasa de devolución")
print("3. Ciertos métodos de pago están asociados con mayores montos de compra")


print("\n" + "="*70)
print("PARTE 2: VISUALIZACIONES Y ANÁLISIS")
print("="*70)

# Configurar el estilo de las gráficas
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# HISTOGRAMA - Distribución de edades de clientes
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.hist(df['customer_age'], bins=20, edgecolor='black', alpha=0.7)
plt.title('Distribución de Edades de Clientes')
plt.xlabel('Edad')
plt.ylabel('Frecuencia')

# HISTOGRAMA - Distribución de montos de transacción
plt.subplot(1, 2, 2)
plt.hist(df['total_amount'], bins=30, edgecolor='black', alpha=0.7)
plt.title('Distribución de Montos de Transacción')
plt.xlabel('Monto Total (MXN)')
plt.ylabel('Frecuencia')
plt.tight_layout()
plt.savefig('histogramas_distribucion.png', dpi=300, bbox_inches='tight')
plt.show()

# GRÁFICO DE BARRAS - Ventas por categoría
plt.figure(figsize=(12, 6))
ventas_cat = df.groupby('product_category')['total_amount'].sum().sort_values(ascending=True)
plt.barh(ventas_cat.index, ventas_cat.values)
plt.title('Ventas Totales por Categoría de Producto')
plt.xlabel('Ventas Totales (MXN)')
plt.ylabel('Categoría')
for i, v in enumerate(ventas_cat.values):
    plt.text(v, i, f'${v:,.0f}', va='center', ha='left')
plt.tight_layout()
plt.savefig('barras_ventas_categoria.png', dpi=300, bbox_inches='tight')
plt.show()

# GRÁFICO DE LÍNEA TEMPORAL - Ventas por mes
plt.figure(figsize=(12, 6))
ventas_mes = df.groupby('purchase_month')['total_amount'].sum()
meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
         'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
plt.plot(ventas_mes.index, ventas_mes.values, marker='o', linewidth=2, markersize=6)
plt.title('Evolución de Ventas por Mes (2024)')
plt.xlabel('Mes')
plt.ylabel('Ventas Totales (MXN)')
plt.xticks(range(1, 13), meses)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('linea_ventas_mes.png', dpi=300, bbox_inches='tight')
plt.show()

# DIAGRAMA DE DISPERSIÓN - Precio vs Satisfacción del Cliente
plt.figure(figsize=(10, 6))
scatter = plt.scatter(df['product_price'], df['customer_satisfaction'],
                     c=df['discount_applied'], cmap='viridis', alpha=0.6)
plt.colorbar(scatter, label='Descuento Aplicado (%)')
plt.title('Relación entre Precio del Producto y Satisfacción del Cliente')
plt.xlabel('Precio del Producto (MXN)')
plt.ylabel('Satisfacción del Cliente (1-5)')
plt.tight_layout()
plt.savefig('dispersion_precio_satisfaccion.png', dpi=300, bbox_inches='tight')
plt.show()

# HEATMAP DE CORRELACIONES
plt.figure(figsize=(12, 8))
correlation_vars = ['customer_age', 'product_price', 'quantity', 'total_amount',
                   'discount_applied', 'shipping_cost', 'delivery_days', 'customer_satisfaction']
correlation_matrix = df[correlation_vars].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
            square=True, linewidths=0.5)
plt.title('Matriz de Correlaciones - Variables Numéricas')
plt.tight_layout()
plt.savefig('heatmap_correlaciones.png', dpi=300, bbox_inches='tight')
plt.show()

# BOX PLOTS por categorías - Satisfacción del cliente por categoría
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='product_category', y='customer_satisfaction')
plt.title('Distribución de Satisfacción del Cliente por Categoría')
plt.xlabel('Categoría de Producto')
plt.ylabel('Satisfacción del Cliente')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('boxplot_satisfaccion_categoria.png', dpi=300, bbox_inches='tight')
plt.show()

# GRÁFICO DE SERIES DE TIEMPO - Ventas diarias
df_daily = df.groupby('purchase_date').agg({
    'total_amount': 'sum',
    'transaction_id': 'count'
}).reset_index()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

# Ventas diarias
ax1.plot(df_daily['purchase_date'], df_daily['total_amount'], alpha=0.7)
ax1.set_title('Ventas Diarias 2024')
ax1.set_ylabel('Ventas Totales (MXN)')
ax1.grid(True, alpha=0.3)

# Número de transacciones diarias
ax2.plot(df_daily['purchase_date'], df_daily['transaction_id'], color='orange', alpha=0.7)
ax2.set_title('Número de Transacciones Diarias 2024')
ax2.set_xlabel('Fecha')
ax2.set_ylabel('Número de Transacciones')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('series_tiempo_ventas_diarias.png', dpi=300, bbox_inches='tight')
plt.show()

# VISUALIZACIÓN ADICIONAL - Análisis por franja horaria
plt.figure(figsize=(14, 8))

# Subplot 1: Ventas por hora del día
plt.subplot(2, 2, 1)
ventas_hora = df.groupby('purchase_hour')['total_amount'].sum()
plt.bar(ventas_hora.index, ventas_hora.values)
plt.title('Ventas por Hora del Día')
plt.xlabel('Hora')
plt.ylabel('Ventas Totales (MXN)')

# Subplot 2: Número de transacciones por franja horaria
plt.subplot(2, 2, 2)
trans_franja = df['time_period'].value_counts()
plt.pie(trans_franja.values, labels=trans_franja.index, autopct='%1.1f%%')
plt.title('Distribución de Transacciones por Franja Horaria')

# Subplot 3: Satisfacción por método de pago
plt.subplot(2, 2, 3)
sat_pago = df.groupby('payment_method')['customer_satisfaction'].mean()
plt.bar(sat_pago.index, sat_pago.values)
plt.title('Satisfacción Promedio por Método de Pago')
plt.xlabel('Método de Pago')
plt.ylabel('Satisfacción Promedio')
plt.xticks(rotation=45)

# Subplot 4: Relación entre días de entrega y devoluciones
plt.subplot(2, 2, 4)
delivery_returns = df.groupby('delivery_days').agg({
    'return_flag': lambda x: (x == 'Sí').sum() / len(x) * 100
}).reset_index()
delivery_returns.columns = ['delivery_days', 'return_rate']
plt.scatter(delivery_returns['delivery_days'], delivery_returns['return_rate'])
plt.title('Tasa de Devolución vs Días de Entrega')
plt.xlabel('Días de Entrega')
plt.ylabel('Tasa de Devolución (%)')

plt.tight_layout()
plt.savefig('analisis_adicional_multiples.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "="*70)
print("2.3 ANÁLISIS DE CORRELACIONES SIGNIFICATIVAS")
print("="*70)

# Encontrar las 3 correlaciones más significativas
correlation_matrix = df[correlation_vars].corr()
correlation_pairs = []

for i in range(len(correlation_matrix.columns)):
    for j in range(i+1, len(correlation_matrix.columns)):
        var1 = correlation_matrix.columns[i]
        var2 = correlation_matrix.columns[j]
        corr_value = correlation_matrix.iloc[i, j]
        correlation_pairs.append((var1, var2, abs(corr_value), corr_value))

# Ordenar por valor absoluto de correlación
correlation_pairs.sort(key=lambda x: x[2], reverse=True)

print("TOP 3 CORRELACIONES MÁS SIGNIFICATIVAS:")
for i, (var1, var2, abs_corr, corr) in enumerate(correlation_pairs[:3], 1):
    print(f"{i}. {var1} vs {var2}: {corr:.3f}")

    # Explicar relevancia de negocio
    if var1 == 'product_price' and var2 == 'total_amount':
        print("   Relevancia: Mayor precio unitario genera mayores ingresos por transacción")
    elif var1 == 'quantity' and var2 == 'total_amount':
        print("   Relevancia: Mayor cantidad comprada incrementa el valor total de la venta")
    elif var1 == 'delivery_days' and var2 == 'customer_satisfaction':
        print("   Relevancia: Entregas más rápidas mejoran la satisfacción del cliente")
    elif var1 == 'discount_applied' and var2 == 'customer_satisfaction':
        print("   Relevancia: Los descuentos pueden influir en la percepción de valor del cliente")
    else:
        print("   Relevancia: Esta correlación requiere análisis más profundo para interpretación de negocio")
    print()

print("\n" + "="*70)
print("ANÁLISIS INFORME EJECUTIVO")
print("="*70)

print("\n1. ¿En qué meses y horas del día se concentran las ventas?")
print("-" * 60)
ventas_mes = df.groupby('purchase_month_name')['total_amount'].sum().sort_values(ascending=False)
print("TOP 3 meses con mayores ventas:")
print(ventas_mes.head(3))

ventas_hora = df.groupby('purchase_hour')['total_amount'].sum().sort_values(ascending=False)
print(f"\nTOP 3 horas con mayores ventas:")
print(ventas_hora.head(3))

print("\n2. ¿Cuál es el perfil demográfico más rentable?")
print("-" * 60)
perfil_demografico = df.groupby(['age_group', 'customer_gender']).agg({
    'total_amount': ['sum', 'mean', 'count'],
    'customer_satisfaction': 'mean'
}).round(2)
perfil_demografico.columns = ['Ventas_Total', 'Ticket_Promedio', 'Num_Transacciones', 'Satisfaccion_Prom']
perfil_demografico = perfil_demografico.sort_values('Ventas_Total', ascending=False)
print("Top 5 perfiles demográficos por ventas totales:")
print(perfil_demografico.head())

print("\n3. ¿Qué categorías tienen mejor margen considerando descuentos?")
print("-" * 60)
margen_categoria = df.groupby('product_category').agg({
    'margin': 'mean',
    'discount_applied': 'mean',
    'total_amount': 'sum'
}).round(2)
margen_categoria = margen_categoria.sort_values('margin', ascending=False)
print(margen_categoria)

print("\n4. ¿Qué variables predicen mejor la satisfacción del cliente?")
print("-" * 60)
satisfaction_corr = df[correlation_vars].corr()['customer_satisfaction'].abs().sort_values(ascending=False)
print("Variables más correlacionadas con satisfacción del cliente:")
print(satisfaction_corr[1:])  # Excluir la correlación consigo misma

print("\n5. ¿Cómo afecta el tiempo de entrega a las devoluciones?")
print("-" * 60)
delivery_analysis = df.groupby('delivery_days').agg({
    'return_flag': lambda x: (x == 'Sí').sum() / len(x) * 100,
    'total_amount': 'count'
}).round(2)
delivery_analysis.columns = ['Tasa_Devolucion_Pct', 'Num_Transacciones']
delivery_analysis = delivery_analysis.sort_values('Tasa_Devolucion_Pct', ascending=False)
print("Análisis de devoluciones por días de entrega:")
print(delivery_analysis)

# Correlación entre días de entrega y devoluciones
df['return_numeric'] = (df['return_flag'] == 'Sí').astype(int)
corr_delivery_return = df['delivery_days'].corr(df['return_numeric'])
print(f"\nCorrelación entre días de entrega y devoluciones: {corr_delivery_return:.3f}")


# Guardar el dataset procesado con variables derivadas
df.to_csv('ecommerce_dataset_procesado.csv', index=False)
print("\nDataset procesado guardado como: ecommerce_dataset_procesado.csv")

# Crear resumen estadístico para el informe
summary_stats = {
    'total_transactions': len(df),
    'total_revenue': df['total_amount'].sum(),
    'avg_ticket': df['total_amount'].mean(),
    'avg_satisfaction': df['customer_satisfaction'].mean(),
    'return_rate': (df['return_flag'] == 'Sí').sum() / len(df) * 100,
    'top_category': df.groupby('product_category')['total_amount'].sum().idxmax(),
    'top_month': df.groupby('purchase_month_name')['total_amount'].sum().idxmax(),
    'peak_hour': df.groupby('purchase_hour')['total_amount'].sum().idxmax()
}

print("\n" + "="*70)
print("RESUMEN ESTADÍSTICO PARA EL INFORME EJECUTIVO")
print("="*70)
for key, value in summary_stats.items():
    print(f"{key}: {value}")


print("\n" + "="*70)
print("GENERANDO VISUALIZACIONES INTERACTIVAS")
print("="*70)

# Dashboard interactivo con Plotly
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Ventas por Categoría', 'Satisfacción vs Precio',
                    'Ventas por Mes', 'Distribución de Edades'),
    specs=[[{"type": "bar"}, {"type": "scatter"}],
           [{"type": "scatter"}, {"type": "histogram"}]]
)

# Gráfico 1: Ventas por categoría
ventas_cat = df.groupby('product_category')['total_amount'].sum().sort_values(ascending=False)
fig.add_trace(
    go.Bar(x=ventas_cat.index, y=ventas_cat.values, name="Ventas"),
    row=1, col=1
)

# Gráfico 2: Satisfacción vs Precio
fig.add_trace(
    go.Scatter(x=df['product_price'], y=df['customer_satisfaction'],
               mode='markers', name="Satisfacción vs Precio",
               marker=dict(color=df['discount_applied'], colorscale='viridis')),
    row=1, col=2
)

# Gráfico 3: Ventas por mes
ventas_mes = df.groupby('purchase_month')['total_amount'].sum()
fig.add_trace(
    go.Scatter(x=ventas_mes.index, y=ventas_mes.values,
               mode='lines+markers', name="Ventas Mensuales"),
    row=2, col=1
)

# Gráfico 4: Distribución de edades
fig.add_trace(
    go.Histogram(x=df['customer_age'], name="Distribución Edades"),
    row=2, col=2
)

fig.update_layout(height=800, title_text="Dashboard Interactivo - E-commerce Analytics")
fig.write_html("dashboard_interactivo.html")
print("Dashboard interactivo guardado como: dashboard_interactivo.html")

# Crear diccionario con todos los hallazgos para la presentación
hallazgos_presentacion = {
    'total_ventas': f"${df['total_amount'].sum():,.2f} MXN",
    'num_transacciones': f"{len(df):,}",
    'ticket_promedio': f"${df['total_amount'].mean():.2f} MXN",
    'satisfaccion_promedio': f"{df['customer_satisfaction'].mean():.2f}/5",
    'tasa_devolucion': f"{(df['return_flag'] == 'Sí').sum() / len(df) * 100:.1f}%",
    'categoria_top': ventas_categoria.index[0],
    'mes_top': df.groupby('purchase_month_name')['total_amount'].sum().idxmax(),
    'hora_pico': df.groupby('purchase_hour')['total_amount'].sum().idxmax(),
    'perfil_rentable': f"{perfil_demografico.index[0]}",
    'correlacion_principal': f"{correlation_pairs[0][0]} vs {correlation_pairs[0][1]}: {correlation_pairs[0][3]:.3f}"
}

# Convert numpy types to native Python types for JSON serialization
for key, value in hallazgos_presentacion.items():
    if isinstance(value, np.integer):
        hallazgos_presentacion[key] = int(value)
    elif isinstance(value, np.floating):
        hallazgos_presentacion[key] = float(value)
    elif isinstance(value, (np.ndarray, pd.Series)):
        hallazgos_presentacion[key] = value.tolist()
    else:
        hallazgos_presentacion[key] = str(value)


import json
with open('hallazgos_presentacion.json', 'w') as f:
    json.dump(hallazgos_presentacion, f, indent=4)

print("\nDatos para presentación guardados en: hallazgos_presentacion.json")