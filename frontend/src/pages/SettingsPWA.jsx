import React from 'react';
import "../styles/pwa-settings.css"
import {translateZodiacs} from "../utils/translations";
import {useStore} from "../utils/store";

const SettingsPwa = () => {
    const {
        pushNotification, setPushNotification, choosedZodiac, setZodiac,
        setLanguage, language, pushTime, setPushNotificationTime
    } = useStore();

    const handleTimeChange = (e) => {
        setPushNotificationTime(e.target.value);
    };

    const handlePushNotificationToggle = async (e) => {
        const isEnabled = e.target.checked;

        if (isEnabled) {
            const permission = await Notification.requestPermission();
            if (permission === "granted") {
                setPushNotification(true);
            } else {
                alert("You have banned notifications. Allow them in the browser settings.");
                e.target.checked = false;
            }
        } else {
            alert(
                "The browser doesn't allow resetting permission to automatically. " +
                "To turn off the notifications, go to the site settings in the browser and change the permits manually."
            )
        }
    }

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
                            <input id="push_notifications" type="checkbox" className={"switch"} checked={pushNotification}
                                   onChange={handlePushNotificationToggle}
                            />
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
                    <div className={"settings__item"} style={{ display: pushNotification ? "flex" : "none" }}>
                        <label htmlFor="push_time">Notification Time</label>
                        <input id="push_time" type="time" value={pushTime || ''} onChange={handleTimeChange}
                               disabled={!pushNotification}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SettingsPwa;