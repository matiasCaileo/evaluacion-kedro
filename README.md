# Evaluación Parcial 1 - Sistema Hospitalario
## SCY1101 Programación para la Ciencia de Datos

## Descripción
Proyecto de transformación de datos para un sistema hospitalario utilizando Kedro.
Procesa 4 datasets (pacientes, consultas, exámenes, medicamentos) aplicando
limpieza, transformación e integración de datos.

## Requisitos
- Python 3.10 o superior
- uv o pip

## Instalación paso a paso

### 1. Clonar el repositorio
```bash
git clone https://github.com/matiasCaileo/evaluacion-kedro.git
cd evaluacion-kedro/evaluacion
```

### 2. Crear y activar entorno virtual
```bash
uv venv
.venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
uv pip install -r requirements.txt
```

### 4. Agregar los datasets en data/01_raw/


### consultas.csv
### examenes.csv
### medicamentos.csv
### pacientes.csv

### 5. Ejecutar el pipeline
```bash
kedro run
```

### 6. Pipelines disponibles
```bash
kedro run --pipeline=ingestion
kedro run --pipeline=cleaning
kedro run --pipeline=transform
kedro run --pipeline=validation
```

### 7. Visualizar pipeline
```bash
kedro viz run
```

### 8. Notebook exploratorio
```bash
jupyter notebook
```

## Resultados
| Dataset | Filas originales | Filas finales |
|---|---|---|
| consultas | 824 | 794 |
| examenes | 618 | 596 |
| medicamentos | 515 | 500 |
| pacientes | 412 | 400 |

Dataset final integrado: 349 pacientes con 0 nulos

## Tecnologías
- Kedro 1.3.0
- Pandas
- Scikit-learn
- Matplotlib / Seaborn
- PyArrow / Parquet
- uv