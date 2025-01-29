import React, {useEffect, useState} from 'react';
import {decodeMonth, decodeMoonEvent} from "../../../utils/decoders";
import {Link} from "react-router-dom";

const AdditionalTables = ({year, data}) => {
    const [fixedData, setFixedData] = useState([]);
    const getMoonPhaseClass = (phase) => {
        switch (phase) {
            case 1: return "new_moon";
            case 3: return "first_quarter";
            case 5: return "full_moon";
            case 7: return "last_quarter";
            default: return "";
        }
    };

    useEffect(() => {
        const fixData = data && data.reduce((acc, {datetime, phase, events}) => {
            const date = new Date(datetime);

            if (isNaN(date)) {
                return acc;
            }

            const month = date.getMonth();
            const day = date.getDate();

            if (!acc[month]) acc[month] = [];

            acc[month].push({day, phase, events});

            return acc;
        }, {});

        setFixedData(fixData);

    }, [data])

    return (
        <div className={"area__additional_tables"}>
            <div className={"df_column"}>
                <div className={"field__phase_calendar"}>
                    <h2>Moon Phases Calendar</h2>
                    {Object.keys(fixedData).map(month => (
                      <div key={month} className="lunar_phases">
                        <div className="phase_month">{decodeMonth(parseInt(month) + 1)}</div>
                        <div className="monthly_lunar_phases">
                          {fixedData[month].map(({ day, phase }) => (
                            <div key={day} className="cell__phase">
                              <div>{day}:</div>
                              <div className={getMoonPhaseClass(phase)}></div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                </div>
            </div>
            <div className="field__events_calendar">
                <h2>Moon Events in {year}</h2>
                <div className="monthly_lunar_events">
                    {Object.keys(fixedData).map((month) => (
                        fixedData[month].map(({day, events}) => (
                            events.length > 0 && (
                                <div key={month-day} className="phase__event">
                                    <Link to={"#"} className={"default__link"}>{decodeMoonEvent(events[0])}</Link>
                                    <div className="phase__date">{day} - {decodeMonth(parseInt(month)+1)}</div>
                                </div>
                            )
                        ))
                    ))}
                </div>
            </div>
        </div>
    );
};

export default AdditionalTables;