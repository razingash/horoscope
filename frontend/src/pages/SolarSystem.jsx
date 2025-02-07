import React, {useEffect, useState} from 'react';
import "../styles/solar_system.css"
import {useFetching} from "../hooks/useFetching";
import SolarSystemService from "../API/SolarSystemService";

const SolarSystem = () => {
    const [planetPositions, setPlanetPositions] = useState([]);
    const [selectedDate, setSelectedDate] = useState(null);
    const [solarSystemData, setSolarSystemData] = useState(null);
    const [fetchSolarSystemMap, isMapLoading, mapError] = useFetching(async () => {
        return await SolarSystemService.getSolarSystemForecast();
    })

    const planetsData = [
        {num: 10, radius: 95, className: "pluto"},
        {num: 9, radius: 85, className: "neptune"},
        {num: 8, radius: 75, className: "uranus"},
        {num: 7, radius: 65, className: "saturn"},
        {num: 6, radius: 55, className: "jupiter"},
        {num: 5, radius: 45, className: "mars"},
        {num: 4, radius: 35, className: "earth"}, /*могут быть казусы из-за того что в skyfield 4 это луна, а я использую 4 для земли*/
        {num: 3, radius: 25, className: "venus"},
        {num: 2, radius: 15, className: "mercury"},
    ];

    const parseDate = (dateString) => new Date(dateString);

    const findNearestDate = (data) => {
        const today = new Date();
        let nearestDate = null;
        let minDiff = Infinity;

        Object.keys(data).forEach((dateString) => {
            const date = parseDate(dateString);
            const diff = Math.abs(today - date);
            if (diff < minDiff) {
                minDiff = diff;
                nearestDate = dateString;
            }
        });

        return nearestDate;
    };

    useEffect(() => {
        const loadData = async () => {
            if (!isMapLoading && !mapError) {
                const data = await fetchSolarSystemMap();
                if (data) {
                    setSolarSystemData(data)
                    const nearestDate = findNearestDate(data);
                    setSelectedDate(nearestDate);
                    const dataForNearestDate = data[nearestDate];

                    const newPositions = planetsData.map((planet) => {
                        const angleDeg = dataForNearestDate[planet.num];
                        const angleRad = angleDeg * (Math.PI / 180);

                        const x = 100 + planet.radius * Math.cos(angleRad);
                        const y = 100 + planet.radius * Math.sin(angleRad);
                        return {...planet, x, y};
                    });

                    setPlanetPositions(newPositions);
                }
            }
        };
        void loadData();
    }, [isMapLoading, mapError]);


    useEffect(() => {
        if (selectedDate && solarSystemData) {
            const dataForSelectedDate = solarSystemData[selectedDate];

            const newPositions = planetsData.map((planet) => {
                const angleDeg = dataForSelectedDate[planet.num];
                const angleRad = angleDeg * (Math.PI / 180);

                const x = 100 + planet.radius * Math.cos(angleRad);
                const y = 100 + planet.radius * Math.sin(angleRad);
                return { ...planet, x, y };
            });

            setPlanetPositions(newPositions);
        }
    }, [selectedDate, solarSystemData]);


    const handlePrevious = () => {
        if (!solarSystemData) return;

        const dates = Object.keys(solarSystemData);
        const currentDateIndex = dates.indexOf(selectedDate);

        if (currentDateIndex > 0) {
            const previousDate = dates[currentDateIndex - 1];
            setSelectedDate(previousDate);
        }
    };

    const handleNext = () => {
        if (!solarSystemData) return;

        const dates = Object.keys(solarSystemData);
        const currentDateIndex = dates.indexOf(selectedDate);

        if (currentDateIndex < dates.length - 1) {
            const nextDate = dates[currentDateIndex + 1];
            setSelectedDate(nextDate);
        }
    };

    return (
        <div className={"section__main"}>
            <h1 className={"dfw_row_jcc"}>
                <div>Solar System for {selectedDate}</div>
                <div className={"switching"}>
                    <div onClick={handlePrevious}>previous</div>
                    <div onClick={handleNext}>next</div>
                </div>
            </h1>
            <div className={"area__solar_system"}>
                <div className={"field__solar_system"}>
                    <svg className={"svg__solar_system"} viewBox={"0 0 200 200"}>
                        {planetsData.map((planet) => (
                            <circle key={planet.num} className="spinner__stroke" cx="100" cy="100" r={planet.radius}/>
                        ))}
                        <circle className="planet__sun" cx="100" cy="100" r="7"></circle>

                        {planetPositions.map((planet) => (
                            <g key={planet.num}>
                            <circle key={planet.num} className={`planet ${planet.className}`} cx={planet.x} cy={planet.y} r="3" fill="white"/>
                            <text x={planet.x + 5} y={planet.y} className="planet_label">{planet.className}</text>
                            </g>
                        ))}
                    </svg>
                </div>
            </div>
        </div>
    );
};

export default SolarSystem;
