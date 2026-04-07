"""Pipeline de validación de datos."""
from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    validar_integridad,
    comparar_antes_despues,
    generar_reporte_final,
)


def create_pipeline(**kwargs) -> Pipeline:
    """Crea el pipeline de validación de datos."""
    return pipeline([
        node(
            func=comparar_antes_despues,
            inputs=["consultas_raw", "consultas_cleaned", "params:consultas"],
            outputs="val_consultas",
            name="validar_consultas",
        ),
        node(
            func=comparar_antes_despues,
            inputs=["examenes_raw", "examenes_cleaned", "params:examenes"],
            outputs="val_examenes",
            name="validar_examenes",
        ),
        node(
            func=comparar_antes_despues,
            inputs=["medicamentos_raw", "medicamentos_cleaned", "params:medicamentos"],
            outputs="val_medicamentos",
            name="validar_medicamentos",
        ),
        node(
            func=comparar_antes_despues,
            inputs=["pacientes_raw", "pacientes_cleaned", "params:pacientes"],
            outputs="val_pacientes",
            name="validar_pacientes",
        ),
        node(
            func=validar_integridad,
            inputs="dataset_integrado",
            outputs="val_integrado",
            name="validar_integrado",
        ),
        node(
            func=generar_reporte_final,
            inputs=[
                "val_consultas",
                "val_examenes",
                "val_medicamentos",
                "val_pacientes",
                "val_integrado",
            ],
            outputs="reporte_validacion",
            name="generar_reporte_final",
        ),
    ])