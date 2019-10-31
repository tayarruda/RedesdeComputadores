# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Base de um servidor HTTP
#

# importacao das bibliotecas
import socket

# definicao do host e da porta do servidor
HOST = '' # ip do servidor (em branco)
PORT = 8080 # porta do servidor

# cria o socket com IPv4 (AF_INET) usando TCP (SOCK_STREAM)
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# permite que seja possivel reusar o endereco e porta do servidor caso seja encerrado incorretamente
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# vincula o socket com a porta (faz o "bind" do IP do servidor com a porta)
listen_socket.bind((HOST, PORT))

# "escuta" pedidos na porta do socket do servidor
listen_socket.listen(1)

# imprime que o servidor esta pronto para receber conexoes
print 'Servidor HTTP aguardando conexoes na porta %s ...' % PORT

while True:
    # aguarda por novas conexoes
    client_connection, client_address = listen_socket.accept()
    # o metodo .recv recebe os dados enviados por um cliente atraves do socket
    request = client_connection.recv(1024)
    # imprime na tela o que o cliente enviou ao servidor
    print request
    mypage = open('index.html','r').read()

    # declaracao da resposta do servidor
    comando = request.split(' ')
    if comando[0] == "GET":
        if comando[1] == '/':
            #deful
            http_response = """\

HTTP/1.1 200 OK

"""+mypage
        #requisicao do favicon
        elif comando[1] == '/icon':
            print "oi"
            contents = open("hearticon.png", "rb").read()
            http_response = "HTTP/1.1 200 OK\r\n"+"Connection: close\r\n" + "Content-Type: image/png\r\n" + \
                "Content-Length: " + str(len(contents)) + "\r\n\r\n" + contents
        else:
            #comando diferente
            try:
                arquivo = comando[1].split('/')
                #o que estiver dentro de format sera substituido
                encontra = open('{}'.format(arquivo[1]), 'r').read()
                http_response = """\

HTTP/1.1 200 OK

"""+encontra
            except IOError:
                nf = open('notfound.html','r').read()
                http_response = """\

HTTP/1.1 404 Not Found


"""+nf
    else:
        brq = open('badrqst.html','r').read()
        http_response = """\
HTTP/1.1 400 Bad Request\r\n\r\n

"""+brq
    # servidor retorna o que foi solicitado pelo cliente (neste caso a resposta e generica)
    client_connection.send(http_response)
    # encerra a conexao
    client_connection.close()

# encerra o socket do servidor
listen_socket.close()
