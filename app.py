import pandas as pd
import boto3
import os
from io import StringIO
from dotenv import load_dotenv

# ---------------------------
# CONFIGURAÇÕES
# ---------------------------
load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

BUCKET_NAME = os.getenv('BUCKET_NAME')

MOVIES_PATH = os.getenv('MOVIES_PATH')
CUSTOMERS_PATH = os.getenv('CUSTOMERS_PATH')

OUTPUT_KEY = os.getenv('OUTPUT_KEY')


# ---------------------------
# FUNÇÃO PARA LER CSV DO S3
# ---------------------------
def read_csv_from_s3(bucket, key):
    print(f"Lendo arquivo S3: s3://{bucket}/{key}")

    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )

    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        csv_data = obj['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_data), sep=';')
        print("✅ Leitura concluída")
        return df
    except Exception as e:
        print(f"❌ Erro ao ler arquivo do S3: {key}")
        raise e


# ---------------------------
# PROCESSAMENTO MOVIES
# ---------------------------
def process_movies(df_movies):
    print("Processando movies...")

    df_movies.columns = ["movie_id", "raw"]
    df_movies["raw"] = df_movies["raw"].str.strip()
    df_movies["raw"] = df_movies["raw"].str.replace('[()]', '', regex=True)

    df_movies[["title", "year"]] = df_movies["raw"].str.split(",", n=1, expand=True)
    df_movies["year"] = df_movies["year"].str.strip().astype(int)

    df_movies = df_movies.drop(columns=["raw"])
    return df_movies


# ---------------------------
# PROCESSAMENTO CUSTOMERS
# ---------------------------
def process_customers(df_customer):
    print("Processando customers...")

    df_customer.columns = ["customer_id", "rating", "rating_date", "movie_id"]

    df_customer["rating"] = df_customer["rating"].astype(float)
    df_customer["movie_id"] = df_customer["movie_id"].astype(int)
    df_customer["customer_id"] = df_customer["customer_id"].astype(int)
    df_customer["rating_date"] = pd.to_datetime(df_customer["rating_date"], errors="coerce")

    df_customer = df_customer.dropna(subset=["movie_id", "rating"])

    return df_customer


# ---------------------------
# UPLOAD PARA S3
# ---------------------------
def upload_to_s3(local_path, bucket, key):
    print(f"Enviando para S3: s3://{bucket}/{key}...")

    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )

    s3.upload_file(local_path, bucket, key)
    print("✅ Upload concluído com sucesso!")


# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":

    # 1. Ler CSVs do S3
    df_movies_raw = read_csv_from_s3(BUCKET_NAME, MOVIES_PATH)
    df_customers_raw = read_csv_from_s3(BUCKET_NAME, CUSTOMERS_PATH)

    # 2. Processar
    df_movies = process_movies(df_movies_raw)
    df_customers = process_customers(df_customers_raw)

    # 3. Join
    print("Fazendo join...")
    df_final = df_customers.merge(df_movies, on="movie_id", how="inner")

    print(df_final.head())

    # 4. Salvar local parquet
    output_file = "final_data.parquet"
    df_final.to_parquet(output_file, index=False)

    # 5. Upload parquet para Processed
    upload_to_s3(output_file, BUCKET_NAME, OUTPUT_KEY)

    print("✅ Processo completo!")
