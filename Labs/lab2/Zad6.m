function Zad1()
[numer_indeksu, Edges, I, B, A, b, r] = page_rank()
end

function [numer_indeksu, Edges, I, B, A, b, r] = page_rank()
numer_indeksu = 191550;
L1 = 5;
L2 = 5;
N = 8;

Edges = [1,1,2,2,2,3,3,3,4,4,5,5,6,6,7,8, 5+1;
         4,6,3,4,5,5,6,7,5,6,4,6,4,7,6,5+1,8];
d=0.85;
I = [];
B = [];
A = [];
b = [];
r = [];
I = speye(8); % matrix of '1'
B = sparse(Edges(2,:),Edges(1,:),1,N,N); % macierz rzadka na podstawie liczby krawedzi  

L = sum(B);
L = 1 ./ L; % diag mac rz
A = spdiags(L(:), 0, numel(L), numel(L)); % calculating A matrix

    b = [];
    for i = 1:N
        b = [b; (1 - d) / N]; 
    end
    M = I - d * B * A;
    r = lsqr(M, b); %oblicza wektor rangi r
end