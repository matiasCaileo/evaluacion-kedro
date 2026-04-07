"""Registro de pipelines del proyecto."""
from evaluacion.pipelines import (
    data_ingestion,
    data_cleaning,
    data_transform,
    data_validation,
)


def register_pipelines():
    """Registra todos los pipelines del proyecto."""
    return {
        "ingestion": data_ingestion.create_pipeline(),
        "cleaning": data_cleaning.create_pipeline(),
        "transform": data_transform.create_pipeline(),
        "validation": data_validation.create_pipeline(),
        "__default__": (
            data_ingestion.create_pipeline()
            + data_cleaning.create_pipeline()
            + data_transform.create_pipeline()
            + data_validation.create_pipeline()
        ),
    }