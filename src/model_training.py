"""
Definicion y entrenamiento de modelos supervisados y no supervisados.
Modulo de entrenamiento para la Evaluacion Parcial N°2.
"""
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def entrenar_modelos_clasificacion(X_train, y_train: int = 42) -> dict:
    """
    Entrena multiples modelos de clasificacion.

    Args:
        X_train: Features de entrenamiento
        y_train: Target de entrenamiento
        random_state: Semilla para reproducibilidad
    Returns:
        Diccionario con modelos entrenados
    """
    modelos = {
        "Logistic Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(random_state=42, max_iter=1000))
        ]),
        "Decision Tree": Pipeline([
            ("scaler", StandardScaler()),
            ("model", DecisionTreeClassifier(random_state=42, max_depth=5))
        ]),
        "Random Forest": Pipeline([
            ("scaler", StandardScaler()),
            ("model", RandomForestClassifier(random_state=42, n_estimators=100))
        ]),
        "Gradient Boosting": Pipeline([
            ("scaler", StandardScaler()),
            ("model", GradientBoostingClassifier(random_state=42, n_estimators=100))
        ]),
        "KNN": Pipeline([
            ("scaler", StandardScaler()),
            ("model", KNeighborsClassifier(n_neighbors=5))
        ]),
        "SVM": Pipeline([
            ("scaler", StandardScaler()),
            ("model", SVC(random_state=42, probability=True))
        ]),
    }

    modelos_entrenados = {}
    for nombre, modelo in modelos.items():
        print(f"Entrenando {nombre}...")
        modelo.fit(X_train, y_train)
        modelos_entrenados[nombre] = modelo
        print(f"  {nombre} entrenado correctamente")

    return modelos_entrenados


def entrenar_modelos_regresion(X_train, y_train) -> dict:
    """
    Entrena multiples modelos de regresion.

    Args:
        X_train: Features de entrenamiento
        y_train: Target de entrenamiento
    Returns:
        Diccionario con modelos entrenados
    """
    modelos = {
        "Linear Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LinearRegression())
        ]),
        "Ridge Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("model", Ridge(alpha=1.0))
        ]),
        "Decision Tree Regressor": Pipeline([
            ("scaler", StandardScaler()),
            ("model", DecisionTreeRegressor(random_state=42, max_depth=5))
        ]),
        "Random Forest Regressor": Pipeline([
            ("scaler", StandardScaler()),
            ("model", RandomForestRegressor(random_state=42, n_estimators=100))
        ]),
    }

    modelos_entrenados = {}
    for nombre, modelo in modelos.items():
        print(f"Entrenando {nombre}...")
        modelo.fit(X_train, y_train)
        modelos_entrenados[nombre] = modelo
        print(f"  {nombre} entrenado correctamente")

    return modelos_entrenados


def entrenar_clustering(X, n_clusters: int = 3) -> dict:
    """
    Entrena modelos de clustering no supervisado.

    Args:
        X: Features
        n_clusters: Numero de clusters para KMeans
    Returns:
        Diccionario con modelos entrenados
    """
    modelos = {
        "KMeans": KMeans(n_clusters=n_clusters, random_state=42, n_init=10),
        "DBSCAN": DBSCAN(eps=0.5, min_samples=5),
    }

    modelos_entrenados = {}
    for nombre, modelo in modelos.items():
        print(f"Entrenando {nombre}...")
        modelo.fit(X)
        modelos_entrenados[nombre] = modelo
        print(f"  {nombre} entrenado correctamente")

    return modelos_entrenados


def aplicar_pca(X, n_components: int = 2):
    """
    Aplica reduccion de dimensionalidad con PCA.

    Args:
        X: Features
        n_components: Numero de componentes
    Returns:
        Tupla (X_reducido, pca)
    """
    pca = PCA(n_components=n_components, random_state=42)
    X_reducido = pca.fit_transform(X)
    varianza = pca.explained_variance_ratio_.sum() * 100
    print(f"PCA: {n_components} componentes explican {varianza:.2f}% de la varianza")
    return X_reducido, pca


def guardar_modelo(modelo, filepath: str) -> None:
    """
    Serializa y guarda un modelo entrenado.

    Args:
        modelo: Modelo entrenado
        filepath: Ruta donde guardar el modelo
    """
    joblib.dump(modelo, filepath)
    print(f"Modelo guardado en: {filepath}")


def cargar_modelo(filepath: str):
    """
    Carga un modelo serializado.

    Args:
        filepath: Ruta del modelo
    Returns:
        Modelo cargado
    """
    modelo = joblib.load(filepath)
    print(f"Modelo cargado desde: {filepath}")
    return modelo