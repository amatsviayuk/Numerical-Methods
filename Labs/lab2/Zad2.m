function Zad2
    r_max = 2;
    n_max = 200;
    a = 4;
    [circles, index_number, circle_areas] = generate_circles(a, r_max, n_max);
end

function [circles, index_number, circle_areas] = generate_circles(a, r_max, n_max)
    index_number = 191550; % numer Twojego indeksu
    L1 = 0;
    L2 = 5;
    circle_areas = [];
    areas = [];
    circles = zeros(n_max, 3); 
    
    iter = 1;
    while iter <= n_max
        R = rand() * r_max;
        X = (a - 2 * R) * rand() + R;
        Y = (a - 2 * R) * rand() + R;
        
        % intersects?
        if X - R < 0 || X + R > a || Y - R < 0 || Y + R > a
            continue; % if no
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
            circles(iter, :) = [X, Y, R]; 
            areas = [areas, R*R*pi]; % Calculate and store the area of the circle
            circle_areas = cumsum(areas)'; % Cumulative sum of circle areas
            iter = iter + 1;
        end
    end
end

