import numpy as np


def kepler2ecef(
    tk,
    toe,
    sqrt_a,
    delta_n,
    m0,
    e,
    omega0,
    omega_dot,
    i0,
    idot,
    omega,
    cus,
    cuc,
    crs,
    crc,
    cis,
    cic,
    **kwargs
):
    GM = 3.986004418e14  # [m^3 s^-2]   Mean anomaly at tk
    omega_e = 7.2921151467e-5  # [rad s^-1]  Mean angular velocity of Earth
    A = sqrt_a**2
    n = np.sqrt(GM / A**3) + delta_n  # corrected mean motion

    M0 = m0  # Mean Anomaly
    Mk = M0 + n * tk  # Mean Anomaly
    Ek = Mk
    e = e
    for i in range(3):
        Ek = Mk + e * np.sin(Ek)
    nuk = np.arctan2(np.sqrt(1 - e**2) * np.sin(Ek), np.cos(Ek) - e)
    phik = nuk + omega
    duk = cuc * np.cos(2 * phik) + cus * np.sin(2 * phik)
    drk = crc * np.cos(2 * phik) + crs * np.sin(2 * phik)
    dik = cic * np.cos(2 * phik) + cis * np.sin(2 * phik)
    uk = phik + duk
    rk = A * (1 - e * np.cos(Ek)) + drk
    ik = i0 + idot * tk + dik
    xkm = rk * np.cos(uk)
    ykm = rk * np.sin(uk)
    omegak = omega0 + (omega_dot - omega_e) * tk - omega_e * toe
    x = xkm * np.cos(omegak) - ykm * np.sin(omegak) * np.cos(ik)
    y = xkm * np.sin(omegak) + ykm * np.cos(omegak) * np.cos(ik)
    z = ykm * np.sin(ik)
    return toe + tk, x, y, z
