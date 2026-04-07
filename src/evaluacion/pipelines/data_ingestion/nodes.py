"""Nodos del pipeline de ingesta y exploración de datos."""
import pandas as pd
import numpy as np


def explorar_dataset(df: pd.DataFrame, nombre: str) -> pd.DataFrame:
    """
    Explora un dataset y genera un reporte de diagnóstico inicial.

    Args:
        df: DataFrame a explorar
        nombre: Nombre del dataset
    Returns:
        DataFrame explorado con caracteres limpios
    """
    # Limpiar caracteres especiales en columnas de texto
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].apply(
            lambda x: str(x).encode("utf-8", errors="ignore").decode("utf-8")
            if pd.notna(x) else x
        )

    print(f"\n{'='*40}")
    print(f"Dataset: {nombre}")
    print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
    print(f"Duplicados: {df.duplicated().sum()}")
    print(f"Nulos:\n{df.isnull().sum()[df.isnull().sum() > 0]}")

    return df


def generar_reporte_diagnostico(
    consultas: pd.DataFrame,
    examenes: pd.DataFrame,
    medicamentos: pd.DataFrame,
    pacientes: pd.DataFrame,
) -> pd.DataFrame:
    """
    Genera un reporte consolidado de diagnóstico de todos los datasets.
    
    Args:
        consultas: DataFrame de consultas
        examenes: DataFrame de exámenes
        medicamentos: DataFrame de medicamentos
        pacientes: DataFrame de pacientes
    Returns:
        DataFrame con el reporte consolidado
    """
    reportes = []
    
    for nombre, df in [
        ("consultas", consultas),
        ("examenes", examenes),
        ("medicamentos", medicamentos),
        ("pacientes", pacientes),
    ]:
        reportes.append({
            "dataset": nombre,
            "filas": df.shape[0],
            "columnas": df.shape[1],
            "total_nulos": int(df.isnull().sum().sum()),
            "duplicados": int(df.duplicated().sum()),
            "porcentaje_nulos": round(df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100, 2),
        })
    
    reporte_df = pd.DataFrame(reportes)
    print("\nReporte de diagnóstico consolidado:")
    print(reporte_df)
    
    return reporte_df

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