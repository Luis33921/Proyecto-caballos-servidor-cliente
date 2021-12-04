#Almaraz Cruz Jacqueline 
#Monroy Martínez Luis Pablo 
import socket
import json

host = "192.168.1.109"
port = 8080
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket se utilizan para enviar mensajes a través de una red.
s = socket.socket()
s.connect((host , port))

def establecerPosIni():
	x = ''
	y = ''
	print("Inicial")
	print("Ingrese los valores de un rango entre 0 & 7")
	entrada = int(input("Posicion X:"))
	while entrada < 0 or entrada > 7:
		print("ERROR!! <Valor no admitido en x>")
		print("Por favor ingresa otro valor dentro del rango")
		entrada = int(input("Posicion X: "))
	x = entrada
	entrada = int(input("Posicion Y: "))
	while entrada < 0 or entrada > 7:
		print("Numero no admitido en y.")
		print("ERROR!!<Valor no admitido en y>")
		print("Por favor ingresa otro valor dentro del rango")
	y = entrada
	data = json.dumps({"x": x, "y": y})
	s.sendall(data.encode())

def main():
	# Recibe el numero de identificacion que le envia el servidor
	data = s.recv(1024)
	num_cliente = int(data.decode())
	
	while True:
		print("\n----------------------")
		print("********Bienvenido al programa********\n")
		print("Cliente #", num_cliente+1)
		print("Programa Caballos distribuidos")
		print("Para realizar alguna consulta, ingrese el numero correcto de acuerdo a la opción deseada:")
		print('1. Iniciar')
		print('2. Camino')
		print('3. Soluciones')
		print('4. Salir')
		
		#Captura lo que el cliente quiera consultar
		Leer = input("> ")
		
		#Se envia el num de cliente que le corresponde, el servidor lo recibe
		# En la linea 213 de CDserver.py es donde lo recibe
		s.sendall(bytes(str(num_cliente),'utf-8'))
		
		#Se analiza que opcion eligio
		if Leer == '1':
			print("Realizando Inicial...")
			s.sendall(b'1')
			establecerPosIni()
		elif Leer == '2':
			print("Camino en proceso...")
			s.sendall(b'2')
		elif Leer == '3':
			print("Realizando BSoluciones...")
			s.sendall(b'3')
		elif Leer == '4':
			print("Saliendo del programa...")
			s.sendall(b'4')
			data = s.recv(1024)
			print(data.decode())
			return
		else:
			s.sendall(bytes(Leer,'utf-8'))
		
		#Recibe la respuesta del servidor
		data = s.recv(1024)
		
		#Y lo imprime
		print(data.decode())

if __name__ == "__main__":
    main()

#Cuando pida que quiere salir, sale del ciclo while, y por lo tanto termina el metodo del main
#al final la siguiete instruccion es lo ultimo que ejecutara por parte del DCcliente.py, que es salir "s.close()"
s.close()
