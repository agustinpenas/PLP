:- dynamic si/1, no/1, atributos/2.

adivinarPersonaje :- atributos(X,Y), satisfaceAtributos(Y), write(X), nl, borraRespuestas(), !.
adivinarPersonaje :- write('Quien es ese? ingrese el nombre papu '), nl, read(P), write('Y sus atributos?'), nl, read(AS), atributosRespondidos(ATR), append(AS, ATR, ATR2), agregarPersonaje(P, ATR2), borraRespuestas(). 

atributosRespondidos([]) :- not(si(_)).
atributosRespondidos([X|XS]) :- si(X), retractall(si(X)), atributosRespondidos(XS),not(member(X,XS)), !.


atributosUnicos(XS) :- not((atributos(_,YS),permutation(YS, XS))).

atributosSinRepetidos([], []).
atributosSinRepetidos([X|XS], L) :- member(X, XS), atributosSinRepetidos(XS, L).
atributosSinRepetidos([X|XS], [X|L]) :- not(member(X, XS)), atributosSinRepetidos(XS, L).

% agregarPersonaje(+Nombre, +Atributos).
agregarPersonaje(_, []) :- fail, !.
agregarPersonaje(P, AS) :- atributosSinRepetidos(AS, ASS), atributosUnicos(ASS), assertz(atributos(P, ASS)).

% mostrarPersonaje(+Nombre).
mostrarPersonaje(_) :- fail.

borraRespuestas :- retractall(si(_)), retractall(no(_)).

% atributos(?Nombre, ?Atributos).
atributos(apu, [indio, padre, hombre, mayor_de_edad, cajero]).
atributos(homero, [hombre, padre, mayor_de_edad, tecnico_nuclear, casado, calvo]).
atributos(bart, [hombre, menor_de_edad, estudiante, quilombero]).
atributos(lisa, [mujer, menor_de_edad, estudiante, responsable, necesita_frenos]).
atributos(marge, [mujer, mayor_de_edad, casado, ama_de_casa]).
atributos(abraham, [hombre, mayor_de_edad, viudo, jubilado, abuelo]).
atributos(barney, [hombre, mayor_de_edad, borracho, soltero]).
atributos(nelson, [hombre, menor_de_edad, quilombero, abusador]).
atributos(moe, [hombre, mayor_de_edad, soltero, portador_de_armas, cantinero]).
atributos(krusty, [hombre, mayor_de_edad, borracho, payaso, judio]).


% satisfaceAtributos(+Atributos).
satisfaceAtributos([]).
satisfaceAtributos([A|AS]) :- satisface(A), satisfaceAtributos(AS).

% satisface(+Atributo).
satisface(A) :- si(A), !.
satisface(A) :- not(no(A)), pregunta(A), si(A).

% pregunta(+Atributo).
pregunta(A) :- mostrarPregunta(A), leerRespuesta(R), guardarRespuesta(A,R).

% mostrarPregunta(+Atributo).
mostrarPregunta(B) :- atom_string(B, A), string_concat("¿Es el/la personaje ", A, A2), string_concat(A2, "?", A3), write(A3), nl.

% leerRespuesta(-Respuesta).
leerRespuesta(R) :- read(R).

% guardarRespuesta(+Atributo, +Respuesta).
guardarRespuesta(A, R) :- R == 'si', !, assertz(si(A)).
guardarRespuesta(A, R) :- R == 'no', !, assertz(no(A)).
guardarRespuesta(A, _) :- write('Respuesta inválida. Se pregunta nuevamente.\n'), pregunta(A).


%%%%%%%%%%%%%%%% TESTS %%%%%%%%%%%%%%%%%%%%%%%%%
test(1) :- true.
tests :- forall(between(1,1,N), test(N)). % Hacer mejores tests y cambiar 1 por la cantidad de tests que tengan.

/*Ej 7.
Falla porque no existe alguno que satisfaga simultaneamente todos los atributos indicados.
Influye en el orden en el que se realizan las preguntas y la rapidez con la que se descartan posibles soluciones.
*/

/*Ej 8.
No, ya que cambia el orden de evaluación: en el caso de assertz hace que considere al personaje agregado como la última posible solución mientras que con 
asserta considera al personaje como la primera posible solución.
*/