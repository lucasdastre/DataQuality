import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandera.pandas as pa
from contrato import schemaCRM , shcemaCRMnew

load_dotenv()

def conections():
    try:
        host = os.getenv('PG_HOST')
        database = os.getenv('PG_DATABASE')
        user = os.getenv('PG_USER')
        pw = os.getenv('PG_PASSWORD')
        port = os.getenv('PG_PORT')

        return create_engine(f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{database}")

    except Exception as e:
        print('Conexão não estabelecida')
        print(e)

@pa.check_output(schemaCRM , lazy= True)
def read_table(table_name: str) -> pd.DataFrame:
    con = conections()
    with con.connect() as conn:
        df =  pd.read_sql(
            f'select * from {table_name}' , conn
        )
    return df

def infer_schema(file : str , schema: pa.DataFrameSchema):
    with open(file, 'w' , encoding= 'utf-8') as f:
        f.write("import pandera as pa\n")
        f.write("from pandera import Column, Check, DataFrameSchema\n\n")
        f.write(schema.to_script())

@pa.check_output(schemaCRM , lazy= True)
@pa.check_input(shcemaCRMnew , lazy= True)
def transformar(df: pd.DataFrame) -> pd.DataFrame:

    df['valor_total'] = df['quantidade'] * df['preco']
    df['cat_normalizada'] = df['categoria'].str.lower()
    df['disponibilidade'] = df['quantidade'] > 0

    return df


def main():

    dataframe = read_table('produtos_bronze')
    # infer = pa.infer_schema(dataframe)
    # infer_schema('app/schema.py' , infer)
    new_df = transformar(dataframe)
    print(new_df)


if __name__ == "__main__":
    main()
