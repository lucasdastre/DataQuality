import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
import pandera as pa
from app import etl


# ==== Fixture de dados fake ====
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "quantidade": [10, 0, 5],
        "preco": [2.5, 3.0, 4.0],
        "categoria": ["Eletrônicos", "Livros", "Eletrodomésticos"]
    })


# ==== Teste da função transformar ====
def test_transformar(sample_df):
    df_result = etl.transformar(sample_df.copy())

    assert "valor_total" in df_result.columns
    assert "cat_normalizada" in df_result.columns
    assert "disponibilidade" in df_result.columns

    assert df_result.loc[0, "valor_total"] == 25.0
    assert df_result.loc[1, "valor_total"] == 0.0
    assert df_result.loc[0, "cat_normalizada"] == "eletrônicos"
    assert df_result.loc[0, "disponibilidade"]
    assert not df_result.loc[1, "disponibilidade"]


# ==== Teste da função read_table ====
def test_read_table():
    mock_engine = MagicMock()
    fake_df = pd.DataFrame({"a": [1], "b": [2]})

    with patch("app.etl.conections", return_value=mock_engine), \
         patch("pandas.read_sql", return_value=fake_df):
        df = etl.read_table("fake_table")

    assert isinstance(df, pd.DataFrame)
    assert df.equals(fake_df)


# ==== Teste da função infer_schema ====
def test_infer_schema(tmp_path):
    schema = pa.DataFrameSchema({"col": pa.Column(int)})
    file_path = tmp_path / "schema.py"

    etl.infer_schema(file_path, schema)

    content = file_path.read_text()
    assert "DataFrameSchema" in content
    assert "col" in content


# ==== Teste da função conections ====
def test_conections(monkeypatch):
    monkeypatch.setenv("PG_HOST", "localhost")
    monkeypatch.setenv("PG_DATABASE", "testdb")
    monkeypatch.setenv("PG_USER", "user")
    monkeypatch.setenv("PG_PASSWORD", "pass")
    monkeypatch.setenv("PG_PORT", "5432")

    engine = etl.conections()
    assert engine is not None
    assert "postgresql+psycopg2" in str(engine.url)
