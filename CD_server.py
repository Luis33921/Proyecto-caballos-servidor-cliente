#Integrantes del equipos
#Almaraz Cruz Jacqueline
#Monroy Martinez Luis Pablo
import socket
import json
import copy

host = ''
port = 8888

PosIni = []
TCamino = []
respuestas = []
soluciones = []
num_cliente = 0

posPosibles = [[] for x in range(64)]
marcados = ["No" for x in range(64)]

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

#crearTableroMov se estiman los movimientos posibles para cada casilla
tableroMov = crearTableroMov()

def iniciar(Pos,Tablero):
	global posPosibles
	global marcados
	for i in range(len(posPosibles)):
		posPosibles[i] = []
	for i in range(len(marcados)):
		marcados[i] = "No"
	M = [[2,[Pos[0],Pos[1]],copy.deepcopy(Tablero)]]
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
		return M
	else:
		print("Reintentando...")
		M2 = iniciar(Pos,Tablero)
		return M2

def proceso(t,posV,posH,i):
	pV = posV
	pH = posH
	espacios = contarEspacios(t)
	tamaño = len(t)*len(t[0])
	if espacios == 0:
		return False
	else:
		if espacios == tamaño:
			t[pV][pH] = tamaño - (espacios - 1)
		else:
			pV,pH = movSiguiente(t,posV,posH,i)
			if pV == posV and pH == posH:
				t[pV][pH] = 0
				marcados[i] = "No"
				return False
			else:
				t[pV][pH] = tamaño - (espacios - 1)
		return [[pV,pH],t]

def movSiguiente(T,pV,pH,i):
	posM = posiblesMovimientos(T,pV,pH)
	if posM:
		if not posPosibles[i] and marcados[i] == "No":
			posPosibles[i] = posM
			marcados[i] = "Si"
	if posPosibles[i]:
		pos = determinarMenorCantidad(T,i)
		pV = pos[0]
		pH = pos[1]
		posPosibles[i].remove(pos)
	return pV,pH

def posiblesMovimientos(T,pV,pH):
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
			aux_pV = pV + (j[0] * desV)
			aux_pH = pH + (j[1] * desH)
			if aux_pV >= 0 and aux_pV < len(T):
					if aux_pH >= 0 and aux_pH < len(T[0]):
						if T[aux_pV][aux_pH] == 0:
							posiblesMov.append([aux_pV,aux_pH])
	return posiblesMov

def contarEspacios(T):
	cont = 0
	for i in T:
		for j in i:
			if j == 0:
				cont += 1
	return cont

def determinarMenorCantidad(T,i):
	menor = 0
	pos = None
	for i in posPosibles[i]:
		if menor == 0:
			menor = tableroMov[i[0]][i[1]]
			pos = i
		else:
			if tableroMov[i[0]][i[1]] < menor:
				menor = tableroMov[i[0]][i[1]]
				pos = i
	return pos

def recibirPosIni(conn):
	global PosIni
	global TCamino
	global respuestas
	if not PosIni:
		data = conn.recv(1024)
		data = json.loads(data.decode())
		PosIni.append(data.get("x"))
		PosIni.append(data.get("y"))
		print('Posicion Inicial establecido.')
		#GENERA LOS TABLEROS PARA BCamino
		T = crearTablero()
		x = PosIni[0]
		y = PosIni[1]
		T[x][y] = 1
		Primeros_movimientos = posiblesMovimientos(T,x,y)
		for i in range(len(Primeros_movimientos)):
			Seg_posicion = Primeros_movimientos[i]
			T2 = copy.deepcopy(T)
			T2[Seg_posicion[0]][Seg_posicion[1]] = 2
			TCamino.append([Seg_posicion,T2])
			respuestas.append([])
		return b'Posicion Inicial establecido'
	else:
		return b'Ya se ha establecido'

def entregarTablero(conn):
	global PosIni
	global TCamino
	global respuestas
	global soluciones
	ind = int(conn.recv(1024).decode())
	if PosIni:
		if not respuestas[ind]:
			Pos = TCamino[ind][0]
			Tablero = TCamino[ind][1]
			result = iniciar(Pos,Tablero)
			respuestas[ind] = result[62][2]
			if not soluciones:
				soluciones.append(ind+1)
				soluciones.append(result[62][2])
			return bytes("Solucion al tablero #" + str(ind+1) + "\n" + str(respuestas[ind]),'utf-8')
		else:
			if TCamino[ind]:
				return bytes("Solucion al tablero #" + str(ind+1) + "\n" + str(respuestas[ind]),'utf-8')
			else:
				return b'Ya no hay tableros disponibles'
	else:
		return b'No se establecio Posicion Inicial'

def enviarSoluciones(conn):
	global soluciones
	if soluciones:
		return bytes("Primera solucion: Tablero #" + str(soluciones[0]) + "\n" + str(soluciones[1]),'utf-8')
	else:
		return b'No hay solucion registrada'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((host, port))
	s.listen(8)
	print('El servidor está comenzando ...')
	conn,addr = s.accept()
	with conn:
		print("Conectado a", addr)
		data = bytes(str(num_cliente),'utf-8')
		conn.sendall(data)
		while True:
			data = conn.recv(1024)
			print(data.decode())
			if data.decode() == '1':
				data = recibirPosIni(conn)
			elif data.decode() == '2':
				data = entregarTablero(conn)
			elif data.decode() == '3':
				data = enviarSoluciones(conn)
			elif data.decode() == '4':
				data = b'Session Finalizada'
				conn.sendall(data)
				break
			conn.sendall(data)
