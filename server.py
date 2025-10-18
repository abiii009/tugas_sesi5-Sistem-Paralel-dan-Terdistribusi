import socket
import threading

# Menyimpan semua koneksi client
clients = []
nicknames = []

# Membuat server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'  # localhost
port = 55555
server.bind((host, port))
server.listen()

print(f"Server berjalan di {host}:{port}")

# Fungsi untuk mengirim pesan ke semua client (broadcast)
def broadcast(message, _client=None):
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                # Jika terjadi kesalahan, hapus client dari daftar
                remove_client(client)

# Fungsi untuk menghapus client
def remove_client(client):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        client.close()
        nickname = nicknames[index]
        nicknames.remove(nickname)
        broadcast(f"{nickname} telah keluar dari chat.\n".encode('utf-8'))
        print(f"{nickname} terputus dari server.")

# Fungsi untuk menangani setiap client
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            remove_client(client)
            break

# Menerima koneksi dari client
def receive_connections():
    while True:
        client, address = server.accept()
        print(f"Terhubung dengan {str(address)}")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname client: {nickname}")
        broadcast(f"{nickname} telah bergabung ke chat!\n".encode('utf-8'))
        client.send("Terhubung ke server chat.\n".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print("Menunggu koneksi client...")
receive_connections()