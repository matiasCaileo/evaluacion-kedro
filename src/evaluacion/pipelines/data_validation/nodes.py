"""Nodos del pipeline de validación de datos."""
import pandas as pd
import numpy as np


def validar_integridad(df: pd.DataFrame) -> pd.DataFrame:
    """
    Verifica la integridad del dataset integrado.

    Args:
        df: DataFrame integrado a validar
    Returns:
        DataFrame con reporte de validación
    """
    reporte = {
        "total_filas": df.shape[0],
        "total_columnas": df.shape[1],
        "nulos_restantes": int(df.isnull().sum().sum()),
        "duplicados_restantes": int(df.duplicated().sum()),
        "porcentaje_nulos": round(df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100, 2),
    }

    print("\n✅ Reporte de validación:")
    for k, v in reporte.items():
        print(f"  {k}: {v}")

    return pd.DataFrame([reporte])


def comparar_antes_despues(
    raw: pd.DataFrame,
    limpio: pd.DataFrame,
    nombre: str,
) -> pd.DataFrame:
    """
    Compara el dataset antes y después de la limpieza.

    Args:
        raw: Dataset original
        limpio: Dataset limpio
        nombre: Nombre del dataset
    Returns:
        DataFrame con comparación
    """
    comparacion = {
        "dataset": nombre,
        "filas_antes": raw.shape[0],
        "filas_despues": limpio.shape[0],
        "filas_eliminadas": raw.shape[0] - limpio.shape[0],
        "nulos_antes": int(raw.isnull().sum().sum()),
        "nulos_despues": int(limpio.isnull().sum().sum()),
        "nulos_eliminados": int(raw.isnull().sum().sum() - limpio.isnull().sum().sum()),
    }

    print(f"\n📊 Comparación {nombre}:")
    for k, v in comparacion.items():
        print(f"  {k}: {v}")

    return pd.DataFrame([comparacion])


def generar_reporte_final(
    val_consultas: pd.DataFrame,
    val_examenes: pd.DataFrame,
    val_medicamentos: pd.DataFrame,
    val_pacientes: pd.DataFrame,
    val_integrado: pd.DataFrame,
) -> pd.DataFrame:
    """
    Genera el reporte final de validación consolidado.

    Args:
        val_consultas: Comparación consultas
        val_examenes: Comparación exámenes
        val_medicamentos: Comparación medicamentos
        val_pacientes: Comparación pacientes
        val_integrado: Validación dataset integrado
    Returns:
        DataFrame con reporte final consolidado
    """
    reporte = pd.concat([
        val_consultas,
        val_examenes,
        val_medicamentos,
        val_pacientes,
    ], ignore_index=True)

    print("\n🎉 Reporte final de validación:")
    print(reporte)

    return reporte