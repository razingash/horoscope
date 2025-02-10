import React from 'react';
import "../styles/pwa-settings.css"
import {translateZodiacs} from "../utils/translations";
import {useStore} from "../utils/store";

const SettingsPwa = () => {
    const {pushNotification, setPushNotifications, choosedZodiac, setZodiac, setLanguage, language} = useStore();

    return (
        <div className={"section__main"}>
            <div className={"field__settings"}>
                <div className={"settings__list"}>
                    <div className={"settings__item"}>
                        <label htmlFor="languages">Language</label>
                        <select id="languages" value={language} onChange={(e) => setLanguage(e.target.value)}>
                            <option value={"en"}>english</option>
                            <option value={"pl"}>polish</option>
                            <option value={"ru"}>русский</option>
                        </select>
                    </div>
                    <div className={"settings__item"}>
                        <div>Nofitications</div>
                        <label htmlFor="push_notifications" className={"checkbox_zipline"}>
                            <span className={"zipline"}></span>
                            <input id="push_notifications" onChange={(e) => setPushNotifications(e.target.checked)}
                                   type="checkbox" className={"switch"} checked={pushNotification}></input>
                            <span className="slider"></span>
                        </label>
                    </div>
                    <div className={"settings__item"} style={{ display: pushNotification ? "flex" : "none" }}>
                        <label htmlFor="zodiac">Zodiac</label>
                        <select id="zodiac" value={choosedZodiac || ""} onChange={(e) => setZodiac(Number(e.target.value))}>
                            <option value="" disabled>select...</option>
                            {translateZodiacs(language).map((zodiac, index) => (
                                <option key={index} value={index + 1}>{zodiac}</option>
                            ))}
                        </select>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SettingsPwa;