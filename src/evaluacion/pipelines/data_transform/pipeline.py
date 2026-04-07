"""Pipeline de transformación de datos."""
from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    integrar_datasets,
    normalizar_columnas,
    codificar_categoricas,
    crear_features,
    agregar_por_paciente,
)


def create_pipeline(**kwargs) -> Pipeline:
    """Crea el pipeline de transformación de datos."""
    return pipeline([
        node(
            func=integrar_datasets,
            inputs=[
                "consultas_cleaned",
                "examenes_cleaned",
                "medicamentos_cleaned",
                "pacientes_cleaned",
            ],
            outputs="dataset_merged",
            name="integrar_datasets",
        ),
        node(
            func=crear_features,
            inputs="dataset_merged",
            outputs="dataset_features",
            name="crear_features",
        ),
        node(
            func=normalizar_columnas,
            inputs=["dataset_features", "params:columnas_numericas"],
            outputs="dataset_normalizado",
            name="normalizar_columnas",
        ),
        node(
            func=codificar_categoricas,
            inputs="dataset_normalizado",
            outputs="dataset_codificado",
            name="codificar_categoricas",
        ),
        node(
            func=agregar_por_paciente,
            inputs="dataset_codificado",
            outputs="dataset_integrado",
            name="agregar_por_paciente",
        ),
    ])