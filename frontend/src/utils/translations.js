
/*use only for UI buttons, headers...
decoders are also used to interpret static backend values to save traffic
*/

export const translateZodiacs = (language = "en") => {
    const data = {
        "en": [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ],
        "pl": [
            "Baran", "Byk", "Bliźnięta", "Rak", "Lew", "Panna",
            "Waga", "Skorpion", "Strzelec", "Koziorożec", "Wodnik", "Ryby"
        ],
        "ru": [
            "Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева",
            "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"
        ]
    };

    return data[language];
};

export const decodeMoonPhase = (num, language="en") => {
    const data = {
        "en": {
            1: "New Moon", 2 : "Waxing Crescent", 3: "First Quarter", 4: "Waxing Gibbous",
            5: "Full Moon",  6: "Waning Gibbous", 7: "Last Quarter", 8: "Waning Crescent"
        },
        "pl": {
            1: "Nów", 2 : "Sierp Przybywający", 3: "Pierwsza Kwadra", 4: "Rosnący Garb",
            5: "Pełnia",  6: "Znikający Garb", 7: "Ostatnia Kwadra", 8: "Znikający Sierp"
        },
        "ru": {
            1: "Новолуние", 2 : "Растущий полумесяц", 3: "Первый Квартал", 4: "Растущая луна",
            5: "Полнолуние",  6: "Убывающая Луна", 7: "Последний квартал", 8: "Убывающий полумесяц"
        }
    }
    return data[language][num];
}

export const decodeMoonEvent = (num, language="en") => {
    const data = {
        "en": {1: "Blue Moon", 2: "Micro Moon", 3: "Super Moon", 4: "Wolf Moon"},
        "pl": {1: "Niebieski Księżyc", 2: "Mikroksiężyc", 3: "Superksiężyc", 4: "Wilczy Księżyc"},
        "ru": {1: "Голубая Луна", 2: "Микролуние", 3: "Суперлуние", 4: "Волчья Луна"}
    }
    return data[language][num];
}

export const decodeMonth = (num) => {
    const data = {
        1: "Jan", 2 : "Feb", 3: "Mar", 4: "Apr", 5: "May",  6: "Jun", 7: "Jul",
        8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }
    return data[num]
}
