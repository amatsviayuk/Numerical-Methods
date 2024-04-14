function [A,b,M,bm,x,err_norm,time,iterations,index_number] = solve_Gauss_Seidel(N)
% SOLVE_GAUSS_SEIDEL solves a linear system using the Gauss-Seidel iterative method.
    % N - size of the matrix
    % A - coefficient matrix of the linear system
    % b - right-hand side vector of the linear system
    % M - auxiliary matrix defined in the Gauss-Seidel method
    % bm - auxiliary vector defined in the Gauss-Seidel method
    % x - solution vector
    % err_norm - norm of the residual error: err_norm = norm(A*x-b)
    % time - time taken to compute the solution
    % iterations - number of iterations performed
    % index_number - your index number
    
    index_number = 191550;
    L1 = 0;
    [A,b] = generate_matrix(N, L1); % coefficient matrix A
    
    L = tril(A, -1); % Lower part of A
    U = triu(A, 1); % Upper part of A
    D = diag(diag(A)); % Diagonal of A
    
    x = ones(N, 1);
    I = eye(size(D)); % Identity matrix
    inv_DpL = (D + L) \ I; % Inverse of (D + L)
    M = -inv_DpL * U;
    bm = inv_DpL * b;
    
    iterations = -1; % cnt
    err_norm = 1;
    tic; % Start timing
    
    while err_norm >= 10^-12 && iterations < 1000 % Loop until convergence
        iterations = iterations + 1;
        err_norm = norm(A*x-b);
        x = M * x + bm; % Update solution with Gauss-Seidel formula
    end
    
    time = toc; % Stop timing
end