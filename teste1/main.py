import requests

def download_file(url: str):
    """Baixa arquivo ZIP da URL e retorna o conteúdo em bytes"""

    print(f"Baixando arquivo de {url}...")

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