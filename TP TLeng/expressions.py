import random
import string

class PrimaryVarDeclaration():

	def __init__(self, field, var_next):
		self.field  = field
		self.var_next = var_next
		self.dicc = dict()

	def evaluate(self):
		self.field.setDicc(self.dicc, True)
		self.var_next.setDicc(self.dicc)
		self.refCheck(self.dicc)
		exp = self.field.generate()
		return exp

	def refCheck(self, dicc):
		diccKeys = list(dicc.keys()) #creo una lista nueva con las claves del diccionario
		while (diccKeys): #mientras siga habiendo claves por revisar
			p = diccKeys[0] #agarro una clave arbitraria, la primera
			diccKeys.remove(p) #la saco de las claves porque ya la voy a revisar
			camino = [p] #empiezo el camino de las referencias con p siendo el punto de partida
			self.DFS(p, diccKeys, dicc, camino)

	def DFS(self, p, diccKeys, dicc, camino):
		if p in dicc:
			k = dicc.get(p) #accedo a la estructura del E correspondiende (sigo la referencia)
		else:
			raise Exception("Se utilizan tipos sin definir")
		while (k.referencias): #mientras siga habiendo referencias sin revisar
			c = k.referencias[0] #tomo referencia arbitraria
			if (c in camino): #si c ya est� en el camino quiere decir que se formar�a un ciclo
				#error de referencia circular
				raise Exception("Hay referencias circulares en los structs")
			else:
				if c:
					camino.append(c) #agrego c al camino
				if c in diccKeys:
					diccKeys.remove(c) #lo saco de las claves porque como estoy por revisarlo ahora no hace falta que lo revise nuevamente
				self.DFS(c, diccKeys, dicc, camino)
				k.referencias.remove(c) #luego de chequear esta referencia la borro y contin�o para no revisarla nuevamente
		camino.remove(p) #si ya cheque� todos los caminos que se desprenden de k entonces debo pasar a chequear otros caminos

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

class FieldDeclaration():

	def __init__(self, referencias, id,  field_array, type_declaration):
		self.referencias = referencias
		self.id = id
		self.type_declaration = type_declaration
		self.field_array = field_array

	def setDicc(self, dicc, inStruct):
		if inStruct:
			if self.id in dicc:
				raise Exception('Tipo ya definido')
			else:
				dicc[self.id] = self.type_declaration
				self.type_declaration.setDicc(dicc, self.field_array["cantArrays"])
		else:
			self.type_declaration.setDicc(dicc, self.field_array["cantArrays"])

	def generate(self):
		return '"' + self.id + '"' + ':' + self.type_declaration.generate()

class TypeNextDeclaration():

	def __init__(self, endOfStruct, referencias, field_declaration, type_next_declaration):
		self.endOfStruct = endOfStruct
		self.referencias = referencias
		self.field_declaration = field_declaration
		self.type_next_declaration = type_next_declaration

	def setDicc(self, dicc):
		if not self.endOfStruct:
			self.field_declaration.setDicc(dicc, False)
			self.type_next_declaration.setDicc(dicc)

	def generate(self):
		s = ''
		if not self.endOfStruct:
			s = self.field_declaration.generate()
			if not self.type_next_declaration.endOfStruct:
				s += ', \n' + self.type_next_declaration.generate()
		return s

class TypeRefDeclaration():

	def __init__(self, id):
		self.id = id
		self.referencias = [id]
	
	def setDicc(self, dicc, cantArrays):
		self.dicc = dicc
		self.cantArrays = cantArrays
	
	def generate(self):
		return generate(self.cantArrays, self.dicc.get(self.id))

class TypeStructDeclaration():

	def __init__(self, next_declaration):
		self.next_declaration = next_declaration
		self.referencias = next_declaration.referencias
	
	def setDicc(self, dicc, cantArrays):
		self.dicc = dicc
		self.cantArrays = cantArrays
		self.next_declaration.setDicc(self.dicc)
	
	def generate(self):
		return '{ \n' + generate(self.cantArrays, self.next_declaration) + '}'

class BasicTypeDeclaration():

	def __init__(self, basicType):
		self.type = basicType
		self.referencias = list()

	def setDicc(self, dicc, cantArrays):
		self.dicc = dicc
		self.cantArrays = cantArrays

	def generate(self):
		value = None
		if self.type == 'string':
			value = RandomString()
		elif self.type == 'int':
			value = RandomInt()
		elif self.type == 'float64':
			value = RandomFloat()
		else:
			value = RandomBool()
		return generate(self.cantArrays, value)

class RandomString():

	def generate(self):
		length = random.randint(5, 10)
		letters = string.ascii_lowercase
		return ''.join(random.choice(letters) for i in range(length))

class RandomInt():

	def generate(self):
		return str(random.randint(-1000, 1000))

class RandomFloat():

	def generate(self):
		return str(random.uniform(0, 1000))

class RandomBool():

	def generate(self):
		true = random.randint(0, 1)
		if true:
			return 'true'
		else:
			return 'false'

def generate(cantArrays, value):
	s = ''
	if cantArrays > 0:
		s = '[ \n'
		i = random.randint(0, 5)
		while i > 0:
			if cantArrays > 1:
				s += generate(cantArrays - 1, value)
			else:
				s += value.generate() + ', \n'
			i -= 1
		s += ']'			
	else:
		s = value.generate() 
	return s
