# 🎬 GFLIX Data Processing — Movies & Ratings

Projeto de processamento local de arquivos CSV (movies + customers_rating), geração de arquivo **Parquet** e upload para o **Amazon S3**.

O pipeline foi desenvolvido em Python e pode ser executado localmente por qualquer pessoa apenas configurando variáveis de ambiente.

---

## ✅ Funcionalidades

* Leitura de CSV de entrada (`movies.csv` e `customers_rating.csv`)
* Tratamento e limpeza das tabelas
* Normalização dos nomes das colunas
* Conversão das datas e tipos
* Junção entre as tabelas via `movie_id`
* Exportação local em formato **Parquet**
* Upload automático para o S3 usando `boto3`

---

## 📁 Estrutura do Projeto

```
📦 gflix-data-processing
 ┣ 📄 app.py
 ┣ 📄 requirements.txt
 ┗ 📄 README.md
```

---

## ⚙️ Pré-requisitos

* Python 3.9+
* pip
* Conta AWS
* S3 Bucket criado (ex: `work-final-five-gflix`)
* Access Key & Secret Key válidas (para uso local)

---

## 🔧 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/gmln-user/aws-final-project
cd aws-final-project
```

2. Crie um ambiente virtual:

```bash
python -m venv .venv
```

3. Ative o ambiente:

* Windows:

```bash
.\.venv\Scripts\activate
```

* Linux/Mac:

```bash
source .venv/bin/activate
```

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuração do `.env`

Crie um arquivo chamado **.env** na raiz do projeto e configure as variáveis:

```
AWS_ACCESS_KEY=SEU_ACCESS_KEY
AWS_SECRET_KEY=SEU_SECRET_KEY
AWS_REGION=us-east-1

BUCKET_NAME=work-final-five-gflix
OUTPUT_KEY=processed/final_data.parquet

MOVIES_PATH=movies.csv
CUSTOMERS_PATH=customers_rating.csv
```

> Você pode usar o arquivo `.env.example` como base.

---

## ▶️ Execução do Pipeline

Após configurar as variáveis:

```bash
python app.py
```

O fluxo será:

1. Processamento dos arquivos CSV
2. Join entre customers × movies
3. Geração do arquivo local:

```
final_data.parquet
```

4. Upload automático ao S3:

```
s3://work-final-five-gflix/processed/final_data.parquet
```

---

## 🧪 Teste Rápido

Após rodar:

```bash
aws s3 ls s3://work-final-five-gflix/processed/
```

Você deverá ver:

```
2025-11-10  22:01:12   45283423 final_data.parquet
```

---

## ⚠️ Observações Importantes

* Não compartilhe credenciais do AWS.
* Para ambientes de produção, use IAM roles (sem access keys).
* Para arquivos muito grandes, recomenda-se o uso de AWS Lambda + S3 streaming ou AWS Glue.

---

## 🧹 Limpeza

Para sair do ambiente virtual:

```bash
deactivate
```

---

## 📜 Licença

MIT License.

---

Se quiser, eu posso melhorar o README com badges, imagem do workflow ou diagramas da arquitetura.


