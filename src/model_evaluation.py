"""
Funciones de evaluacion y comparacion de modelos.
Modulo de evaluacion para la Evaluacion Parcial N°2.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    mean_squared_error, mean_absolute_error, r2_score
)
from sklearn.model_selection import cross_val_score, StratifiedKFold, KFold


def evaluar_clasificacion(modelo, X_test, y_test, nombre: str) -> dict:
    """
    Evalua un modelo de clasificacion con multiples metricas.

    Args:
        modelo: Modelo entrenado
        X_test: Features de prueba
        y_test: Target de prueba
        nombre: Nombre del modelo
    Returns:
        Diccionario con metricas
    """
    y_pred = modelo.predict(X_test)

    metricas = {
        "modelo": nombre,
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred, average="weighted", zero_division=0), 4),
        "recall": round(recall_score(y_test, y_pred, average="weighted", zero_division=0), 4),
        "f1_score": round(f1_score(y_test, y_pred, average="weighted", zero_division=0), 4),
    }

    try:
        y_prob = modelo.predict_proba(X_test)[:, 1]
        metricas["roc_auc"] = round(roc_auc_score(y_test, y_prob), 4)
    except Exception:
        metricas["roc_auc"] = None

    print(f"\nModelo: {nombre}")
    print(f"  Accuracy:  {metricas['accuracy']}")
    print(f"  Precision: {metricas['precision']}")
    print(f"  Recall:    {metricas['recall']}")
    print(f"  F1 Score:  {metricas['f1_score']}")

    return metricas


def evaluar_regresion(modelo, X_test, y_test, nombre: str) -> dict:
    """
    Evalua un modelo de regresion con multiples metricas.

    Args:
        modelo: Modelo entrenado
        X_test: Features de prueba
        y_test: Target de prueba
        nombre: Nombre del modelo
    Returns:
        Diccionario con metricas
    """
    y_pred = modelo.predict(X_test)

    metricas = {
        "modelo": nombre,
        "mae": round(mean_absolute_error(y_test, y_pred), 4),
        "mse": round(mean_squared_error(y_test, y_pred), 4),
        "rmse": round(np.sqrt(mean_squared_error(y_test, y_pred)), 4),
        "r2": round(r2_score(y_test, y_pred), 4),
    }

    print(f"\nModelo: {nombre}")
    print(f"  MAE:  {metricas['mae']}")
    print(f"  RMSE: {metricas['rmse']}")
    print(f"  R2:   {metricas['r2']}")

    return metricas


def validacion_cruzada(modelo, X, y, cv: int = 5, tarea: str = "clasificacion") -> dict:
    """
    Realiza validacion cruzada robusta.

    Args:
        modelo: Modelo a evaluar
        X: Features
        y: Target
        cv: Numero de folds
        tarea: 'clasificacion' o 'regresion'
    Returns:
        Diccionario con resultados de CV
    """
    if tarea == "clasificacion":
        scoring = "f1_weighted"
        kfold = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
    else:
        scoring = "r2"
        kfold = KFold(n_splits=cv, shuffle=True, random_state=42)

    scores = cross_val_score(modelo, X, y, cv=kfold, scoring=scoring)

    resultado = {
        "scores": scores,
        "media": round(scores.mean(), 4),
        "std": round(scores.std(), 4),
    }

    print(f"  CV ({scoring}): {resultado['media']} +/- {resultado['std']}")
    return resultado


def comparar_modelos(resultados: list) -> pd.DataFrame:
    """
    Genera tabla comparativa de modelos.

    Args:
        resultados: Lista de diccionarios con metricas
    Returns:
        DataFrame comparativo ordenado por mejor metrica
    """
    df = pd.DataFrame(resultados)
    if "f1_score" in df.columns:
        df = df.sort_values("f1_score", ascending=False)
    elif "r2" in df.columns:
        df = df.sort_values("r2", ascending=False)
    df = df.reset_index(drop=True)
    print("\nComparacion de modelos:")
    print(df.to_string())
    return df


def graficar_matriz_confusion(modelo, X_test, y_test, nombre: str, save_path: str = None):
    """
    Grafica la matriz de confusion.

    Args:
        modelo: Modelo entrenado
        X_test: Features de prueba
        y_test: Target de prueba
        nombre: Nombre del modelo
        save_path: Ruta para guardar el grafico
    """
    y_pred = modelo.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title(f"Matriz de Confusion - {nombre}")
    plt.ylabel("Real")
    plt.xlabel("Predicho")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Grafico guardado en: {save_path}")
    plt.show()


def graficar_comparacion_modelos(df_comparacion: pd.DataFrame, metrica: str, save_path: str = None):
    """
    Grafica comparacion de modelos por metrica.

    Args:
        df_comparacion: DataFrame con metricas de modelos
        metrica: Nombre de la metrica a graficar
        save_path: Ruta para guardar el grafico
    """
    plt.figure(figsize=(10, 6))
    colores = ["#2ecc71" if i == 0 else "#3498db" for i in range(len(df_comparacion))]
    plt.barh(df_comparacion["modelo"], df_comparacion[metrica], color=colores)
    plt.xlabel(metrica.upper())
    plt.title(f"Comparacion de Modelos - {metrica.upper()}")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Grafico guardado en: {save_path}")
    plt.show()