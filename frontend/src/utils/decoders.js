/*функции для переводов ключевых данных по типу заголовка(в конце сделать)*/

export const decodeMoonPhase = (num) => {
    const data = {
        1: "New Moon", 2 : "Waxing Crescent", 3: "First Quarter", 4: "Waxing Gibbous",
        5: "Full Moon",  6: "Waning Gibbous", 7: "Last Quarter", 8: "Waning Crescent"
    }
    return data[num];
}

export const decodeMoonEvent = (num) => {
    const data = {
        1: "Blue Moon", 2: "Micro Moon", 3: "Super Moon", 4: "Wolf Moon"
    }
    return data[num]
}
