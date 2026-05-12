# Evaluacion Parcial 1 y 2 - Sistema Hospitalario
## SCY1101 - Programacion para la Ciencia de Datos

## Descripcion
Proyecto completo de ciencia de datos sobre un sistema hospitalario.
Incluye pipelines de datos con Kedro y modelos de machine learning.

## Requisitos
- Python 3.10 o superior
- uv o pip

## Instalacion

### 1. Clonar el repositorio
git clone https://github.com/matiasCaileo/evaluacion-kedro.git
cd evaluacion-kedro/evaluacion

### 2. Crear y activar entorno virtual
uv venv
.venv\Scripts\activate

### 3. Instalar dependencias
uv pip install -r requirements.txt
uv pip install scikit-learn imbalanced-learn joblib

### 4. Agregar los datasets en data/01_raw/
consultas.csv
examenes.csv
medicamentos.csv
pacientes.csv

## Evaluacion Parcial 1 - Pipelines Kedro

### Ejecutar pipeline completo
kedro run

### Pipelines disponibles
kedro run --pipeline=ingestion
kedro run --pipeline=cleaning
kedro run --pipeline=transform
kedro run --pipeline=validation

### Visualizar pipeline
kedro viz run

## Evaluacion Parcial 2 - Machine Learning

### Notebooks en orden de ejecucion
1. notebooks/01_exploratory_analysis.ipynb
2. notebooks/02_supervised_modeling.ipynb
3. notebooks/03_model_evaluation.ipynb
4. notebooks/04_hyperparameter_optimization.ipynb
5. notebooks/05_final_analysis.ipynb

### Abrir notebooks
jupyter notebook

## Estructura del proyecto
evaluacion/
├── conf/base/
│   ├── catalog.yml
│   └── parameters.yml
├── data/
│   ├── 01_raw/          - CSV originales
│   ├── 02_intermediate/ - Datos limpios
│   ├── 03_primary/      - Datos integrados
│   └── 08_reporting/    - Reportes
├── docs/
│   └── informe_tecnico_ev2.docx
├── notebooks/           - 5 notebooks ML
├── src/
│   ├── data_preprocessing.py
│   ├── model_training.py
│   ├── model_evaluation.py
│   ├── hyperparameter_tuning.py
│   ├── models/trained_models/
│   └── results/metrics/, plots/
└── requirements.txt

## Resultados
| Modelo | F1 Score |
|---|---|
| Random Forest Optimizado | 0.6537 |
| Gradient Boosting Optimizado | 0.6287 |
| Decision Tree | 0.6031 |

## Tecnologias
- Kedro 1.3.0
- Pandas, NumPy
- Scikit-learn
- Matplotlib, Seaborn
- PyArrow, Parquet
- uv