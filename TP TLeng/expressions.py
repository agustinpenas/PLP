class PrimaryVarDeclaration():

	def __init__(self, field, var_next):
		self.field  = field
		self.var_next = var_next
		self.dicc = new Dictionary()

	def evaluate(self):
		field.setDicc(self.dicc)
		var_next.setDicc(self.dicc)
		self.refCheck(self.dicc)
		exp = field.generate()
		return exp

	def refCheck(self, dicc):
		diccKeys = list(dicc.keys()) #creo una lista nueva con las claves del diccionario
		while (diccKeys): #mientras siga habiendo claves por revisar
			p = diccKeys[0] #agarro una clave arbitraria, la primera
			diccKeys.remove(p) #la saco de las claves porque ya la voy a revisar
			camino = list(p) #empiezo el camino de las referencias con p siendo el punto de partida
			self.DFS(p,diccKeys,dicc,camino)

	def DFS(self,p,diccKeys,dicc,camino):
		k= dicc.get(p) #accedo a la estructura del E correspondiende (sigo la referencia)
		while (k.referencias): #mientras siga habiendo referencias sin revisar
			c = k.referencias[0] #tomo referencia arbitraria
			if (c in camino): #si c ya está en el camino quiere decir que se formaría un ciclo
				#error de referencia circular
			else:
				camino.append(c) #agrego c al camino
				claves.remove(c) #lo saco de las claves porque como estoy por revisarlo ahora no hace falta que lo revise nuevamente
				self.DFS(c,diccKeys,dicc,camino)
				k.referencias.remove(c) #luego de chequear esta referencia la borro y continúo para no revisarla nuevamente
		camino.remove(k) #si ya chequeé todos los caminos que se desprenden de k entonces debo pasar a chequear otros caminos

class VarDeclaration():

	def __init__(self, field, var_next):
		self.field 	  = field
		self.var_next = var_next

	def setDicc(self, dicc):
		self.field.setDicc(dicc, True)
		self.var_next.setDicc(dicc)

class VarNextDeclaration():

	def __init__(self, var_next, isEmpty):
		self.var_next = var_next
		self.isEmpty  = isEmpty

	def setDicc(self, dicc):
		if !(self.isEmpty):
			self.var_next.setDicc(dicc)