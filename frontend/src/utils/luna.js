/*добавить функцию для расчета времени в текущей временной зоны относительно UTC для MoonCalendar.jsx*/

const PI = Math.PI;

export const generateShadowPath = (phase, r=50) => {
    const angle = (phase * PI) / 180;
    const f = Math.cos(angle);
    let pathData = "";
    if (phase <= 180) {
        for (let i = 0; i <= 360; i++) {
            const cosi = Math.cos(i * PI / 180);
            let x = cosi > 0 ? f * r * cosi + 50 : r * cosi + 50;
            let y = r * Math.sin(i * PI / 180) + 50;
            pathData += (i === 0 ? "M" : "L") + x + "," + y + " ";
        }
    } else {
        for (let i = 0; i <= 360; i++) {
            const cosi = Math.cos(i * PI / 180);
            let x = cosi < 0 ? f * r * cosi + 50 : r * cosi + 50;
            let y = r * Math.sin(i * PI / 180) + 50;
            pathData += (i === 0 ? "M" : "L") + x + "," + y + " ";
        }
    }
    return pathData;
};

export const calculateMoonIlluminationPercent = (dt) => {
    /*функция для расчета освещенности(Видимости) луны в зависимости от времени*/
    let T = (toJulianDay(dt) - 2451545.0) / 36525.0;

    let T2 = T * T;
    // лунные параметры
    let F = (93.2721 + 483202.0 * T - 0.003403 * T2 - T * T2 / 3526000) * 0.0174533;
    let L1 = (218.316 + 481268.0 * T) * 0.0174533;
    let M1 = (134.963 + 477199.0 * T + 0.008997 * T2 + T2 / 69700) * 0.0174533;
    let D2 = (297.85 + 445267.0 * T - 0.00163 * T2 + T2 / 545900) * 2 * 0.0174533;

    let [LAM0, R] = sunPosition(T, T2); // долгота Солнца и расстояние Земля-Солнце

    // лунное расстояние
    let SUMR = -20954 * Math.cos(M1) - 3699 * Math.cos(D2 - M1) - 2956 * Math.cos(D2);
    let DR = 385000 + SUMR;

    // геоцентрическая широта
    let B = 5.128 * Math.sin(F) + 0.2806 * Math.sin(M1 + F) + 0.2777 * Math.sin(M1 - F) + 0.1732 * Math.sin(D2 - F);
    let SUML = 6.289 * Math.sin(M1) + 1.274 * Math.sin(D2 - M1) + 0.6583 * Math.sin(D2) +
               0.2136 * Math.sin(2 * M1) - 0.1851 * Math.sin(0) - 0.1143 * Math.sin(2 * F);
    let LAM = L1 + SUML * 0.0174533;

    // получение освещенной стороны луны
    let TEMP = Math.cos(B * 0.0174533) * Math.cos(LAM - LAM0 * 0.0174533);
    let PSI = Math.acos(TEMP);
    let NUM = R * Math.sin(PSI);
    let DEN = DR - R * TEMP;
    let I = Math.atan(NUM / DEN);
    if (NUM * DEN < 0) {
        I = I + PI;
    }
    if (NUM < 0) {
        I = I + PI;
    }

    return (100 * (1 + Math.cos(I)) / 2).toFixed(2);
}

const sunPosition = (T, T2) => {
    // Вычисления для долготы Солнца и его расстояния от Земли
    let L = 280.466 + 36000.8 * T;
    let M = 357.529 + 35999 * T - 0.0001536 * T2 + T2 / 24490000;
    M = M * 0.0174533;

    let C = (1.915 - 0.004817 * T - 0.000014 * T2) * Math.sin(M) +
        (0.01999 - 0.000101 * T) * Math.sin(2 * M) + 0.00029 * Math.sin(3 * M);
    let V = M + C * 0.0174533;
    let E = 0.01671 - 0.00004204 * T - 0.0000001236 * T2;
    let R = 1.00072 / (1 + E * Math.cos(V)) * 145980000;
    let THETA = L + C;
    let OM = 125.04 - 1934.1 * T;
    let LAM0 = THETA - 0.00569 - 0.00478 * Math.sin(OM * 0.0174533);

    return [LAM0, R];
}

const toJulianDay = (dt) => {
    return 367 * dt.getFullYear()
        - Math.floor((7 * (dt.getFullYear() + Math.floor((dt.getMonth() + 9) / 12))) / 4)
        + Math.floor((275 * (dt.getMonth() + 1)) / 9) + dt.getDate() + 1721013.5
        + (dt.getHours() + dt.getMinutes() / 60 + dt.getSeconds() / 3600) / 24;
};
