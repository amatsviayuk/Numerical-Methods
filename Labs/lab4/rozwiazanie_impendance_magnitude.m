function rozwiazanie_impendance_magnitude
    a = 1;
    b = 50;
    ytolerance = 1e-12;
    max_iterations = 100;
    
    [omega_bisection, ~, ~, xtab_bisection, xdif_bisection] = bisection_method(a, b, max_iterations, ytolerance, @impedance_magnitude);
    [omega_secant, ~, ~, xtab_secant, xdif_secant] = secant_method(a, b, max_iterations, ytolerance, @impedance_magnitude);
    
    figure;
    subplot(2,1,1); % upper chart
    plot(xtab_bisection, '-o', 'DisplayName', 'Bisekcja');
    hold on;
    plot(xtab_secant, '-x', 'DisplayName', 'Sieczne');

    xlabel('Iteracje');
    ylabel('Wartość xsolution');
    title('Zmiany w kolejnych iteracjach');
    legend('Location', 'best');
    
    subplot(2,1,2);
    semilogy(xdif_bisection, '-o', 'DisplayName', 'Bisekcja');
    hold on;
    semilogy(xdif_secant, '-x', 'DisplayName', 'Sieczne');

    xlabel('Iteracje');
    ylabel('Wartość xdif');
    title('Różnice w kolejnych iteracjach');
    legend('Location', 'best');

end

function [xsolution,ysolution,iterations,xtab,xdif] = secant_method(a,b,max_iterations,ytolerance,fun)
    % a - lewa granica przedziału poszukiwań miejsca zerowego (x0=a)
    % b - prawa granica przedziału poszukiwań miejsca zerowego (x1=b)
    % max_iterations - maksymalna liczba iteracji działania metody siecznych
    % ytolerance - wartość abs(fun(xsolution)) powinna być mniejsza niż ytolerance
    % fun - nazwa funkcji, której miejsce zerowe będzie wyznaczane
    %
    % xsolution - obliczone miejsce zerowe
    % ysolution - wartość fun(xsolution)
    % iterations - liczba iteracji wykonana w celu wyznaczenia xsolution
    % xtab - wektor z kolejnymi kandydatami na miejsce zerowe, począwszy od x2
    % xdiff - wektor wartości bezwzględnych z różnic pomiędzy i-tym oraz (i+1)-ym elementem wektora xtab; xdiff(1) = abs(xtab(2)-xtab(1));
    
    xsolution = [];
    ysolution = [];
    iterations = [];
    xtab = [];
    xdif = [];

    format long
    func = @(x) x.^2 - 4.01;
    a = 0;
    b = 4;
    max_iterations = 100;
    ytolerance = 1e-12;    
    iter = 0;
    while 1
        iter = iter + 1;
        c = b - ((func(b) * (b - a)) / (func(b) - func(a))); % formula 6
    
        xtab = [xtab; c];
        [r, t] = size(xtab);
        
        if r >= 2
            xdif = [xdif; abs(xtab(r, 1) - xtab(r - 1, 1))]; % r,r-1 column difference --> xdif
        end
        
        if abs(func(c)) < ytolerance || iter == max_iterations
            xsolution = [xsolution, c];
            ysolution = [ysolution, func(c)];
    
            iterations = [iterations, iter];
            iter = 0;
            break;
        end
        
        a = b; % shift
        b = c;
    end

end

function impedance_delta = impedance_magnitude(omega)
omega = 10;
if omega <= 0
    error("Podano zlą omegę");
end
R = 525;
C = 7 * 10^(-5);
L = 3;
M = 75; % docelowa wartość modułu impedancji

mianL = 1 / R^2;
mianPL = omega * C;
mianPP = 1 / (omega * L);

Z_mian = (mianL + (mianPL - mianPP)^2)^0.5;
Z = 1 / Z_mian;

impedance_delta = Z - M;

end

function [xsolution,ysolution,iterations,xtab,xdif] = bisection_method(a,b,max_iterations,ytolerance,fun)
% a - lewa granica przedziału poszukiwań miejsca zerowego
% b - prawa granica przedziału poszukiwań miejsca zerowego
% max_iterations - maksymalna liczba iteracji działania metody bisekcji
% ytolerance - wartość abs(fun(xsolution)) powinna być mniejsza niż ytolerance
% fun - nazwa funkcji, której miejsce zerowe będzie wyznaczane
%
% xsolution - obliczone miejsce zerowe
% ysolution - wartość fun(xsolution)
% iterations - liczba iteracji wykonana w celu wyznaczenia xsolution
% xtab - wektor z kolejnymi kandydatami na miejsce zerowe, począwszy od xtab(1)= (a+b)/2
% xdiff - wektor wartości bezwzględnych z różnic pomiędzy i-tym oraz (i+1)-ym elementem wektora xtab; xdiff(1) = abs(xtab(2)-xtab(1));

xsolution = [];
ysolution = [];
iterations = [];
xtab = [];
xdif = [];

func = @(x) x.^2 - 4.01;
a = 0;
b = 4;
max_iterations = 100;
ytolerance = 1e-12;
iter = 0;
while 1
    iter = iter + 1;
    c = (a + b) / 2;
    xtab = [xtab; c];
    [r, t] = size(xtab);

    if r >= 2
        xdif = [xdif; abs(xtab(r, 1) - xtab(r - 1, 1))];
    end

    if abs(func(c)) < ytolerance
        xsolution = [xsolution, c];
        ysolution = [ysolution, func(c)];
        iterations = [iterations, iter];
        iter = 0;
        break;
    elseif func(a) * func(c) < 0
        b = c;
    else
        a = c;
    end

    if iter == max_iterations
        break
    end
end
end