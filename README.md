# Examen Extemporáneo - Herramientas de Visualización
## Análisis de Ventas E-commerce 2024

### Información del Estudiante
- **Nombre:** Paulina Chiquete Ayala
- **Matrícula:** 2109037
- **Materia:** Herramientas de Visualización - Ingeniería de Datos
- **Fecha:** 12/08/2025

---

## 📁 Estructura del Proyecto

```
examen-ecommerce-2024/
├── ecommerce_dataset_examen.csv          # Dataset original
├── ecommerce_dataset_procesado.csv       # Dataset con variables derivadas
├── analisis_completo.py                  # Código principal del análisis
├── presentacion_ecommerce.html           # Presentación HTML interactiva
├── dashboard_interactivo.html             # Dashboard con Plotly
├── hallazgos_presentacion.json           # Datos para la presentación
├── informe_ejecutivo_manuscrito.pdf      # Informe ejecutivo (escaneado)
├── README.md                              # Este archivo
└── visualizaciones/
    ├── histogramas_distribucion.png
    ├── barras_ventas_categoria.png
    ├── linea_ventas_mes.png
    ├── dispersion_precio_satisfaccion.png
    ├── heatmap_correlaciones.png
    ├── boxplot_satisfaccion_categoria.png
    ├── series_tiempo_ventas_diarias.png
    └── analisis_adicional_multiples.png
```

---

## 🚀 Instrucciones de Ejecución

### Prerrequisitos
```bash
pip install pandas numpy matplotlib seaborn plotly
```

### Ejecución del Análisis Completo
```bash
# 1. Asegúrate de que el archivo ecommerce_dataset_examen.csv esté en el directorio
# 2. Ejecuta el script principal:
python analisis_completo.py

# 3. Abre la presentación HTML:
# Abrir presentacion_ecommerce.html en el navegador

# 4. Ver dashboard interactivo:
# Abrir dashboard_interactivo.html en el navegador
```


## 🔍 Hallazgos Principales

### 1. Patrones Temporales
- **Mes de mayor venta:** [Se determina al ejecutar el código]
- **Hora pico:** [Se determina al ejecutar el código]
- **Estacionalidad:** Identificada en el análisis temporal

### 2. Perfil Demográfico Rentable
- **Segmento objetivo:** [Se determina al ejecutar el código]
- **Características:** Edad, género y comportamiento de compra
- **Ticket promedio:** Calculado por segmento

### 3. Categorías de Productos
- **Categoría líder:** Mayor volumen de ventas
- **Mejor margen:** Considerando descuentos aplicados
- **Satisfacción por categoría:** Análisis comparativo

### 4. Factores de Satisfacción
- **Variables predictoras:** Identificadas via correlación
- **Impacto del tiempo de entrega:** Cuantificado
- **Relación precio-satisfacción:** Documentada

---

## 📈 Recomendaciones Estratégicas

### 1. Optimización Temporal
- Campañas promocionales en horarios de baja actividad
- Estrategias específicas para meses de menor venta
- Optimización de recursos en horas pico

### 2. Mejora Logística
- Reducción
