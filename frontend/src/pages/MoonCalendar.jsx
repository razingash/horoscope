import React, {use, useEffect, useState} from 'react';
import './../styles/moon.css'
import {calculateMoonIlluminationPercent} from "../utils/utils";

const MoonCalendar = () => {
    const [days, setDays] = useState([]);
    const [month, setMonth] = useState(null);
    const [year, setYear] = useState(null);
    const rad = Math.PI / 180;

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

    const calculateShadowPath = () => {
        const date = new Date();
        const illuminationPercent = calculateMoonIlluminationPercent(date);

        const phase = 180//180 - (illuminationPercent / 100) * 180;
        const f = Math.cos(phase * rad);

        const shadowLeftX = 50 - f * 25;
        const shadowRightX = Math.abs(f) * 50;

        const shadowTopY = 0;
        const shadowBottomY = 100;
        let leftCurveStrength, rightCurveStrength;

        if (phase < 180) { // waxing
            leftCurveStrength = 20 + (phase / 180) * 20;
            rightCurveStrength = 20;
        } else { // waning
            leftCurveStrength = 20;
            rightCurveStrength = 20 + ((360 - phase) / 180) * 20;
        }

        const oppositeSideShift = phase < 180 ? shadowRightX : shadowLeftX;

        return `
            M 0,50
            Q ${shadowLeftX - leftCurveStrength},${shadowTopY} 50,${shadowTopY}
            Q ${oppositeSideShift  + rightCurveStrength},${shadowTopY} 100,50  
            Q ${oppositeSideShift  + rightCurveStrength},${shadowBottomY} 50,${shadowBottomY}
            Q ${shadowLeftX - leftCurveStrength},${shadowBottomY} 0,50
            Z
        `;
    }

    const updateMoonShadow = (path) => {
        const moonShadow = document.querySelector("#moon-shadow");
        moonShadow.setAttribute("d", path);
    }

    useEffect(() => {
        const shadowPath = calculateShadowPath();
        updateMoonShadow(shadowPath);
    }, [])

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
                <div className={"field__moon__illumination"}>
                    <svg className={"svg__moon"}>
                        <use xlinkHref={"#moon"}></use>
                    </svg>
                </div>
            </div>
        </div>
    );
};

export default MoonCalendar;