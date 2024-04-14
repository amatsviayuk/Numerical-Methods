function Zad5
N = 1000:1000:8000;
n = length(N);
time_Jacobi = ones(1,n);
time_Gauss_Seidel = 2*ones(1,n);
iterations_Jacobi = 40*ones(1,n);
iterations_Gauss_Seidel = 40*ones(1,n);
for i = 1:n
    [A,b,M,bm,x,err_norm,time,iterations,index_number] = solve_Jacobi(N(i));
    iterations_Jacobi(i) = iterations; % pasting new values
    time_Jacobi(i) = time;
    [A,b,M,bm,x,err_norm,time,iterations,index_number] = solve_Gauss_Seidel(N(i));
    iterations_Gauss_Seidel(i) = iterations;
    time_Gauss_Seidel(i) = time;

end
plot_problem_5(N,time_Jacobi,time_Gauss_Seidel,iterations_Jacobi,iterations_Gauss_Seidel);
end

function plot_problem_5(N, time_Jacobi, time_Gauss_Seidel, iterations_Jacobi, iterations_Gauss_Seidel)
    subplot(2, 1, 1);
    plot(N, time_Jacobi, 'b-', N, time_Gauss_Seidel, 'r-');
    title('Czas obliczeń dla metody Jacobiego i Gaussa-Seidla');
    xlabel('Rozmiar macierzy N');
    ylabel('Czas s');
    legend('Jacobi', 'Gauss-Seidel', 'Location', 'eastoutside');
    grid on;

    subplot(2, 1, 2);
    bar_data = [iterations_Jacobi', iterations_Gauss_Seidel'];
    bar(N, bar_data);
    title('Liczba iteracji dla metody Jacobi i Gaussa-Seidla');
    xlabel('Rozmiar macierzy N');
    ylabel('Liczba iteracji');
    legend('Jacobi', 'Gauss-Seidel', 'Location', 'eastoutside');
    grid on;

    saveas(gcf, 'zadanie5.png');
end