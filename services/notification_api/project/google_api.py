import os, requests

def google_matrix_api_request(origem, destino):
    # Faz uma requisição para a API do Google Maps Matrix
    # Retorna a resposta da requisição em formato JSON
    # Registra a chave de API em uma variável de ambiente. Ela está no arquivo .env
    key = os.getenv('YOUR_API_KEY')
    if not key:
        raise ValueError('Required API key not found in environment variables.')
    
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={}&destinations={}&key={}'
    
    try:
        response = requests.get(url.format(origem, destino, key))
        response.raise_for_status()  # Se a requisição falhar, uma exceção será lançada
    except requests.exceptions.RequestException as e:
        print(f"Um erro ocorreu com a requisição para a API do Google: {e}")
        return None

    return response.json()