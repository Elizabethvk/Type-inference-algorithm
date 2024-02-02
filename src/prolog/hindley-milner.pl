:- op(600, yfx, '@').  % Function application
:- op(450, xfy, '=>'). % Type variable quantification

% Defines/validates a typing context.
tcx([]).
tcx([X-Sigma | Tcx]) :-
    atom(X),
    sigma_type(Sigma),
    tcx(Tcx).

% Defines/validates an abstracted ("sigma") type. These are often called "type
% schemes".
sigma_type(Vs=>Tau) :-
    set_of_vars(Vs),
    tau_type(Tau).

% Defines/validates a set of variables.
set_of_vars([]).
set_of_vars([V | Vs]) :-
    var(V),
    maplist(\==(V), Vs),
    set_of_vars(Vs).

% Defines/validates a simple ("tau") type.
tau_type(A->B) :-
    tau_type(A),
    tau_type(B).
tau_type(tuple(Ts)) :-
    maplist(tau_type, Ts).
tau_type(Constructor) :-
    Constructor =.. [Name | Args],
    length(Args, Arity),
    type_constructor(Name/Arity),
    maplist(tau_type, Args).
tau_type(V) :- var(V). % An Inference/Generic Variable.

type_constructor(nat/0).
type_constructor(bool/0).
type_constructor(list/1).

inference(_Tcx, N, nat) :- integer(N), N >= 0, !.
inference(Tcx, A+B, nat) :-
    !,
    inference(Tcx, A, ATy),
    inference(Tcx, B, BTy),
    ( ATy = nat, BTy = nat -> true
    ; throw(type_check_err('The arguments to `+` must have type nat'(ATy, BTy)))
    ).

inference(_Tcx, true,  bool) :- !.
inference(_Tcx, false, bool) :- !.

inference(_Tcx, [], list(_)) :- !.
inference(Tcx, [Tm | Tms], list(EleTy)) :-
    !,
    inference(Tcx, Tm, EleTy),
    inference(Tcx, Tms, list(TailEleTy)),
    ( EleTy = TailEleTy -> true
    ; throw(type_check_err('You can\'t add an element of type A to a list of type list(B)'(EleTy, TailEleTy)))
    ).

inference(Tcx, tuple(Tms), tuple(Tys)) :-
    !,
    maplist({Tcx}/[E, ETy]>>inference(Tcx, E, ETy), Tms, Tys).

inference(Tcx, X->Body, FreshXTy->BodyTy) :-
    atom(X),
    !,
    % Function parameters are not allowed to have generic types. For example
    % this is not allowed:
    % `fn thing(x: for<T> (T, T)) -> int`
    inference([X-[]=>FreshXTy | Tcx], Body, BodyTy).

inference(Tcx, let(X, Binding, Body), BodyTy) :-
    atom(X),
    !,
    inference(Tcx, Binding, BindingTy),
    generalize(Tcx, BindingTy, BindingScheme),
    inference([X-BindingScheme | Tcx], Body, BodyTy).

inference(Tcx, Fn@Arg, RetTy) :-
    !,
    inference(Tcx, Arg, ArgTy),
    inference(Tcx, Fn, ParamTy->RetTy),
    ( ParamTy = ArgTy -> true
    ; throw(type_check_err('Expected argument of type A, got B'(ParamTy, ArgTy)))
    ).

inference(Tcx, X, Ty) :-
    atom(X),
    !,
    ( member(X-Vs=>Ty0, Tcx) -> instantiate(Vs=>Ty0, Ty)
    ; throw(type_check_err('Unbound variable'(X)))
    ).

instantiate(Vs=>Ty0, Ty) :-
    copy_term(Vs, Ty0, _, Ty).

generalize(Tcx, Ty0, Vs=>Ty) :-
    term_variables(Ty0, TyVars),
    term_variables(Tcx, TcxVars),
    include({TcxVars}/[X]>>maplist(\==(X), TcxVars), TyVars, Vs0),
    copy_term(Vs0=>Ty0, Vs=>Ty).

% inspired from https://gist.github.com/eignnx/fee2484ab11ba6a5900a01674b7a6d5d
