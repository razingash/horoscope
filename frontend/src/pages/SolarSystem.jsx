import React, {useEffect, useState} from 'react';
import "../styles/solar_system.css"
import {useFetching} from "../hooks/useFetching";
import SolarSystemService from "../API/SolarSystemService";

const SolarSystem = () => {
    const [planetPositions, setPlanetPositions] = useState([]);
    const [fetchSolarSystemMap, isMapLoading, mapError] = useFetching(async () => {
        return await SolarSystemService.getSolarSystemForecast();
    })

    const planetsData = [
        {num: 10, radius: 95},
        {num: 9, radius: 85},
        {num: 8, radius: 75},
        {num: 7, radius: 65},
        {num: 6, radius: 55},
        {num: 5, radius: 45},
        {num: 4, radius: 35}, /*могут быть казусы из-за того что в skyfield 4 это луна, а я использую 4 для земли*/
        {num: 3, radius: 25},
        {num: 2, radius: 15},
    ];

    useEffect(() => {
        const loadData = async () => {
            if (!isMapLoading && !mapError) {
                const data = await fetchSolarSystemMap();
                if (data) {
                    const newPositions = planetsData.map((planet) => {
                        const angleDeg = data[planet.num];
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

    return (
        <div className={"section__main"}>
            <h1>Solar System Now</h1>
            <div className={"area__solar_system"}>
                <div className={"field__solar_system"}>
                    <svg className={"svg__solar_system"} viewBox={"0 0 200 200"}>
                        {planetsData.map((planet) => (
                            <circle key={planet.num} className="spinner__stroke" cx="100" cy="100" r={planet.radius}/>
                        ))}
                        <circle className="planet__sun" cx="100" cy="100" r="7"></circle>

                        {planetPositions.map((planet) => (
                            <circle key={planet.num} className={`planet`} cx={planet.x} cy={planet.y} r="3" fill="white"/>
                        ))}
                    </svg>
                </div>
            </div>
        </div>
    );
};

export default SolarSystem;
