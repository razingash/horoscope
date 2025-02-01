import React, {useEffect, useState} from 'react';
import "../styles/moon.css"
import {useFetching} from "../hooks/useFetching";
import TranslatorService from "../API/TranslatorService";
import {useStore} from "../utils/store";
import {decodeMoonEvent} from "../utils/translations";

const MoonEventsDescription = () => {
    const {language} = useStore();
    const [description, setDescription] = useState([]);
    const [fetchDescription] = useFetching(async() => {
        return await TranslatorService.getMoonEventsDescription(language);
    }, 0, 1000);

    useEffect(() => {
        const loadData = async () => {
            const data = await fetchDescription();
            data && setDescription(data);
        }
        void loadData();
    }, [])

    return (
        <div className={"section__main"}>
            <div className={"area__events_description"}>
                {description && description.map(event => (
                <div className={"field__event"}>
                    <div className={"event__header"}>{decodeMoonEvent(event.event_type, language)}</div>
                    <span className={"event__spacing"}></span>
                    <div className={"event__description"}>{event.description}</div>
                </div>
                ))}
            </div>
        </div>
    );
};

export default MoonEventsDescription;