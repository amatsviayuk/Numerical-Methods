function Zad1()
clear all
close all
format compact
n_max = 200;
a = 100;
r_max = 50;
[circles, index_number] = generate_circles(a, r_max, n_max);
plot_circles(a, circles, index_number); 
print -dpng zadanie1.png 
end

function [circles, index_number] = generate_circles(a, r_max, n_max)
    index_number = 191550; % numer Twojego indeksu
    L1 = 0;
    circles = zeros(n_max, 3); % Inicjalizacja macierzy circles (3 col)
    
    iter = 1;
    while iter <= n_max
        R = rand() * r_max; % Inicjalizacja okregu
        X = (a - 2 * R) * rand() + R;
        Y = (a - 2 * R) * rand() + R;
        isInter = false;
        
        for j = 1:size(circles, 1) 
            r1 = circles(j, 3); % current circle in circles
            x1 = circles(j, 1);
            y1 = circles(j, 2);
    
            dis = sqrt((X - x1)^2 + (Y - y1)^2); % r1 to r2 dist
            
            if dis < r1 + R
                isInter = true;
                break;
            end
        end
        
        if ~isInter
            circles(iter, :) = [X, Y, R]; % Dodanie nowego koła do macierzy circles
            iter = iter + 1;
        end
    end
end

function plot_circles(a, circles, index_number)
axis equal; % X == Y
    axis([0 a 0 a]); % axis limit
     hold on; % draw
    for i = 1:size(circles, 1) 
    plot_circle(circles(i, 3), circles(i, 1), circles(i, 2));
    %pause(0.1);
    end
    hold off;
end








