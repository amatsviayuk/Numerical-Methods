function impedance_delta = impedance_magnitude(omega)
omega = 10
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