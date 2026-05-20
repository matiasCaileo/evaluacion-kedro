# Evaluacion Parcial 1 y 2 - Sistema Hospitalario
## SCY1101 - Programacion para la Ciencia de Datos

## Descripcion
Proyecto completo de ciencia de datos sobre un sistema hospitalario.
Incluye pipelines de datos con Kedro y modelos de machine learning.

## Enlace Dataset
https://www.kaggle.com/datasets/kanakbaghel/hospital-management-dataset

## Requisitos
- Python 3.10 o superior
- uv o pip

## IMPORTANTE - Pasos para ejecutar el proyecto

### PASO 1 - Clonar el repositorio
git clone https://github.com/matiasCaileo/evaluacion-kedro.git
cd evaluacion-kedro/evaluacion

### PASO 2 - Crear y activar entorno virtual
uv venv
.venv\Scripts\activate

### PASO 3 - Instalar dependencias
uv pip install -r requirements.txt
uv pip install scikit-learn imbalanced-learn joblib

### PASO 4 - Agregar los datasets originales
Copiar los 4 archivos CSV en la carpeta data/01_raw/:
data/01_raw/consultas.csv
data/01_raw/examenes.csv
data/01_raw/medicamentos.csv
data/01_raw/pacientes.csv

### PASO 5 - Ejecutar pipeline Kedro (OBLIGATORIO antes de los notebooks)
Este paso genera los datos limpios que usan los notebooks.
Sin este paso los notebooks fallaran.
kedro run

### PASO 6 - Abrir y ejecutar los notebooks en orden
jupyter notebook
Ejecutar en este orden usando Kernel - Restart and Run All:
1. notebooks/01_exploratory_analysis.ipynb
2. notebooks/02_supervised_modeling.ipynb
3. notebooks/03_model_evaluation.ipynb
4. notebooks/04_hyperparameter_optimization.ipynb
5. notebooks/05_final_analysis.ipynb

## Evaluacion Parcial 1 - Pipelines Kedro

### Pipelines disponibles
kedro run --pipeline=ingestion
kedro run --pipeline=cleaning
kedro run --pipeline=transform
kedro run --pipeline=validation

### Visualizar pipeline
kedro viz run

## Estructura del proyecto
evaluacion/
├── conf/base/
│   ├── catalog.yml       - Definicion de datasets
│   └── parameters.yml    - Parametros configurables
├── data/
│   ├── 01_raw/           - CSV originales (agregar aqui)
│   ├── 02_intermediate/  - Datos limpios generados por kedro run
│   ├── 03_primary/       - Datos integrados
│   └── 08_reporting/     - Reportes y visualizaciones
├── docs/
│   └── informe_tecnico_ev2.docx
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_supervised_modeling.ipynb
│   ├── 03_model_evaluation.ipynb
│   ├── 04_hyperparameter_optimization.ipynb
│   └── 05_final_analysis.ipynb
├── src/
│   ├── data_preprocessing.py
│   ├── model_training.py
│   ├── model_evaluation.py
│   ├── hyperparameter_tuning.py
│   ├── models/trained_models/  - Modelos serializados
│   └── results/
│       ├── metrics/            - Metricas en CSV
│       └── plots/              - Graficos en PNG
└── requirements.txt

## Resultados obtenidos
| Modelo | F1 Score |
|---|---|
| Random Forest Optimizado | 0.6537 |
| Gradient Boosting Optimizado | 0.6287 |
| Decision Tree | 0.6031 |

## Tecnologias utilizadas
- Kedro 1.3.0
- Pandas, NumPy
- Scikit-learn
- Matplotlib, Seaborn
- PyArrow, Parquet
- uv
