//Escriban acá su código.
//Ejercico 1
let qf = { esFinal : true, transiciones : null, acepta : function (s) {return s.length == 0}}

let q3 = { esFinal : true, transiciones : {}}
let q2 = { esFinal : true, transiciones : {c : q3}}
let q1 = { esFinal : false, transiciones : {a : this, b : q2, c : q3}}

//Ejercicio 2
String.prototype.head = function () {return this.charAt(0)}
String.prototype.tail = function () {return this.substring(1, this.length)}

//Ejercicio 3.2
q1.acepta = function (s) {
	let aceptoCadena = (s.length == 0) && this.esFinal
	for (let estado in this.transiciones) {
		if (s.head() == estado){
			let hijoAcepta = this.transiciones[estado].acepta(s.tail())
			aceptoCadena = aceptoCadena || hijoAcepta
		}
	}
	return aceptoCadena
}


Object.setPrototypeOf(q2,q1);
Object.setPrototypeOf(q3,q1);

//Ejercicio 3.1
function Estado(esFinal, transiciones){
	this.esFinal = esFinal
	this.transiciones = transiciones
}

Estado.prototype.acepta = function (s) {
	let aceptoCadena = (s.length == 0) && this.esFinal
	for (let estado in this.transiciones) {
		if (s.head() == estado){
			let hijoAcepta = this.transiciones[estado].acepta(s.tail())
			aceptoCadena = aceptoCadena || hijoAcepta
		}
	}
	return aceptoCadena
}

q3 = new Estado(true, {})
q2 = new Estado(true, {c : q3})
q1 = new Estado(false,  {b : q2, c : q3})
q1.transiciones.a = q1;

//Ejercicio 4
Estado.prototype.nuevaTransicion = function (etiqueta, destino){
	this.transiciones[etiqueta] = destino
}

//q3.nuevaTransicion('a', q1)

//Ejericio 5
let algunoAcepta = function(s,qs) {
	if (Array.isArray(qs)){
		return qs.some(q => q.acepta(s))
	}else{
		return qs.acepta(s)
	}
}


///Ej 6
Estado.prototype.acepta = function (s) {
	let aceptoCadena = (s.length == 0) && this.esFinal;
	for (let estado in this.transiciones) {

		if (s.head() == estado){
			let hijoAcepta = algunoAcepta(s.tail(),this.transiciones[estado]);
			aceptoCadena = aceptoCadena || hijoAcepta;
		}
	}
	return aceptoCadena;
}

Estado.prototype.nuevaTransicionND = function (etiqueta, destino){
	if (this.transiciones[etiqueta] != destino){
		if (Array.isArray(this.transiciones[etiqueta])){
			let array = this.transiciones[etiqueta]
			if (!array.includes(destino)){
				array.push(destino);
			}
		}else{
			if (this.transiciones[etiqueta] == undefined){
				this.transiciones[etiqueta] = destino
			}else{
				let array = [destino, this.transiciones[etiqueta]]
				this.transiciones[etiqueta] = array	
			}
		}
	}
}

q3.nuevaTransicionND('d', q2)
q3.nuevaTransicionND('d', q1)

//Ejercicio 7
let esDeterministicoOFueVisitado = function(q,visitados){
	let esDeterministico = true;
	for (let estado in q.transiciones) {
		if (Array.isArray(q.transiciones[estado])){
			return false
		}else{
			if (!visitados.includes(q.transiciones[estado])){
				visitados.push(q.transiciones[estado]);
				esDeterministico = esDeterministico && esDeterministicoOFueVisitado(q.transiciones[estado],visitados)
			}
		}
	}
	return esDeterministico;
}

let esDeterministico = q => esDeterministicoOFueVisitado(q,[q])


function calcularResultado(){

	console.log(esDeterministico(q2))
	console.log(q1.acepta('bcdcdb'))
	console.log(algunoAcepta('a', q1))
	console.log(algunoAcepta('bc', [q1, q2]))
	console.log(q1.acepta('bc'))
	console.log(q1.acepta('abcab'))
	console.log(q1.acepta('abcaa'))
	//Editen esta función para que devuelva lo que quieran ver. Pueden escribir acá sus tests.
	return "Ac&aacute; va el resultado.";
}
