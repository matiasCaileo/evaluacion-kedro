"""Nodos del pipeline de transformación de datos."""
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder


def integrar_datasets(
    consultas: pd.DataFrame,
    examenes: pd.DataFrame,
    medicamentos: pd.DataFrame,
    pacientes: pd.DataFrame,
) -> pd.DataFrame:
    """
    Integra los 4 datasets mediante joins.

    Args:
        consultas: DataFrame de consultas limpias
        examenes: DataFrame de exámenes limpios
        medicamentos: DataFrame de medicamentos limpios
        pacientes: DataFrame de pacientes limpios
    Returns:
        DataFrame integrado
    """
    # Join consultas con pacientes
    df = consultas.merge(pacientes, on="id_paciente", how="left")

    # Join con examenes
    df = df.merge(examenes, on="id_consulta", how="left")

    # Join con medicamentos
    df = df.merge(medicamentos, on="id_consulta", how="left")

    print(f"Dataset integrado: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df


def normalizar_columnas(df: pd.DataFrame, columnas: list) -> pd.DataFrame:
    """
    Normaliza columnas numéricas entre 0 y 1.

    Args:
        df: DataFrame con columnas a normalizar
        columnas: Lista de columnas a normalizar
    Returns:
        DataFrame con columnas normalizadas
    """
    scaler = MinMaxScaler()
    cols_existentes = [c for c in columnas if c in df.columns]

    if cols_existentes:
        df[cols_existentes] = scaler.fit_transform(df[cols_existentes].fillna(0))

    return df


def codificar_categoricas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Codifica variables categóricas usando Label Encoding.

    Args:
        df: DataFrame con columnas categóricas
    Returns:
        DataFrame con variables categóricas codificadas
    """
    cat_cols = df.select_dtypes(include=["object"]).columns
    le = LabelEncoder()

    for col in cat_cols:
        df[col] = le.fit_transform(df[col].astype(str))

    return df


def crear_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea nuevas variables derivadas del dataset integrado.

    Args:
        df: DataFrame integrado
    Returns:
        DataFrame con nuevas features
    """
    # Edad del paciente
    if "fecha_nacimiento" in df.columns:
        df["fecha_nacimiento"] = pd.to_datetime(df["fecha_nacimiento"], errors="coerce")
        df["edad"] = (pd.Timestamp.now() - df["fecha_nacimiento"]).dt.days // 365

    # Costo total por consulta
    if "costo_x" in df.columns and "costo_unitario" in df.columns:
        df["costo_total"] = df["costo_x"].fillna(0) + df["costo_unitario"].fillna(0)

    # Indicador de examen y medicamento
    df["tiene_examen"] = df["id_examen"].notna().astype(int)
    df["tiene_medicamento"] = df["id_prescripcion"].notna().astype(int)

    print(f"Features creadas: edad, costo_total, tiene_examen, tiene_medicamento")
    return df


def agregar_por_paciente(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera agregaciones por paciente usando groupby.

    Args:
        df: DataFrame integrado
    Returns:
        DataFrame con agregaciones por paciente
    """
    # Buscar columna de costo disponible
    costo_col = None
    for col in ["costo_x", "costo", "costo_total"]:
        if col in df.columns:
            costo_col = col
            break

    agg_dict = {
        "total_consultas": ("id_consulta", "count"),
        "total_examenes": ("id_examen", "count"),
        "total_medicamentos": ("id_prescripcion", "count"),
    }

    if costo_col:
        agg_dict["costo_promedio"] = (costo_col, "mean")

    agg = df.groupby("id_paciente").agg(**agg_dict).reset_index()

    print(f"Agregaciones por paciente: {agg.shape}")
    return agg