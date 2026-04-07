# Informe Técnico - Sistema Hospitalario
## SCY1101 Programación para la Ciencia de Datos

---

## 1. Resumen Ejecutivo

El presente proyecto desarrolla un flujo completo de transformación de datos para un sistema hospitalario, utilizando el framework Kedro como herramienta de orquestación. Se procesaron 4 datasets con información de pacientes, consultas médicas, exámenes de laboratorio y prescripciones de medicamentos, aplicando técnicas avanzadas de limpieza, transformación e integración de datos.

**Resultados clave:**
- 2.369 registros procesados en total
- 69 duplicados eliminados
- Dataset final integrado: 349 pacientes con 5 variables agregadas
- 4 pipelines modulares implementados y ejecutables

---

## 2. Análisis Exploratorio

### 2.1 Descripción de los Datasets

| Dataset | Filas originales | Columnas | Nulos | Duplicados |
|---|---|---|---|---|
| pacientes | 412 | 8 | 159 (4.82%) | 12 |
| consultas | 824 | 8 | 449 (6.81%) | 24 |
| examenes | 618 | 8 | 237 (4.79%) | 18 |
| medicamentos | 515 | 7 | 180 (4.99%) | 15 |

### 2.2 Problemas de Calidad Detectados

- **Valores nulos:** presentes en todas las columnas con un promedio del 5.35%
- **Duplicados:** entre 3% y 4% en cada dataset
- **Fechas en formatos mixtos:** DD/MM/YYYY y YYYY-MM-DD coexistían en los mismos campos
- **Strings inconsistentes:** especialidades médicas en mayúsculas, minúsculas y título
- **Tipos de datos incorrectos:** IDs como float64 en vez de enteros, costos como strings
- **Caracteres especiales:** bytes inválidos en campos de texto (encoding mixto)

---

## 3. Metodología

### 3.1 Arquitectura del Proyecto

El proyecto sigue la estructura estándar de Kedro con 4 pipelines modulares:

**Pipeline 1 - Data Ingestion (AD 1.1)**
Responsable de cargar los 4 archivos CSV desde `data/01_raw/` y generar un reporte de diagnóstico inicial con métricas de calidad por dataset.

**Pipeline 2 - Data Cleaning (AD 1.2)**
Aplica el siguiente flujo de limpieza para cada dataset:
1. Eliminación de duplicados y limpieza de caracteres especiales
2. Conversión de tipos de datos (IDs a Int64, costos a float)
3. Estandarización de fechas a formato YYYY-MM-DD
4. Normalización de strings (strip + Title Case)
5. Imputación de nulos (mediana para numéricos, moda para categóricos)
6. Detección y eliminación de outliers con Z-score (umbral: 3.0)

**Pipeline 3 - Data Transformation (AD 1.3)**
1. Join de los 4 datasets usando id_paciente e id_consulta
2. Creación de features derivadas: edad, costo_total, tiene_examen, tiene_medicamento
3. Normalización MinMax de variables numéricas
4. Label Encoding de variables categóricas
5. Agregación por paciente con groupby

**Pipeline 4 - Data Validation (AD 1.4)**
Verifica la integridad del dataset final y genera reportes de comparación antes/después para cada dataset.

### 3.2 Decisiones Técnicas

**Encoding de caracteres:** Los archivos CSV originales contenían bytes inválidos (0x8d) incompatibles con encodings estándar. Se utilizó `latin-1` con `encoding_errors: ignore` para la lectura, y se limpió el contenido antes de guardar en formato Parquet.

**Formato Parquet:** Se eligió Parquet para los datasets intermedios en vez de CSV por sus ventajas en rendimiento, compresión y preservación de tipos de datos.

**Imputación por mediana:** Se eligió la mediana sobre la media para variables numéricas por ser más robusta ante outliers.

**Z-score para outliers:** Se utilizó Z-score con umbral 3.0 por ser adecuado para distribuciones aproximadamente normales.

---

## 4. Resultados y Validación

### 4.1 Resultados del Procesamiento

| Dataset | Filas originales | Filas finales | Reducción |
|---|---|---|---|
| consultas | 824 | 794 | 3.6% |
| examenes | 618 | 596 | 3.6% |
| medicamentos | 515 | 500 | 2.9% |
| pacientes | 412 | 400 | 2.9% |

### 4.2 Dataset Final Integrado

- **349 pacientes** únicos con historial completo
- **5 variables:** total_consultas, costo_promedio, total_examenes, total_medicamentos, id_paciente
- **0 valores nulos**
- **0 duplicados**

### 4.3 Features Creadas

| Feature | Descripción | Justificación |
|---|---|---|
| edad | Años del paciente calculados desde fecha_nacimiento | Variable predictiva clave en salud |
| costo_total | Suma de costo consulta + costo medicamento | Indicador de gasto total por atención |
| tiene_examen | 1 si la consulta tiene examen asociado | Indicador binario de complejidad |
| tiene_medicamento | 1 si la consulta tiene medicamento asociado | Indicador binario de tratamiento |

---

## 5. Conclusiones y Recomendaciones

### 5.1 Conclusiones

- El flujo de datos implementado en Kedro permite procesar de forma reproducible y modular los 4 datasets hospitalarios
- Los 4 pipelines ejecutan sin errores con `kedro run`
- La calidad de los datos mejoró significativamente tras el procesamiento
- El dataset final está listo para etapas posteriores de modelado predictivo

### 5.2 Recomendaciones

- Implementar validación de esquemas con Great Expectations para mayor robustez
- Agregar tests unitarios para cada nodo en la carpeta `tests/`
- Considerar un modelo predictivo de readmisión hospitalaria usando el dataset integrado
- Mejorar la imputación de nulos con modelos KNN para mayor precisión

---

## 6. Tecnologías Utilizadas

- **Python 3.11**
- **Kedro 1.3.0** — Orquestación del flujo de datos
- **Pandas** — Manipulación de datos
- **Scikit-learn** — Normalización y encoding
- **Matplotlib/Seaborn** — Visualización
- **PyArrow/Parquet** — Almacenamiento eficiente
- **uv** — Gestión del entorno virtual
- **Git/GitHub** — Control de versiones

---

*Informe generado como parte de la Evaluación Parcial N°1 — SCY1101 Programación para la Ciencia de Datos*
