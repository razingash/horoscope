import React, {useEffect, useState} from 'react';
import './../styles/moon.css'
import {calculateMoonIlluminationPercent, generateShadowPath} from "../utils/luna";
import TimeCounter from "../components/TimeCounter";
import {decodeMoonPhase} from "../utils/translations";
import {useFetching} from "../hooks/useFetching";
import LunarService from "../API/LunarService";
import AdditionalTables from "../components/UI/Luna/AdditionalTables";
import {useStore} from "../utils/store";


const MoonCalendar = () => {
    const {language} = useStore();
    const [year, setYear] = useState(null);
    const [currentDate, setCurrentDate] = useState(null);
    const [shadowPath, setShadowPath] = useState(null);
    const [isMoonRising, setIsMoonRising] = useState(null); // later store it in local storage
    const [moonCovering, setMoonCovering] = useState(null);
    const [illuminationPercent, setIlluminationPercent] = useState(null);
    const [lunarPhase, setLunarPhase] = useState(null);
    const [lunarPhases, setLunarPhases] = useState([]);
    const [prevLunarPhase, setPrevLunarPhase] = useState(null);
    const [nextLunarPhase, setNextLunarPhase] = useState(null);
    const [fetchLunarPhases, isLunarPhasesLoading, lunarPhasesError] = useFetching(async() => {
        return await LunarService.getMoonInfoByTimezone(year);
    }, 0, 1000);

    useEffect(() => {
        const loadData = async () => {
            if (!isLunarPhasesLoading && !lunarPhasesError) {
                const data = await fetchLunarPhases();
                if (data) {
                    const transformedPhase = Math.floor((data[0].phase - 1) / 2) + 1;
                    data.unshift(...Array(transformedPhase - 1).fill(''))
                    setLunarPhases(data)
                }
            }
        }
        year && void loadData();
    }, [year])

    useEffect(() => {
        if (lunarPhase) {
            if (lunarPhase - 1 !== -1) {
                const prevPhase = ((lunarPhase - 2 + 8) % 8) + 1;
                const nextPhase = (lunarPhase % 8) + 1;
                setPrevLunarPhase(prevPhase);
                setNextLunarPhase(nextPhase);
            }
        }
    }, [lunarPhase])

    useEffect(() => {
        const currentDate = new Date();
        const currentYear = currentDate.getFullYear();
        setCurrentDate(currentDate);
        setYear(currentYear);
    }, [])

    useEffect(() => {
        moonCovering && setShadowPath(generateShadowPath(moonCovering));
    }, [moonCovering])

    useEffect(() => {
        const date = new Date();
        const illumination = calculateMoonIlluminationPercent(date);
        setIlluminationPercent(illumination);

        if (isMoonRising == null) { // проверить позже этот код, вроде правильно но в фазах может быть баг
            let previousTime = new Date(date.getTime() - 24 * 60 * 60 * 1000);
            const previousIllumination = calculateMoonIlluminationPercent(previousTime);
            if (illumination < previousIllumination) { // "Убывающая Луна Waning"
                setIsMoonRising(false);
                if (illumination < 50) { // Waning Crescent
                    setLunarPhase(8);
                } else { // Waning Gibbous
                    setLunarPhase(6);
                }
            } else { //"Восходящая Луна Waxing"
                setIsMoonRising(true);
                if (lunarPhases.length === 0) {
                    if (illumination > 50) { // Waxing Gibbous
                        setLunarPhase(4);
                    } else { // Waxing Crescent
                        setLunarPhase(2);
                    }
                }
            }
        }

        if (lunarPhases.length > 0) {
            lunarPhases.forEach((phase) => {
                const phaseDate = new Date(phase.datetime);
                if (currentDate.toDateString() === phaseDate.toDateString()) {
                    setLunarPhase(phase.phase);
                }
            });
        }

        if (isMoonRising === true) { // ! скорее всего так все будет правильно(понаблюдать)
            let moonCovering = illumination * 1.8
            setMoonCovering(moonCovering);
        } else if (isMoonRising === false) {
            let moonCovering = illumination * 1.8 + 90
            setMoonCovering(moonCovering);
        }
    }, [isMoonRising, lunarPhases])

    const handlePreviousYear = () => {
        if (year >= 2020) {
            setYear(year - 1);
        }
    }

    const handleNextYear = () => {
        if (year <= 2030) {
            setYear(year + 1);
        }
    }

    return (
        <div className={"section__main"}>
            <div className={"field__moon__illumination"}>
                <svg className={"svg__moon"} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
                    <use xlinkHref={"#moon"}></use>
                    {shadowPath && <path id="moon-shadow" d={shadowPath.toString()} />}
                </svg>
                <div className={"field__moon__description"}>
                    <table>
                        <tbody>
                            <tr>
                                <th>Timezone:</th>
                                <td>{Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC'}</td>
                            </tr>
                            <tr>
                                <th>Current time:</th>
                                <td><TimeCounter/></td>
                            </tr>
                            <tr>
                                <th>Illumination:</th>
                                <td>{illuminationPercent}%</td>
                            </tr>
                            <tr>
                                <th>Phase Type:</th>
                                <td>{decodeMoonPhase(lunarPhase, language)}</td>
                            </tr>
                            <tr>
                                <th>Next Phase:</th>
                                <td>{decodeMoonPhase(nextLunarPhase, language)}</td>
                            </tr>
                            <tr>
                                <th>Previous Phase:</th>
                                <td>{decodeMoonPhase(prevLunarPhase, language)}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <h2 className={"dfw_row_jcc"}>
                <div>Moon Calendar for {year}</div>
                <div className={"switching"}>
                    <div onClick={handlePreviousYear}>previous</div>
                    <div onClick={handleNextYear}>next</div>
                </div>
            </h2>
            <div className={"area__calendar"}>
                <div className={"field__moon_calendar"}>
                    <div className={"calendar__header"}>
                        <div className={"calendar__header__item"}>New Moon</div>
                        <div className={"calendar__header__item"}>First Quarter</div>
                        <div className={"calendar__header__item"}>Full Moon</div>
                        <div className={"calendar__header__item"}>Last Quarter</div>
                    </div>
                    {lunarPhases && lunarPhases.map((dataset, index) => (
                        dataset.datetime ? (
                            <div className={"calendar__cell"} key={index}>{dataset.datetime.slice(5)}</div>
                        ) : (
                             <div className={"calendar__cell cell__invisible"} key={index}>{'00-00 00:00:00'}</div>
                        )
                    ))}
                </div>
            </div>
            <AdditionalTables year={year} data={lunarPhases}/>
        </div>
    );
};

export default MoonCalendar;