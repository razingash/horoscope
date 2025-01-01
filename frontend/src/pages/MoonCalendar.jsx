import React, {useEffect, useState} from 'react';
import './../styles/moon.css'

const MoonCalendar = () => {
    const [days, setDays] = useState([]);
    const [month, setMonth] = useState(null);
    const [year, setYear] = useState(null);

    /*возможно стоит объединить два хука в один*/
    useEffect(() => {
        const currentDate = new Date();
        const currentYear = currentDate.getFullYear();
        const currentMonth = currentDate.getMonth() + 1;
        setYear(currentYear);
        setMonth(currentMonth);

    }, [])

    useEffect(() => { /*вроде есть лучший способ получить правильный день недели*/
        if (year && month) {
            const firstDayOfMonth = new Date(year, month - 1, 1).getDay();
            const correctedFirstDay = firstDayOfMonth === 0 ? 6 : firstDayOfMonth - 1;
            const daysInMonth = new Date(year, month, 0).getDate();

            const calendarDays = [
                ...Array(correctedFirstDay ).fill(null),
                ...Array.from({ length: daysInMonth }, (_, i) => i + 1),
            ]

            const totalCells = calendarDays.length < 35 ? 35 : Math.ceil(calendarDays.length / 7) * 7;
            const neededCells = totalCells - calendarDays.length;

            setDays([...calendarDays, ...Array(neededCells).fill(null)]);
        }
    }, [year, month])

    const handlePreviousMonth = () => {
        if (month === 1) {
            if (year >= 2020) {
                setYear(year - 1);
                setMonth(12);
            }
        } else {
            setMonth(month - 1);
        }
    }

    const handleNextMonth = () => {
        if (month === 12) {
            if (year <= 2030) {
                setYear(year + 1);
                setMonth(1);
            }
        } else {
            setMonth(month + 1);
        }
    }


    return (
        <div className={"section__main"}>
            <h1 className={"testing__h1"}>
                <div>Moon Calendar for {year}-{month}</div>
                <div className={"testing__switching"}>
                    <div onClick={handlePreviousMonth}>previous</div>
                    <div onClick={handleNextMonth}>next</div>
                </div>
            </h1>
            <div className={"area__calendar"}>
                <div className={"field__moon_calendar"}>
                    <div className={"calendar__header"}>
                        <div className={"calendar__header__item"}>Mon</div>
                        <div className={"calendar__header__item"}>Tue</div>
                        <div className={"calendar__header__item"}>Wed</div>
                        <div className={"calendar__header__item"}>Thu</div>
                        <div className={"calendar__header__item"}>Fri</div>
                        <div className={"calendar__header__item"}>Sat</div>
                        <div className={"calendar__header__item"}>Sun</div>
                    </div>
                    {days.map((day, index) => (
                        <div className={"calendar__cell"} key={index}>{day ?? ''}</div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default MoonCalendar;