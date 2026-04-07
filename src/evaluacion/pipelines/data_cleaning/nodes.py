"""Nodos del pipeline de limpieza de datos."""
import pandas as pd
import numpy as np


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina filas duplicadas y limpia caracteres problemáticos.

    Args:
        df: DataFrame con posibles duplicados
    Returns:
        DataFrame sin duplicados y con caracteres limpios
    """
    n_antes = len(df)
    df = df.drop_duplicates()
    print(f"Duplicados eliminados: {n_antes - len(df)}")

    # Limpiar caracteres especiales problemáticos
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].apply(
            lambda x: x.encode("utf-8", errors="ignore").decode("utf-8")
            if isinstance(x, str) else x
        )

    return df


def estandarizar_fechas(df: pd.DataFrame, columnas: list) -> pd.DataFrame:
    """
    Estandariza fechas a formato YYYY-MM-DD.
    
    Args:
        df: DataFrame con columnas de fecha
        columnas: Lista de columnas a estandarizar
    Returns:
        DataFrame con fechas estandarizadas
    """
    for col in columnas:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
    return df


def limpiar_strings(df: pd.DataFrame, columnas: list) -> pd.DataFrame:
    """
    Normaliza strings: strip + Title Case.
    
    Args:
        df: DataFrame con columnas de texto
        columnas: Lista de columnas a limpiar
    Returns:
        DataFrame con strings normalizados
    """
    for col in columnas:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
    return df


def tratar_nulos(df: pd.DataFrame, estrategia: str = "median") -> pd.DataFrame:
    """
    Imputa valores nulos según estrategia elegida.

    Args:
        df: DataFrame con valores nulos
        estrategia: Estrategia de imputación (median/mean/mode)
    Returns:
        DataFrame sin valores nulos
    """
    # Columnas numéricas flotantes
    num_float = df.select_dtypes(include=["float64", "float32"]).columns
    # Columnas enteras (incluyendo Int64 nullable)
    num_int = df.select_dtypes(include=["Int64", "int64", "int32"]).columns
    # Columnas de texto
    cat = df.select_dtypes(include=["object"]).columns

    if estrategia == "median":
        df[num_float] = df[num_float].fillna(df[num_float].median())
        for col in num_int:
            df[col] = df[col].fillna(int(df[col].median()))
    elif estrategia == "mean":
        df[num_float] = df[num_float].fillna(df[num_float].mean())
        for col in num_int:
            df[col] = df[col].fillna(int(df[col].mean()))

    df[cat] = df[cat].fillna(df[cat].mode().iloc[0])

    print(f"Nulos restantes: {df.isnull().sum().sum()}")
    return df


def tratar_outliers(df: pd.DataFrame, umbral: float = 3.0) -> pd.DataFrame:
    """
    Elimina outliers usando Z-score.
    
    Args:
        df: DataFrame con posibles outliers
        umbral: Umbral de Z-score (default 3.0)
    Returns:
        DataFrame sin outliers
    """
    n_antes = len(df)
    num = df.select_dtypes(include=[np.number]).columns
    
    for col in num:
        z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
        df = df[z_scores < umbral]
    
    print(f"Outliers eliminados: {n_antes - len(df)}")
    return df


def convertir_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte columnas al tipo de dato correcto.
    
    Args:
        df: DataFrame con tipos incorrectos
    Returns:
        DataFrame con tipos corregidos
    """
    # Convertir IDs de float a int donde sea posible
    for col in df.columns:
        if 'id_' in col:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
        if col in ['costo', 'costo_unitario']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df