"""Pipeline de ingesta y exploración de datos."""
from kedro.pipeline import Pipeline, node, pipeline
from .nodes import explorar_dataset, generar_reporte_diagnostico


def create_pipeline(**kwargs) -> Pipeline:
    """Crea el pipeline de ingesta de datos."""
    return pipeline([
        node(
            func=explorar_dataset,
            inputs=["consultas_raw", "params:consultas"],
            outputs="consultas_explored",
            name="explorar_consultas",
        ),
        node(
            func=explorar_dataset,
            inputs=["examenes_raw", "params:examenes"],
            outputs="examenes_explored",
            name="explorar_examenes",
        ),
        node(
            func=explorar_dataset,
            inputs=["medicamentos_raw", "params:medicamentos"],
            outputs="medicamentos_explored",
            name="explorar_medicamentos",
        ),
        node(
            func=explorar_dataset,
            inputs=["pacientes_raw", "params:pacientes"],
            outputs="pacientes_explored",
            name="explorar_pacientes",
        ),
        node(
            func=generar_reporte_diagnostico,
            inputs=[
                "consultas_explored",
                "examenes_explored",
                "medicamentos_explored",
                "pacientes_explored",
            ],
            outputs="reporte_diagnostico",
            name="generar_reporte_diagnostico",
        ),
    ])