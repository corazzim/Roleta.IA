import requests
import time

API_URL = "https://casino.betfair.com/api/tables-details"
GAME_TABLE_ID_DESEJADO = "103910"

# Armazena o último número conhecido
ultimo_estado = None

# Substitua "SUA_API_KEY" pela sua chave API real
API_KEY = "SUA_API_KEY"

def buscar_numero_unico():
    # Adiciona os cabeçalhos necessários
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Authorization": f"Bearer {API_KEY}"  # Inclui o cabeçalho de autenticação
    }

    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        dados = response.json()

        # Se a estrutura real for "tables", troque para: dados.get("tables", [])
        game_tables = dados.get("gameTables", [])
        
        for table in game_tables:
            if str(table.get("gameTableId")) == GAME_TABLE_ID_DESEJADO:
                # lastNumbers pode ser uma lista de strings
                last_numbers_raw = table.get("lastNumbers", [])
                if last_numbers_raw:
                    # Agora buscamos o primeiro elemento (à esquerda),
                    # pois é ele que representa o número realmente novo.
                    return int(last_numbers_raw[0])
                else:
                    return None
        return None  # Não encontrou a mesa
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None

def main():
    global ultimo_estado

    while True:
        numero_atual = buscar_numero_unico()
        
        # Se encontrou um número e for diferente do último conhecido, imprime
        if numero_atual is not None and numero_atual != ultimo_estado:
            print(f"Número atualizado: {numero_atual}")
            ultimo_estado = numero_atual
        
        # Intervalo de 1 segundo antes de verificar novamente
        time.sleep(1)

if __name__ == "__main__":
    main()
