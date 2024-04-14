function Zad2
    N = 1000:1000:8000;
    vtime_direct = ones(1,length(N)); 
    for i = 1:length(N)
        [~, ~, ~, time_direct, ~, ~] = solve_direct(N(i)); % getting time_direct for each element
        vtime_direct(i) = time_direct; % czas wyznaczenia rozwiazania
    end
    plot_direct(N, vtime_direct);
end

function plot_direct(N,vtime_direct)
    % N - wektor zawierający rozmiary macierzy dla których zmierzono czas obliczeń metody bezpośredniej
    % vtime_direct - czas obliczeń metody bezpośredniej dla kolejnych wartości N
    figure; % new chart
    plot(N, vtime_direct, '-o', 'LineWidth', 2);
    title('Czas rozwiazania');
    xlabel('Matrix size ');
    ylabel('Time ');
    grid on; % net
    print -dpng zadanie2.png;
end

function [A,b,x,time_direct,err_norm,index_number] = solve_direct(N)
% A - macierz z równania macierzowego A * x = b
% b - wektor prawej strony równania macierzowego A * x = b
% x - rozwiązanie równania macierzowego
% time_direct - czas wyznaczenia rozwiązania x
% err_norm - norma błędu rezydualnego rozwiązania x; err_norm = norm(A*x-b);
% index_number - Twój numer indeksu
index_number = 191550;
L1 = 0;

[A,b] = generate_matrix(N, L1);

tic;
x = A\b;
time_direct = toc;
err_norm = norm(A*x-b);
end