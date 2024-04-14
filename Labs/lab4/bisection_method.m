function [xsolution,ysolution,iterations,xtab,xdif] = bisection_method(a,b,max_iterations,ytolerance,func)
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