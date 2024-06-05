% Facts
parent(homer, bart).
parent(homer, lisa).
parent(homer, maggie).
parent(marge, bart).
parent(marge, lisa).
parent(marge, maggie).
parent(abraham, homer).
parent(mona, homer).
parent(clancy, marge).
parent(jacqueline, marge).

% Rule
grandparent(X, Y) :- parent(X, Z), parent(Z, Y).

