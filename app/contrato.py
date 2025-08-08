import pandera as pa
from pandera.typing import Series
from pandera import Field


class schemaCRM(pa.DataFrameModel):
    """
    Define o esquema para a validação de dados de produtos com Pandera.

    Este esquema inclui campos básicos para produtos, incluindo um campo
    de e-mail validado por expressão regular.

    Attributes:
        id_produto (Series[int]): Identificador do produto, deve estar entre
            1 e 20.
        nome (Series[str]): Nome do produto.
        quantidade (Series[int]): Quantidade disponível do produto,
            deve estar entre 20 e 200.
        preco (Series[float]): Preço do produto, deve estar entre
            5.0 e 120.0.
        categoria (Series[str]): Categoria do produto.
        email (Series[str]): E-mail associado ao produto, deve seguir o
            formato padrão de e-mails.
    """

    id_produto: Series[int] = Field(ge=21, le=31)
    nome: Series[str]
    quantidade: Series[int] = Field(ge=20, le=200)
    preco: Series[float] = Field(ge=5.0, le=120.0)
    categoria: Series[str]

    class Config:
        coerce = True
        strict = False
        ordered = False
        add_missing_columns = False
        unique_column_names = False


class schemaCRMnew(pa.DataFrameModel):
    """
    Contrato de dados para colunas calculadas no processo de
    transformação do CRM.

    Attributes:
        valor_total (float): Valor total do produto, calculado como
            quantidade * preço. Deve ser maior ou igual a zero.
        cat_normalizada (str): Nome da categoria do produto
            em letras minúsculas.
        disponibilidade (bool): Indica se o produto está disponível
            em estoque (True) ou não (False).
    """

    valor_total: Series[float] = pa.Field(ge=0)
    cat_normalizada: Series[str]
    disponibilidade: Series[bool]
