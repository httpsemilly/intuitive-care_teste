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