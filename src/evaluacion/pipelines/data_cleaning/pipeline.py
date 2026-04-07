"""Pipeline de limpieza de datos."""
from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    eliminar_duplicados,
    estandarizar_fechas,
    limpiar_strings,
    tratar_nulos,
    tratar_outliers,
    convertir_tipos,
)


def create_pipeline(**kwargs) -> Pipeline:
    """Crea el pipeline de limpieza de datos."""
    return pipeline([
        # Limpieza de consultas
        node(func=eliminar_duplicados, inputs="consultas_raw", outputs="consultas_sin_dups", name="dedup_consultas"),
        node(func=convertir_tipos, inputs="consultas_sin_dups", outputs="consultas_tipos_ok", name="tipos_consultas"),
        node(func=estandarizar_fechas, inputs=["consultas_tipos_ok", "params:columnas_fecha_consultas"], outputs="consultas_fechas_ok", name="fechas_consultas"),
        node(func=limpiar_strings, inputs=["consultas_fechas_ok", "params:columnas_string_consultas"], outputs="consultas_strings_ok", name="strings_consultas"),
        node(func=tratar_nulos, inputs=["consultas_strings_ok", "params:estrategia_nulos"], outputs="consultas_nulos_ok", name="nulos_consultas"),
        node(func=tratar_outliers, inputs=["consultas_nulos_ok", "params:umbral_outliers"], outputs="consultas_cleaned", name="outliers_consultas"),

        # Limpieza de examenes
        node(func=eliminar_duplicados, inputs="examenes_raw", outputs="examenes_sin_dups", name="dedup_examenes"),
        node(func=convertir_tipos, inputs="examenes_sin_dups", outputs="examenes_tipos_ok", name="tipos_examenes"),
        node(func=estandarizar_fechas, inputs=["examenes_tipos_ok", "params:columnas_fecha_examenes"], outputs="examenes_fechas_ok", name="fechas_examenes"),
        node(func=tratar_nulos, inputs=["examenes_fechas_ok", "params:estrategia_nulos"], outputs="examenes_nulos_ok", name="nulos_examenes"),
        node(func=tratar_outliers, inputs=["examenes_nulos_ok", "params:umbral_outliers"], outputs="examenes_cleaned", name="outliers_examenes"),

        # Limpieza de medicamentos
        node(func=eliminar_duplicados, inputs="medicamentos_raw", outputs="medicamentos_sin_dups", name="dedup_medicamentos"),
        node(func=convertir_tipos, inputs="medicamentos_sin_dups", outputs="medicamentos_tipos_ok", name="tipos_medicamentos"),
        node(func=tratar_nulos, inputs=["medicamentos_tipos_ok", "params:estrategia_nulos"], outputs="medicamentos_nulos_ok", name="nulos_medicamentos"),
        node(func=tratar_outliers, inputs=["medicamentos_nulos_ok", "params:umbral_outliers"], outputs="medicamentos_cleaned", name="outliers_medicamentos"),

        # Limpieza de pacientes
        node(func=eliminar_duplicados, inputs="pacientes_raw", outputs="pacientes_sin_dups", name="dedup_pacientes"),
        node(func=convertir_tipos, inputs="pacientes_sin_dups", outputs="pacientes_tipos_ok", name="tipos_pacientes"),
        node(func=estandarizar_fechas, inputs=["pacientes_tipos_ok", "params:columnas_fecha_pacientes"], outputs="pacientes_fechas_ok", name="fechas_pacientes"),
        node(func=limpiar_strings, inputs=["pacientes_fechas_ok", "params:columnas_string_pacientes"], outputs="pacientes_strings_ok", name="strings_pacientes"),
        node(func=tratar_nulos, inputs=["pacientes_strings_ok", "params:estrategia_nulos"], outputs="pacientes_nulos_ok", name="nulos_pacientes"),
        node(func=tratar_outliers, inputs=["pacientes_nulos_ok", "params:umbral_outliers"], outputs="pacientes_cleaned", name="outliers_pacientes"),
    ])