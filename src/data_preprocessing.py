"""
Funciones de limpieza, transformación y preparación de datos.
Módulo de preprocesamiento para la Evaluación Parcial N°2.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split


def cargar_datos_limpios(filepath: str) -> pd.DataFrame:
    """
    Carga el dataset limpio desde Parquet.

    Args:
        filepath: Ruta al archivo Parquet
    Returns:
        DataFrame cargado
    """
    try:
        df = pd.read_parquet(filepath)
        print(f" Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
        return df
    except Exception as e:
        raise ValueError(f"Error al cargar datos: {e}")


def preparar_features_clasificacion(df: pd.DataFrame) -> tuple:
    """
    Prepara features para modelo de clasificación.
    Variable objetivo: resultado (local/visitante/empate)

    Args:
        df: DataFrame con datos de consultas limpios
    Returns:
        Tupla (X, y) con features y target
    """
    # Seleccionar columnas numéricas disponibles
    feature_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Eliminar columnas que no son features útiles
    cols_excluir = ['id', 'id_consulta', 'id_paciente', 'id_medico',
                    'id_examen', 'id_prescripcion', 'match_api_id']
    feature_cols = [c for c in feature_cols if c not in cols_excluir]

    # Variable objetivo: costo (alto/bajo)
    if 'costo' in df.columns:
        mediana = df['costo'].median()
        y = (df['costo'] > mediana).astype(int)
        feature_cols = [c for c in feature_cols if c != 'costo']
    else:
        raise ValueError("No se encontró columna objetivo válida")

    X = df[feature_cols].fillna(0)

    print(f"Features preparadas: {X.shape[1]} variables")
    print(f"Distribución target: {y.value_counts().to_dict()}")
    return X, y


def preparar_features_regresion(df: pd.DataFrame) -> tuple:
    """
    Prepara features para modelo de regresión.
    Variable objetivo: costo

    Args:
        df: DataFrame con datos limpios
    Returns:
        Tupla (X, y) con features y target
    """
    feature_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    cols_excluir = ['id', 'id_consulta', 'id_paciente', 'id_medico',
                    'id_examen', 'id_prescripcion', 'costo']
    feature_cols = [c for c in feature_cols if c not in cols_excluir]

    if 'costo' not in df.columns:
        raise ValueError("No se encontró columna 'costo' para regresión")

    X = df[feature_cols].fillna(0)
    y = df['costo'].fillna(df['costo'].median())

    print(f"Features para regresión: {X.shape[1]} variables")
    return X, y


def escalar_datos(X_train: pd.DataFrame, X_test: pd.DataFrame) -> tuple:
    """
    Escala los datos usando StandardScaler.

    Args:
        X_train: Features de entrenamiento
        X_test: Features de prueba
    Returns:
        Tupla (X_train_scaled, X_test_scaled, scaler)
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("Datos escalados con StandardScaler")
    return X_train_scaled, X_test_scaled, scaler


def dividir_datos(X, y, test_size: float = 0.2, random_state: int = 42) -> tuple:
    """
    Divide los datos en train y test.

    Args:
        X: Features
        y: Target
        test_size: Proporción del conjunto de prueba
        random_state: Semilla para reproducibilidad
    Returns:
        Tupla (X_train, X_test, y_train, y_test)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    print(f" Train: {X_train.shape[0]} filas | Test: {X_test.shape[0]} filas")
    return X_train, X_test, y_train, y_test