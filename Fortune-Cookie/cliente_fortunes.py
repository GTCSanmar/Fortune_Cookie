import socket

HOST = '127.0.0.1'
PORT = 5000

def main():
    print("Cliente de Fortunes conectado ao servidor.")
    print("Comandos disponíveis:")
    print("GET-FORTUNE | ADD-FORTUNE <frase> | UPD-FORTUNE <pos> <nova frase> | LST-FORTUNE | SAIR\n")
    print("Dica: pressione ENTER duas vezes para sair.\n")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            cmd = input(">> ").strip()

            # Se o usuário apertar ENTER duas vezes, encerra
            if cmd == "":
                print("Encerrando o cliente (ENTER duplo detectado).")
                break

            if cmd.upper() == "SAIR":
                print("Encerrando o cliente por comando.")
                break

            s.sendall(cmd.encode('utf-8'))
            data = s.recv(4096).decode('utf-8')
            print("Servidor:", data)

    print("Conexão encerrada.")

if __name__ == "__main__":
    main()
