import random
import string

class PrimaryVarDeclaration():

	def __init__(self, field, var_next):
		self.field  = field
		self.var_next = var_next
		self.dicc = dict()

	def evaluate(self):
		self.field.setDicc(self.dicc)
		self.var_next.setDicc(self.dicc)
		self.refCheck(self.dicc)
		exp = self.field.generate()
		return exp

	def refCheck(self, dicc):
		diccKeys = list(dicc.keys()) #creo una lista nueva con las claves del diccionario
		while (diccKeys): #mientras siga habiendo claves por revisar
			p = diccKeys[0] #agarro una clave arbitraria, la primera
			diccKeys.remove(p) #la saco de las claves porque ya la voy a revisar
			camino = list(p) #empiezo el camino de las referencias con p siendo el punto de partida
			self.DFS(p, diccKeys, dicc, camino)

	def DFS(self, p, diccKeys, dicc, camino):
		k = dicc.get(p) #accedo a la estructura del E correspondiende (sigo la referencia)
		while (k.referencias): #mientras siga habiendo referencias sin revisar
			c = k.referencias[0] #tomo referencia arbitraria
			if (c in camino): #si c ya est� en el camino quiere decir que se formar�a un ciclo
				#error de referencia circular
				raise Exception("Hay referencias circulares en los structs")
			else:
				camino.append(c) #agrego c al camino
				diccKeys.remove(c) #lo saco de las claves porque como estoy por revisarlo ahora no hace falta que lo revise nuevamente
				self.DFS(c, diccKeys, dicc, camino)
				k.referencias.remove(c) #luego de chequear esta referencia la borro y contin�o para no revisarla nuevamente
		camino.remove(k) #si ya cheque� todos los caminos que se desprenden de k entonces debo pasar a chequear otros caminos

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
		if not self.isEmpty:
			self.var_next.setDicc(dicc)

class TypeRefDeclaration():

	def __init__(self, id):
		self.id = id
		self.referencias = [id.value]
	
	# dicc e isArray tendrían que estar en el init o se pueden declarar así nomás?
	def setDicc(self, dicc, isArray):
		self.dicc = dicc
		self.isArray = isArray
	
	def generate(self):
		generate(self.isArray, self.dicc.get(self.id.value))

class TypeStructDeclaration():

	def __init__(self, next_declaration):
		self.next_declaration = next_declaration
		self.referencias = self.next_declaration.referencias
	
	def setDicc(self, dicc, isArray):
		self.dicc = dicc
		self.isArray = isArray
		self.next_declaration.setDicc(self.dicc)
	
	def generate(self):
		generate(self.isArray, self.next_declaration)

class BasicTypeDeclaration():

	def __init__(self, basicType):
		self.type = basicType
		self.referencias = []

	def setDicc(self, dicc, isArray):
		self.dicc = dicc
		self.isArray = isArray

	def generate(self):
		value = None
		if self.type == 'string':
			value = RandomString()
		elif self.type == 'int':
			value = RandomInt()
		elif self.type == 'float64':
			value = RandomFloat()
		else:
			value = RandomBool
		generate(self.isArray, value)

class RandomString():

	def generate(self):
		length = random.randint(1, 10)
		letters = string.ascii_lowercase
		return ''.join(random.choice(letters) for i in range(length))

class RandomInt():

	def generate(self):
		return random.randint(-1000, 1000)

class RandomFloat():

	def generate(self):
		return random.uniform(0, 1000)

class RandomBool():
	
	def generate(self):
		true = random.randint(0, 1)
		if true:
			return 'true'
		else:
			return 'false'

def generate(isArray, value):
	s = ''
	if isArray:
		s = '[ \n'
		i = random.randint(0, 5)
		while i > 0:
			s += value.generate() + ', \n'
			i -= 1
		s += ']'			
	else:
		s = value.generate() + ', \n'
	return s
