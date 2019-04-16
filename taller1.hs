import Test.HUnit

-- Definiciones de tipos

data AB a = Nil | Bin (AB a) a (AB a) deriving Eq

instance Show a => Show (AB a) where
  show t = padAB t 0 0

-- Funciones auxiliares

pad :: Int -> String
pad i = replicate i ' '

padAB :: Show a => AB a -> Int -> Int -> String
padAB = foldAB (const $ const "") (\ri x rd n base ->let l = length $ show x in pad n ++ show x ++ ri 4 (base+l) ++ "\n" ++ rd (n+4+base+l) base)

-- Crea una hoja de un árbol binario AB
abHoja :: a -> AB a
abHoja x = Bin Nil x Nil

-- Devuelve una lista con los elementos de los nodos de un árbol binario AB recorridos en profundidad de izquierda a derecha
inorder :: AB a -> [a]    
inorder = foldAB [] (\i r d -> i ++ (r:d))

-- Estructuras para tests

-- Heap (<) completo
ab1 = Bin (abHoja 4) 2 (abHoja 5)
-- Heap (<) completo
ab2 = Bin (abHoja 6) 3 (abHoja 7)
-- Heap (>) completo
ab3 = Bin (Bin (abHoja 4) 5 (abHoja 2)) 7 (Bin (abHoja 3) 6 (abHoja 1))
-- Heap (<)
ab4 = Bin ab1 1 (abHoja 3)
-- ABB completo
ab5 = Bin (Bin (abHoja 1) 2 (abHoja 3)) 4 (Bin (abHoja 5) 6 (abHoja 7))
-- Heap (<)
ab6 = Bin ab1 0 (abHoja 6)
-- ABB
ab7 = Bin (Bin (abHoja 1) 2 (abHoja 4)) 5 (abHoja 7)
-- Heap (<) infinito, probar truncando
ab8 = Bin (mapAB (*2) ab8) 1 (mapAB ((+1) . (*2)) ab8)

ab9 = Bin (Bin (abHoja 1) 2 (abHoja 4)) 5 (Bin (abHoja 3) 7 Nil)


-- Ejercicios

recAB :: b->(AB a->a->AB a->b->b->b)->AB a->b
recAB casonil fbin t = case t of
                              Nil -> casonil
                              Bin i r d -> fbin i r d (rec i) (rec d)           
                              where rec = recAB casonil fbin

foldAB :: b->(b->a->b->b)->AB a->b
foldAB casonil fbin = recAB casonil (\i r d ri rd -> fbin ri r rd)
{-foldAB casonil fbin t = case t of
                              Nil -> casonil
                              Bin i r d -> fbin (rec i) r (rec d)
                              where rec = foldAB casonil fbin-}



mapAB :: (a -> b) -> AB a -> AB b
mapAB f= foldAB Nil (\i r d-> Bin i (f r) d)

nilOCumple :: (a -> a -> Bool) -> a -> AB a -> Bool
nilOCumple f x = foldAB True (\i r d-> f r x)

esABB :: Ord a => AB a -> Bool
esABB = recAB True (\i r d ri rd->  (i==Nil || ((mejorSegunAB (>) i)<=r) ) && ( d==Nil || (r<(mejorSegunAB (<) d)) ) && ri && rd )
                  where mejorSegunAB f (Bin i x d) = foldAB x (\ ri r rd -> if f r ri 
                                                                      then if f rd r 
                                                                           then rd 
                                                                           else r 
                                                                      else if f rd ri 
                                                                            then rd
                                                                            else ri) (Bin i x d)

esHeap :: (a -> a -> Bool)  -> AB a -> Bool
esHeap f = recAB True (\i r d ri rd -> foldr (\x rec -> f r x && rec) True (inorder i ++ (inorder d)) && ri && rd)

cantNodos :: AB a -> Integer
cantNodos = foldAB 0 (\ri r rd -> 1+ri+rd) 

altura :: AB a -> Integer
altura = foldAB 0 (\ ri r rd -> max ri rd + 1)

completo :: AB a -> Bool
completo t = 2^(altura t) - 1 == (cantNodos t)


insertarABB :: Ord a => AB a -> a -> AB a
insertarABB t x = recAB (Bin Nil x Nil) (\i r d ri rd -> if x<=r 
                                                         then Bin ri r d 
                                                         else Bin i r rd) t

insertarHeap :: (a -> a -> Bool) -> AB a -> a -> AB a
insertarHeap f = recAB (\x-> (Bin Nil x Nil)) (\i r d ri rd x -> if f r x then elegirSubarbolParaInsertar r i r d (ri x) (rd x) else elegirSubarbolParaInsertar x i r d (ri r) (rd r)) 
  where elegirSubarbolParaInsertar raiz i r d ri rd = if completo i && (cantNodos i > (cantNodos d) )
                                                      then Bin i raiz rd
                                                      else Bin ri raiz d

{-  where elegirSubarbolParaInsertar raiz i r d ri rd = if not (completo i) && (altura i <= (altura d) ) || (altura i < (altura d) ) || completo (Bin i r d)
                                                      then Bin ri raiz d
                                                      else Bin i raiz rd-}

truncar :: AB a -> Integer -> AB a
truncar = foldAB (const Nil) (\ri r rd n -> if n==0
                                            then Nil
                                            else Bin (ri (n-1)) r (rd (n-1)))

--Ejecución de los tests
main :: IO Counts
main = do runTestTT allTests

allTests = test [
  "ejercicio1" ~: testsEj1,
  "ejercicio2" ~: testsEj2,
  "ejercicio3" ~: testsEj3,
  "ejercicio4" ~: testsEj4,
  "ejercicio5" ~: testsEj5,
  "ejercicio6" ~: testsEj6,
  "ejercicio7" ~: testsEj7
  ]

testsEj1 = test [
  [1,2,4,5,7] ~=? inorder ab7,
  [1,2,3,4,5,6,7] ~=? inorder ab5
  ]
  
testsEj2 = test [
  [5,3,6,1,7] ~=? inorder (mapAB (+1) ab6)
  ]


testsEj3 = test [
  nilOCumple (>) 1 Nil ~=? True,
  nilOCumple (<=) 4 Nil ~=? True,
  nilOCumple (<) 1 ab1 ~=? False, 
  nilOCumple (>) 7 ab1 ~=? False,
  nilOCumple (>) 1 ab1 ~=? True
  ]

testsEj4 = test [
  esABB ab7 ~=? True,
  esABB ab1 ~=? False,
  esABB (Nil::AB Integer) ~=? True,
  esABB ab9 ~=? False,
  esHeap (<) ab7 ~=? False,
  esHeap (<) (truncar ab8 10) ~=? True,
  esHeap (>) ab4 ~=? False,
  esHeap (>) (Nil::AB Integer) ~=? True
  ]

testsEj5 = test [
  completo Nil ~=? True,
  completo ab2 ~=? True,
  completo ab4 ~=? False,
  completo (truncar a (altura a - 1)) ~=? True

  ]
    where a=foldl (insertarHeap (<)) Nil [5,3,6,1,7]

testsEj6 = test [
  True ~=? esHeap (<) (insertarHeap (<) (insertarHeap (<) ab6 3) 1),
  True ~=? esABB (insertarABB (insertarABB ab7 6) 9)
  ]

testsEj7 = test [
  [8,4,12,2,10,6,14,1,9,5,13,3,11,7,15] ~=? inorder (truncar ab8 4),
  True ~=? esHeap (<) (truncar ab8 5)
  ]
