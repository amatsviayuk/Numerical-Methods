function [A,b,M,bm,x,err_norm,time,iterations,index_number] = solve_Jacobi(N)
    % SOLVE_JACOBI solves a linear system using the Jacobi iterative method.
    % N - size of the matrix
    % A - coefficient matrix of the linear system
    % b - right-hand side vector of the linear system
    % M - auxiliary matrix defined in the Jacobi method
    % bm - auxiliary vector defined in the Jacobi method
    % x - solution vector
    % err_norm - norm of the residual error: err_norm = norm(A*x-b)
    % time - time taken to compute the solution
    % iterations - number of iterations performed
    % index_number - your index number
    
    index_number = 191550;
    L1 = 0; 
    [A,b] = generate_matrix(N, L1); % coefficient matrix A and right-hand side vector b
    
    x = ones(N, 1);
    M = -diag(diag(A)) \ (tril(A, -1) + triu(A, 1));
    bm = diag(diag(A)) \ b;
    
    tic; % Start timing
    max_iterations = 1000;
    tolerance = 1e-12; % Tolerance for convergence
    for iterations = 1:max_iterations
        x_old = x; % Store previous solution
        x = M * x_old + bm; % Update solution using Jacobi formula
        err_norm = norm(A*x-b); % Compute the norm of the residual error
        if err_norm < tolerance % Check for convergence
            break;
        end
    end
    time = toc; % Stop timing

end
