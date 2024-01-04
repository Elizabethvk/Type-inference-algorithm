:-use_module(library(clpfd)).
:-use_module(library(lists)).

:- op(1105, xfy, &).
:- op(1105, xfy, $).

is_type(int).
is_type(bool).
is_type(A -> B) :- is_type(A), is_type(B).

% https://davidchristiansen.dk/tutorials/bidirectional.pdf

% Co-product types? AType + BType
% For the if

% infer_type(Gamma, Term, Type).
% From the context
infer_type(Gamma, X, Type) :- member([X, Type], Gamma).

infer_type(_, yes, bool). % constant
infer_type(_, no, bool). % constant
infer_type(Gamma, A | B, bool) :- 
    infer_type(Gamma, A, bool),
    infer_type(Gamma, B, bool).
infer_type(Gamma, A & B, bool) :- 
    infer_type(Gamma, A, bool),
    infer_type(Gamma, B, bool).
infer_type(Gamma, -A, bool) :- 
    infer_type(Gamma, A, bool).

infer_type(_, X, int) :- integer(X). % constant
infer_type(Gamma, X + Y, int) :- 
    infer_type(Gamma, X, int),
    infer_type(Gamma, Y, int).
infer_type(Gamma, X - Y, int) :- 
    infer_type(Gamma, X, int),
    infer_type(Gamma, Y, int).
infer_type(Gamma, X * Y, int) :- 
    infer_type(Gamma, X, int),
    infer_type(Gamma, Y, int).
infer_type(Gamma, X ^ Y, int) :- 
    infer_type(Gamma, X, int),
    infer_type(Gamma, Y, int).

infer_type(Gamma, X == Y, bool) :- 
    infer_type(Gamma, X, int),
    infer_type(Gamma, Y, int).
infer_type(Gamma, X < Y, bool) :- 
    infer_type(Gamma, X, int),
    infer_type(Gamma, Y, int).
infer_type(Gamma, X > Y, bool) :- 
    infer_type(Gamma, X, int),
    infer_type(Gamma, Y, int).

infer_type(Gamma, X : T, T) :- check_type(Gamma, X, T).

infer_type(Gamma, F $ X, B) :-
    check_type(Gamma, X, A),
    infer_type(Gamma, F, A -> B).

check_type(Gamma, X, T) :- infer_type(Gamma, X, T). 
check_type(Gamma, Cond -> A ; B, T) :-
    check_type(Gamma, Cond, bool),
    check_type(Gamma, A, T),
    check_type(Gamma, B, T).
check_type(Gamma, lambda([X, A], Body), A -> B) :-
    is_type(A),
    append([[X, A]], Gamma, ExtendedGamma),
    check_type(ExtendedGamma, Body, B).


% infer_type(Gamma, Cond -> A ; B, Type) :-
%     infer_type(Gamma, Cond, bool),
%     infer_type(Gamma, A, Type),
%     infer_type(Gamma, B, Type).
% 
% infer_type(Gamma, F $ X, Type) :-
%     infer_type(Gamma, X, A),
%     infer_type(Gamma, F, A -> Type).
% 
% infer_type(Gamma, lambda(X, Body), A -> B) :- 
%     infer_type(Gamma, X, A),
%     append([X, A], Gamma, ExtendedGamma),
% 	  infer_type(ExtendedGamma, Body, B).

% 
% ?- infer_type([], 3 == 5, T)
% 
% ?- infer_type([x, int], x == 0 -> 0 ; (x == 1 -> 1 ; x), T )
% 
% ?- infer_type(
%               [
%               [f : bool -> bool], 
%               [g : bool -> bool]], 
%               lambda(b : bool, 
%                      f $ (g $ b)),
%               T)
%               
% ?- omega = lambda([x, A], x $ x),infer_type([], Omega, X).
% 
