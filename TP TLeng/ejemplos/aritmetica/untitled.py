class PrimaryVarDeclaration():

	def __init__(self, field, var_next):
		self.field  = field
		self.var_next = var_next
		self.dicc = new Dictionary()

	def evaluate(self):
		field.setDicc(self.dicc)
		var_next.setDicc(self.dicc)
		exp = field.generate()
		return exp

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