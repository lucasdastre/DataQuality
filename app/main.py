from pydantic import BaseModel, field_validator, ValidationError


class Operacao(BaseModel):
    x: int
    y: int

    @field_validator("x", "y")
    def valores_devem_ser_positivos(cls, valor, info):
        if valor < 0:
            raise ValueError(f"O campo '{info.field_name}' não negativo.")
        return valor


def soma(operacao: Operacao):
    return operacao.x + operacao.y


def funcao_ola():
    return "Olá, mundo!"


if __name__ == "__main__":
    funcao_ola()

    # ✅ Teste com valores válidos
    try:
        dados_validos = Operacao(x=5, y=6)
        print("Resultado da soma:", soma(dados_validos))
    except ValidationError as e:
        print("Erro de validação (válido):", e)

    # ❌ Teste com valor negativo
    try:
        dados_invalidos = Operacao(x=5, y=-6)
        print("Resultado da soma:", soma(dados_invalidos))
    except ValidationError as e:
        print("Erro de validação (inválido):")
        print(e)
