#Integrantes del equipos
#Almaraz Cruz Jacqueline
#Monroy Martinez Luis Pablo
import socket
import json

host = '127.0.0.1'
port = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

data = s.recv(1024)
num_cliente = int(data.decode())
print("Cliente #", num_cliente+1)

PosIni = []

def establecerPosIni():
	global PosIni
	if not PosIni:
		x = ''
		y = ''
		print("BInicial")
		print("Ingrese los valores de [0-7]")
		entrada = int(input("x> "))
		while entrada < 0 or entrada > 7:
			print("Numero no admitido en x.")
			entrada = int(input("x> "))
		x = entrada
		entrada = int(input("y> "))
		while entrada < 0 or entrada > 7:
			print("Numero no admitido en y.")
			entrada = int(input("y> "))
		y = entrada
		PosIni.append(x)
		PosIni.append(y)
		data = json.dumps({"x": x, "y": y})
		s.sendall(data.encode())

def main():
	Terminar = False
	while not Terminar:
		print("----------------------")
		print("Programa Caballos distribuidos")
		print("Para realizar alguna consulta, escribe lo siguiente:")
		print('1. BInicial')
		print('2. BCamino')
		print('3. BSoluciones')
		print('4. Salir')
		Leer = input("> ")
		if Leer == '1':
			s.sendall(b'1')
			establecerPosIni()
		elif Leer == '2':
			s.sendall(b'2')
			print("BCamino")
			s.sendall(bytes(str(num_cliente),'utf-8'))
		elif Leer == '3':
			s.sendall(b'3')
			print("BSoluciones")
		elif Leer == '4':
			s.sendall(b'4')
			print("Saliendo...")
			data = s.recv(1024)
			print(data.decode())
			return
		else:
			print("Expresión no reconocido, intenta escribirlo de forma correcta.\n")
		data = s.recv(1024)
		print(data.decode())

if __name__ == "__main__":
	main()

s.close()
