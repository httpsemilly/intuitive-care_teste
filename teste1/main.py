import requests
import zipfile
import pandas as pd
from io import BytesIO

def download_file(url: str):
    """Baixa arquivo ZIP da URL e retorna o conteúdo em bytes"""

    print(f"Baixando arquivo de {url}")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        print("Download do arquivo concluído!")

        return response.content
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP ao baixar arquivo: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao baixar arquivo: {e}")
        return None
    
def extract_zip(zip_content: bytes):
    """Extrai o conteúdo do arquivo ZIP que foi baixado e retorna um DataFrame"""

    zip_file = BytesIO(zip_content)

    with zipfile.ZipFile(zip_file, mode='r') as zip:
        files = zip.namelist()

        for file in files:
            if file.endswith('.csv'):
                csv_filename = file

        csv_content = zip.read(csv_filename)
        
        csv_buffer = BytesIO(csv_content)
        df = pd.read_csv(csv_buffer, delimiter=';', decimal=',', encoding='utf-8')

        return df
    
def process_statements(df, quarter: str, year: int):
    """Filtra e processa demonstrações contábeis, focando em despesas com eventos/sinistros. Retorna DataFrame"""

    pattern = r'^DESPESAS\s+COM\s+EVENTOS\s*/\s*SINISTROS'
    filtered_df = df[df['DESCRICAO'].str.contains(pattern, case=False, na=False, regex=True)]
    
    selected_df = filtered_df[['REG_ANS', 'VL_SALDO_FINAL']]

    grouped_df = selected_df.groupby('REG_ANS').sum().reset_index()
    grouped_df.rename(columns={'VL_SALDO_FINAL': 'ValorDespesas'}, inplace=True)
    grouped_df.insert(1, 'Trimestre', quarter)
    grouped_df.insert(2, 'Ano', year)

    return grouped_df

def download_registry_data():
    url = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"

    print(f"Baixando arquivo de cadastro de operadoras de {url}")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        print("Download do arquivo concluído!")
        
        csv_file = BytesIO(response.content)

        registry_df = pd.read_csv(csv_file, delimiter=';', decimal=',', encoding='utf-8')
        registry_df.columns = registry_df.columns.str.upper()
        registry_df = registry_df[['CNPJ', 'REGISTRO_OPERADORA', 'RAZAO_SOCIAL']]
        registry_df = registry_df.rename(columns={'REGISTRO_OPERADORA': 'REG_ANS', 'RAZAO_SOCIAL': 'RazaoSocial'})
        registry_df['CNPJ'] = registry_df['CNPJ'].astype(str).str.zfill(14)

        return registry_df
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP ao baixar arquivo: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao baixar arquivo: {e}")
        return None
