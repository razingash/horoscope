import React, {useEffect, useState} from 'react';
import './../styles/horoscope.css'
import {useFetching} from "../hooks/useFetching";
import HoroscopeService from "../API/HoroscopeService";
import {useStore} from "../utils/store";

const Horoscope = ({type}) => {
    const {language} = useStore();
    const [zodiacs, setZodiacs] = useState({});
    const [fetchHoroscope, isHoroscopeLoading, horoscopeError] = useFetching(async() => {
        return await fetchHoroscopeByType();
    }, 0, 1000)

    const fetchHoroscopeByType = async () => {
        const rawDate = new Date()
        const date = rawDate.toISOString().split('T')[0] + "T00:00:00Z";
        // eslint-disable-next-line default-case
        switch (type) {
            case 1:
                return await HoroscopeService.getDailyHoroscope(date, language);
            case 2:
                return await HoroscopeService.getWeeklyHoroscope(date, language);
            case 3:
                return await HoroscopeService.getMonthlyHoroscope(date, language);
            case 4:
                return await HoroscopeService.getAnnualHoroscope(date, language);
        }
    }

    useEffect(() => {
        const loadData = async () => {
            if (!isHoroscopeLoading && !horoscopeError) {
                const data = await fetchHoroscope();
                data && setZodiacs(data);
            }
        }
        void loadData();
    }, [type, isHoroscopeLoading, horoscopeError])


    return (
        <div className={"section__main"}>
            <h1>Horoscope</h1>
            <div className={"area__horoscope"}>
                {Object.entries(zodiacs).length > 0 ? (Object.entries(zodiacs).map(([zodiac, description]) => (
                    <div className="field__prediction" key={zodiac}>
                        <hr />
                        <svg className="svg__zodiac">
                            <use xlinkHref={`#zodiac_${zodiac}`} />
                        </svg>
                        <div className="container__prediction">{description}</div>
                    </div>
                ))) : (
                    <div>Loading...</div>
                )}
            </div>
        </div>
    );
};

export default Horoscope;