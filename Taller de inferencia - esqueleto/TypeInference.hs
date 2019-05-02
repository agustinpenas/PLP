module TypeInference (TypingJudgment, Result(..), inferType)

where

import Data.List(intersect)
import Exp
import Type
import Unification

------------
-- Errors --
------------
data Result a = OK a | Error String


--------------------
-- Type Inference --
--------------------
type TypingJudgment = (Env, AnnotExp, Type)


inferType :: PlainExp -> Result TypingJudgment
inferType e = case infer' e 0 of
    OK (_, tj) -> OK tj
    Error s -> Error s


infer' :: PlainExp -> Int -> Result (Int, TypingJudgment)

-- COMPLETAR DESDE AQUI

infer' (VarExp x)     n = OK ( n+1, (extendE emptyEnv x (TVar n) , VarExp x , TVar n) )

infer' (ZeroExp) n = OK (n, (emptyEnv, ZeroExp, TNat))

infer' (LamExp x () e) n = case infer' e n of 
							OK (n1, ( cntx', e', t')) ->  (if elem x (domainE cntx')
															then OK (n1 , (removeE cntx' x, LamExp x (evalE cntx' x) e', TFun (evalE cntx' x) t' ))
															else OK (n1+1 , (removeE cntx' x, LamExp x (TVar n1) e', TFun (TVar n1) t' )) )
							Error s -> Error s

infer' (AppExp x y) n = case infer' x n of
							OK (n1, ( cntx', x', tx')) ->  case infer' y n1 of
																OK (n2, ( cnty', y', ty')) -> case mgu ( (tx',TFun ty' (TVar n2) ):listaDeVariablesCompartidas cntx' cnty' (domainE cntx') (domainE cnty') ) of
																																									UOK subst -> OK (n2+1, (
																																															joinE [subst <.> cntx', subst <.> cnty'],
																																															subst <.> AppExp x' y',
																																															subst <.> (TVar n2) ))
																																									UError a b -> uError a b
																Error s -> Error s	
							Error s -> Error s			
	where 	listaDeVariablesCompartidas a b c = foldr (\x rec -> if elem x c then  (evalE a x, evalE b x):rec else rec) []
--------------------------------
-- YAPA: Error de unificacion --
--------------------------------
uError :: Type -> Type -> Result (Int, a)
uError t1 t2 = Error $ "Cannot unify " ++ show t1 ++ " and " ++ show t2
