function Zad4()
r_max = 2;
n_max = 200;
a = 10;
[circles, index_number, circle_areas, rand_counts, counts_mean] = generate_circles(a, r_max, n_max);
end

function [circles, index_number, circle_areas, rand_counts, counts_mean] = generate_circles(a, r_max, n_max)
    index_number = 191550; % numer Twojego indeksu
    L1 = 0;
    L2 = 5;
    circle_areas = [];
    areas = [];
    circles = zeros(n_max, 3); 
    rand_counts = []; % rand cnt array
    counts_mean = []; % avg rand array
    rand_count = 0; % rand cnt
    iter = 1;
    while iter <= n_max
        rand_count = rand_count + 1;
        R = rand() * r_max;
        X = (a - 2 * R) * rand() + R;
        Y = (a - 2 * R) * rand() + R;

        if X - R < 0 || X + R > a || Y - R < 0 || Y + R > a
            continue; 
        end
        
        isInter = false;
        
        for j = 1:size(circles, 1)
            r1 = circles(j, 3);
            x1 = circles(j, 1);
            y1 = circles(j, 2);
    
            dis = sqrt((X - x1)^2 + (Y - y1)^2);
            
            if dis < r1 + R
                isInter = true;
                break;
            end
        end
        
        if ~isInter
            circles(iter, :) = [X, Y, R]; % Dodanie nowego koła do macierzy circles
            areas = [areas, R*R*pi];
            circle_areas = cumsum(areas)';
            rand_counts = [rand_counts; rand_count]; % [iter] -> array
            counts_mean = [counts_mean; mean(rand_counts, 'all')]; % array_push.back(avg(all))
            iter = iter + 1;
        end
    end
end







