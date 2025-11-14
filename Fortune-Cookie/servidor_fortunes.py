import socket
import threading
import random

HOST = '127.0.0.1'
PORT = 5000

# Base inicial de frases
fortunes = [
    "Acredite nos seus sonhos e vá atrás deles!",
    "O sucesso nasce do querer.",
    "Grandes realizações começam com pequenos passos.",
    "Seja a mudança que você quer ver no mundo.",
]

lock = threading.Lock()

def handle_client(conn, addr):
    print(f"[+] Conexão estabelecida com {addr}")
    with conn:
        while True:
            data = conn.recv(1024).decode('utf-8').strip()
            if not data:
                break

            print(f"[{addr}] Comando recebido: {data}")
            response = process_command(data)
            conn.sendall(response.encode('utf-8'))
    print(f"[-] Conexão encerrada com {addr}")

def process_command(command):
    global fortunes
    parts = command.split(' ', 2)
    cmd = parts[0].upper()

    with lock:
        if cmd == "GET-FORTUNE":
            return random.choice(fortunes) if fortunes else "Nenhuma frase armazenada."

        elif cmd == "ADD-FORTUNE":
            if len(parts) < 2:
                return "Erro: use ADD-FORTUNE <nova frase>"
            fortunes.append(parts[1])
            return "Frase adicionada com sucesso."

        elif cmd == "UPD-FORTUNE":
            if len(parts) < 3:
                return "Erro: use UPD-FORTUNE <pos> <nova frase>"
            try:
                pos = int(parts[1])
                if 0 <= pos < len(fortunes):
                    fortunes[pos] = parts[2]
                    return "Frase atualizada com sucesso."
                else:
                    return "Erro: posição inválida."
            except ValueError:
                return "Erro: posição deve ser um número inteiro."

        elif cmd == "LST-FORTUNE":
            return "\n".join(f"{i}: {f}" for i, f in enumerate(fortunes))

        else:
            return "Comando desconhecido."

def main():
    print("[*] Servidor de Fortunes iniciado...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[*] Aguardando conexões em {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    main()
