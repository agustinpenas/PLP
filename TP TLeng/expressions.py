import random
import string
from sys import stderr, exit

# A -> type T S'
class PrimaryTypeDefinition():

	def __init__(self, type_declaration, new_type):
		self.type_declaration  = type_declaration
		self.new_type = new_type
		self.dicc = dict()

	def evaluate(self):
		self.type_declaration.setDicc(self.dicc, False)
		self.new_type.setDicc(self.dicc)
		self.refCheck(self.dicc)
		exp = self.type_declaration.generate(True)
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
			stderr.write('El tipo "' + p + '" está sin definir')
			exit()
		while (k.referencias): #mientras siga habiendo referencias sin revisar
			c = k.referencias[0] #tomo referencia arbitraria
			if (c in camino): #si c ya está en el camino quiere decir que se formaría un ciclo
				stderr.write('Hay referencias circulares en el tipo "' + p + '"')
				exit()
			else:
				if c:
					camino.append(c) #agrego c al camino
				if c in diccKeys:
					diccKeys.remove(c) #lo saco de las claves porque como estoy por revisarlo ahora no hace falta que lo revise nuevamente
				self.DFS(c, diccKeys, dicc, camino)
				k.referencias.remove(c) #luego de chequear esta referencia la borro y contin�o para no revisarla nuevamente
		camino.remove(p) #si ya chequeé todos los caminos que se desprenden de k entonces debo pasar a chequear otros caminos

# S -> type T S'
class TypeDefinition():

	def __init__(self, type_declaration, new_type):
		self.type_declaration = type_declaration
		self.new_type = new_type

	def setDicc(self, dicc):
		self.type_declaration.setDicc(dicc, False)
		self.new_type.setDicc(dicc)

# S' -> S | lambda
class NewTypeDefinition():

	def __init__(self, new_type, isEmpty):
		self.new_type = new_type
		self.isEmpty  = isEmpty

	def setDicc(self, dicc):
		if not self.isEmpty:
			self.new_type.setDicc(dicc)

# T -> id T' E
class TypeDeclaration():

	def __init__(self, referencias, id,  field_array, _type):
		self.referencias = referencias
		self.id = id
		self.type = _type
		self.field_array = field_array

	def setDicc(self, dicc, inStruct):
		if not inStruct:
			if self.id in dicc:
				stderr.write('El tipo "' + self.id + '" ya está definido')
				exit()
			else:
				dicc[self.id] = self.type
				self.type.setDicc(dicc, self.field_array["cantArrays"])
		else:
			self.type.setDicc(dicc, self.field_array["cantArrays"])

	def generate(self, isPrimaryType):
		if isPrimaryType:
			s = self.type.generate()
		else:
			s = '"' + self.id + '"' + ':' + self.type.generate()
		return s

# E' -> T E' | lambda
class StructField():

	def __init__(self, endOfStruct, referencias, type_declaration, next_struct_field):
		self.endOfStruct = endOfStruct
		self.referencias = referencias
		self.type_declaration = type_declaration
		self.next_struct_field = next_struct_field

	def setDicc(self, dicc):
		if not self.endOfStruct:
			self.type_declaration.setDicc(dicc, True)
			self.next_struct_field.setDicc(dicc)

	def generate(self):
		s = ''
		if not self.endOfStruct:
			s = self.type_declaration.generate(False)
			if not self.next_struct_field.endOfStruct:
				s += ', \n' + self.next_struct_field.generate()
		return s

# E -> id
class TypeRef():

	def __init__(self, id):
		self.id = id
		self.referencias = [id]
	
	def setDicc(self, dicc, cantArrays):
		self.dicc = dicc
		self.cantArrays = cantArrays
	
	def generate(self):
		return generate(self.cantArrays, self.dicc.get(self.id))

# E -> struct{E'}
class TypeStruct():

	def __init__(self, struct_field):
		self.struct_field = struct_field
		self.referencias = struct_field.referencias
	
	def setDicc(self, dicc, cantArrays):
		self.dicc = dicc
		self.cantArrays = cantArrays
		self.struct_field.setDicc(self.dicc)
	
	def generate(self):
		if self.cantArrays > 0:
			s = self.cantArrays
			self.cantArrays = 0
			return generate(s, self)
		else:
			return '{ \n' + generate(self.cantArrays, self.struct_field) + '\n}'

# E -> string | int | float64 | bool
class BasicType():

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
		return '"' + ''.join(random.choice(letters) for i in range(length)) + '"'

class RandomInt():

	def generate(self):
		return str(random.randint(0, 1000))

class RandomFloat():

	def generate(self):
		return str('{:.1f}'.format(random.uniform(0, 1000)))

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
				s += value.generate()
			if i == 1:
				s += ' \n'
			else:
				s += ', \n'
			i -= 1
		s += ']'			
	else:
		s = value.generate() 
	return s
