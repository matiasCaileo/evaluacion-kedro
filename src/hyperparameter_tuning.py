"""
Funciones para optimizacion de hiperparametros.
Modulo de tuning para la Evaluacion Parcial N°2.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def grid_search_random_forest(X_train, y_train, cv: int = 5) -> dict:
    """
    Optimiza hiperparametros de Random Forest con GridSearchCV.

    Args:
        X_train: Features de entrenamiento
        y_train: Target de entrenamiento
        cv: Numero de folds
    Returns:
        Diccionario con mejor modelo y resultados
    """
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", RandomForestClassifier(random_state=42))
    ])

    param_grid = {
        "model__n_estimators": [50, 100, 200],
        "model__max_depth": [3, 5, 10, None],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 4],
    }

    kfold = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)

    print("Ejecutando GridSearchCV para Random Forest...")
    grid_search = GridSearchCV(
        pipeline,
        param_grid,
        cv=kfold,
        scoring="f1_weighted",
        n_jobs=-1,
        verbose=1,
    )
    grid_search.fit(X_train, y_train)

    print(f"Mejores parametros: {grid_search.best_params_}")
    print(f"Mejor F1 CV: {grid_search.best_score_:.4f}")

    return {
        "mejor_modelo": grid_search.best_estimator_,
        "mejores_params": grid_search.best_params_,
        "mejor_score": grid_search.best_score_,
        "resultados_cv": pd.DataFrame(grid_search.cv_results_),
    }


def randomized_search_gradient_boosting(X_train, y_train, cv: int = 5, n_iter: int = 20) -> dict:
    """
    Optimiza hiperparametros de Gradient Boosting con RandomizedSearchCV.

    Args:
        X_train: Features de entrenamiento
        y_train: Target de entrenamiento
        cv: Numero de folds
        n_iter: Numero de iteraciones
    Returns:
        Diccionario con mejor modelo y resultados
    """
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", GradientBoostingClassifier(random_state=42))
    ])

    param_dist = {
        "model__n_estimators": [50, 100, 200, 300],
        "model__max_depth": [3, 4, 5, 6],
        "model__learning_rate": [0.01, 0.05, 0.1, 0.2],
        "model__subsample": [0.6, 0.8, 1.0],
        "model__min_samples_split": [2, 5, 10],
    }

    kfold = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)

    print("Ejecutando RandomizedSearchCV para Gradient Boosting...")
    random_search = RandomizedSearchCV(
        pipeline,
        param_dist,
        n_iter=n_iter,
        cv=kfold,
        scoring="f1_weighted",
        n_jobs=-1,
        random_state=42,
        verbose=1,
    )
    random_search.fit(X_train, y_train)

    print(f"Mejores parametros: {random_search.best_params_}")
    print(f"Mejor F1 CV: {random_search.best_score_:.4f}")

    return {
        "mejor_modelo": random_search.best_estimator_,
        "mejores_params": random_search.best_params_,
        "mejor_score": random_search.best_score_,
        "resultados_cv": pd.DataFrame(random_search.cv_results_),
    }


def comparar_antes_despues_tuning(
    modelo_base,
    modelo_optimizado,
    X_test,
    y_test,
    nombre: str,
) -> pd.DataFrame:
    """
    Compara el rendimiento antes y despues del tuning.

    Args:
        modelo_base: Modelo sin optimizar
        modelo_optimizado: Modelo optimizado
        X_test: Features de prueba
        y_test: Target de prueba
        nombre: Nombre del modelo
    Returns:
        DataFrame con comparacion
    """
    from sklearn.metrics import f1_score, accuracy_score

    y_pred_base = modelo_base.predict(X_test)
    y_pred_opt = modelo_optimizado.predict(X_test)

    comparacion = pd.DataFrame({
        "version": ["Base", "Optimizado"],
        "accuracy": [
            round(accuracy_score(y_test, y_pred_base), 4),
            round(accuracy_score(y_test, y_pred_opt), 4),
        ],
        "f1_score": [
            round(f1_score(y_test, y_pred_base, average="weighted", zero_division=0), 4),
            round(f1_score(y_test, y_pred_opt, average="weighted", zero_division=0), 4),
        ],
    })

    print(f"\nComparacion antes/despues de tuning - {nombre}:")
    print(comparacion.to_string())
    return comparacion


def graficar_impacto_hiperparametros(resultados_cv: pd.DataFrame, param: str, save_path: str = None):
    """
    Grafica el impacto de un hiperparametro en el rendimiento.

    Args:
        resultados_cv: DataFrame con resultados de GridSearchCV
        param: Nombre del parametro a graficar
        save_path: Ruta para guardar el grafico
    """
    import matplotlib.pyplot as plt

    col = f"param_{param}"
    if col not in resultados_cv.columns:
        print(f"Parametro {param} no encontrado en resultados")
        return

    df_plot = resultados_cv.groupby(col)["mean_test_score"].mean().reset_index()

    plt.figure(figsize=(8, 5))
    plt.plot(df_plot[col].astype(str), df_plot["mean_test_score"], marker="o", color="#2ecc71")
    plt.title(f"Impacto de {param} en F1 Score")
    plt.xlabel(param)
    plt.ylabel("F1 Score (CV)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Grafico guardado en: {save_path}")
    plt.show()