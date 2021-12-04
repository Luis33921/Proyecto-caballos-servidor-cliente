#Almaraz Cruz Jacqueline 
#Monroy Martínez Luis Pablo 
#1
import socket
from threading import Thread
import json
import copy
"""Variables"""
CaminoTablero = []
respuestas = []
soluciones = []
posicionInicial = []
contarCliente = 0

"""INICIA CODIGO DEL CAMINO DEL CABALLO"""
marcados = ["No" for x in range(64)]
posibPosiciones = [[] for x in range(64)]


def crearTablero():
	return [
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0]
	]
def crearTableroMov():
	return [
		[2,3,4,4,4,4,3,2],
		[3,4,6,6,6,6,4,3],
		[4,6,8,8,8,8,6,4],
		[4,6,8,8,8,8,6,4],
		[4,6,8,8,8,8,6,4],
		[4,6,8,8,8,8,6,4],
		[3,4,6,6,6,6,4,3],
		[2,3,4,4,4,4,3,2]
	]

"""TablaMovimientos se estiman los movimientos posibles para cada casilla"""
tableroMov = crearTableroMov()
#2
def iniciar(ubicacion,Tablero):
	global posibPosiciones
	global marcados
	for i in range(len(posibPosiciones)):
		posibPosiciones[i] = []
	for i in range(len(marcados)):
		marcados[i] = "No"
	M = [[2,[ubicacion[0],ubicacion[1]],copy.deepcopy(Tablero)]]
	tamaño = len(M[0][2])*len(M[0][2][0]) - 3
	i = 0
	while i <= tamaño:
		iteracion = proceso(copy.deepcopy(M[i][2]),M[i][1][0],M[i][1][1],M[i][0])
		if iteracion:
			if (len(M)) >= (i+2):
				M[i+1] =[M[i][0]+1] + iteracion
			else:
				M.append([M[i][0]+1] + iteracion)
		else:
			i -= 2
		i += 1
	if len(M) == 63:
		print("Solución terminada.")
		return M[62][2]
	else:
		return "No hay solucion"
#3
def SigMovimiento(TableroM,posicionVertical,posicionHorizontal,i):
	posM = posiblesMovimientos(TableroM,posicionVertical,posicionHorizontal)
	if posM:
		if not posibPosiciones[i] and marcados[i] == "No":
			posibPosiciones[i] = posM
			marcados[i] = "Si"
	if posibPosiciones[i]:
		ubicacion = determinarMenorCantidad(TableroM,i)
		posicionVertical = ubicacion[0]
		posicionHorizontal = ubicacion[1]
		posibPosiciones[i].remove(ubicacion)
	return posicionVertical,posicionHorizontal
#4
def posiblesMovimientos(TableroM,posicionVertical,posicionHorizontal):
	valores = [2,1]
	formas = [[-1,1],[1,1],[1,-1],[-1,-1]]
	posiblesMov = []
	for i in valores:
		desH = i
		if desH == 1:
			desV = 2
		else:
			desV = 1
		for j in formas:
			aux_pV = posicionVertical + (j[0] * desV)
			aux_pH = posicionHorizontal + (j[1] * desH)
			if aux_pV >= 0 and aux_pV < len(TableroM):
					if aux_pH >= 0 and aux_pH < len(TableroM[0]):
						if TableroM[aux_pV][aux_pH] == 0:
							posiblesMov.append([aux_pV,aux_pH])
	return posiblesMov
#5	
def proceso(TableroM,posV,posH,i):
	posicionVertical = posV
	posicionHorizontal = posH
	espacios = EspaciosLibres(TableroM)
	if espacios == 0:
		return False
	else:
		posicionVertical,posicionHorizontal = SigMovimiento(TableroM,posV,posH,i)
		if posicionVertical == posV and posicionHorizontal == posH:
			TableroM[posicionVertical][posicionHorizontal] = 0
			marcados[i] = "No"
			return False
		else:
			TableroM[posicionVertical][posicionHorizontal] = 64 - (espacios - 1)
		return [[posicionVertical,posicionHorizontal],TableroM]

#6
def EspaciosLibres(TableroM):
#cuenta y devuelve el numero de espacios por el cual el caballo no ha pasado.
	cont = 0
	for i in TableroM:
		for j in i:
			if j == 0:
				cont += 1
	return cont
#7
def determinarMenorCantidad(TableroM,i):
	menor = 0
	ubicacion = None
	for i in posibPosiciones[i]:
		if menor == 0:
			menor = tableroMov[i[0]][i[1]]
			ubicacion = i
		else:
			if tableroMov[i[0]][i[1]] < menor:
				menor = tableroMov[i[0]][i[1]]
				ubicacion = i
	return ubicacion

"""***************************FIN DEL PROGRAMA****************************"""

#8
def recibirPosIni(conn):
	global posicionInicial
	global CaminoTablero
	global respuestas
#ignorando el valor de retorno de json.loads()
	#Luego intenta decodificar el mismo sin formato nuevamente e intenta usarlo como el resultado decodificado de Python. Llame json.loads()
	data = conn.recv(1024)
	data = json.loads(data.decode())
	posicionInicial.append(data.get("x"))
	posicionInicial.append(data.get("y"))
	print('Posicion Inicial establecido.')
	#GENERA LOS TABLEROS PARA BCamino
	TableroM = crearTablero()
	x = posicionInicial[0]
	y = posicionInicial[1]
	TableroM[x][y] = 1
	Primeros_movimientos = posiblesMovimientos(TableroM,x,y)
	for i in range(len(Primeros_movimientos)):
		Seg_posicion = Primeros_movimientos[i]
		T2 = copy.deepcopy(TableroM)
		T2[Seg_posicion[0]][Seg_posicion[1]] = 2
		CaminoTablero.append([Seg_posicion,T2])
		respuestas.append([])
#9
def entregarTablero(conn,ind):
	global posicionInicial
	global CaminoTablero
	global respuestas
	global soluciones
	if not respuestas[ind]:
		ubicacion = CaminoTablero[ind][0]
		Tablero = CaminoTablero[ind][1]
		result = iniciar(ubicacion,Tablero)
		respuestas[ind] = result
		if not soluciones:
			soluciones.append(ind+1)
			soluciones.append(result)
		return bytes("Solucion al tablero #" + str(ind+1) + "\n" + str(respuestas[ind]),'utf-8')
	else:
		if CaminoTablero[ind]:
			return bytes("Solucion al tablero #" + str(ind+1) + "\n" + str(respuestas[ind]),'utf-8')
		else:
			return b'Ya no hay tableros disponibles'
#10
class Client(Thread):
	def __init__(self, conn, addr):
		# Inicializar clase padre.
		Thread.__init__(self)
		self.conn = conn
		self.addr = addr
	
	def run(self):
		global posicionInicial
		global soluciones
		global contarCliente
		
		# El servidor le asigna un numero de identificacion al cliente, permite distinguir en la consola
		# cuales acciones estan haciendo los clientes
		data = bytes(str(contarCliente),'utf-8')
		self.conn.sendall(data)
		
		#Se incrementa para que el siguiente cliente no se le asigne al mismo del anterior
		contarCliente += 1
		
		while True:
			#Primero el servidor captura o recibe que num de cliente es
			n_cliente = int(self.conn.recv(1024).decode())
			
			#El servidor captura las opciones que va seleccionando el cliente
			data = self.conn.recv(1024)
			
			if data.decode() == '1':
				print("Cliente #", n_cliente + 1, "realizo Inicial")
				if not posicionInicial:
					recibirPosIni(self.conn)
					data = b'Posicion Inicial establecido'
				else:
					data = self.conn.recv(1024) #es para que capture la posicion pero no pasa por recibirPosIni ya que se estara ignorando cuando se ingrese mas de una vez la PosIni
					data = b'Ya se ha establecido anteriormente'
#11
			elif data.decode() == '2':
				print("Cliente #", n_cliente + 1, "realizo Camino")
				if posicionInicial:
					data = entregarTablero(self.conn,n_cliente)
				else:
					data = b'No se establecio Posicion Inicial'
			elif data.decode() == '3':
				print("Cliente #", n_cliente + 1, "realizo Soluciones")
				if soluciones:
					data = bytes("Primera solucion: Tablero #" + str(soluciones[0]) + "\n" + str(soluciones[1]),'utf-8')
				else:
					data = b'No hay solucion registrada'
			elif data.decode() == '4':
				print("Cliente #", n_cliente + 1, "realizo Salir")
				data = b'Session Finalizada'
				self.conn.sendall(data)
				return
			else:
				print("Error en sentencia:",data.decode())
				data = b'Expresion no reconocido, intenta escribirlo de forma correcta'
			
			#Envia el resultado que ha generado el cliente segun la decision que toma.
			self.conn.sendall(data)
#12
def main():
	global contarCliente
	#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s = socket.socket()
	
	# Escuchar peticiones en el puerto 8080.
	host = "192.168.1.109"
	port = 8080
	#BUFFER_SIZE = 1024 # Usamos un número pequeño para tener una respuesta rápida 
	
	s.bind((host, port))
	s.listen()
	print('El servidor ha iniciado ...')
	while True:
		conn, addr = s.accept()
		c = Client(conn, addr)
		c.start()
		print("Se ha conectado el cliente #",str(contarCliente+1),"(%s:%d)" % addr)

if __name__ == "__main__":
	main()
