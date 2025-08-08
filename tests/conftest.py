import pandera as pa
import pytest


def pytest_sessionstart(session):
    """Executa antes de qualquer teste ser importado."""
    import app.etl as etl

    empty_schema = pa.DataFrameSchema({})

    # Remove todos os decorators originais
    transformar_sem_decorators = etl.transformar.__wrapped__.__wrapped__
    read_table_sem_decorator = etl.read_table.__wrapped__

    # Reaplica com schemas vazios
    etl.read_table = pa.check_output(empty_schema, lazy=True)(read_table_sem_decorator)
    etl.transformar = pa.check_output(empty_schema, lazy=True)(
        pa.check_input(empty_schema, lazy=True)(transformar_sem_decorators)
    )


@pytest.fixture(autouse=True)
def _no_pandera():
    """Mantém compatibilidade, mas aqui não precisa fazer nada."""
    pass
