import {createContext, useContext, useEffect, useState} from "react";

export const StoreContext = createContext(null);

export const useStore = () => {
    return useContext(StoreContext);
}

export const languages = ["en", "ru", "pl"];

export const StoreProvider = ({children}) => {
    const [languageChangedByHeader, setLanguageChangedByHeader] = useState(false);
    const [language, setLanguageState] = useState(localStorage.getItem("language"));
    const [choosedZodiac, setChoosedZodiac] = useState(localStorage.getItem("zodiac"));
    const [pushNotification, setPushNotification] = useState(Notification.permission === "granted");

    const [pushTime, setPushTime] = useState(localStorage.getItem("pushTime") || "10:00");
    const [isPwaMode, setIsPwaMode] = useState(null);

    useEffect(() => {
        const isPwa =  window.matchMedia('(display-mode: window-controls-overlay)').matches ||
            window.matchMedia('(display-mode: standalone)').matches ||
            window.matchMedia('(display-mode: minimal-ui)').matches ||
            window.matchMedia('(display-mode: fullscreen)').matches;

        setIsPwaMode(isPwa);
    }, [])

    useEffect(() => {
        if (pushNotification && pushTime) {
            const delay = calculateDelay(pushTime);
            console.log(`Push notification scheduled in ${delay / 1000} seconds`);

            const timer = setTimeout(() => {
                triggerPushNotification("Your notification");
            }, delay);

            return () => clearTimeout(timer);
        }
    }, [pushNotification, pushTime]);

    const calculateDelay = (time) => {
        const now = new Date();
        const [hours, minutes] = time.split(":").map(Number);
        const targetTime = new Date();

        targetTime.setHours(hours, minutes, 0, 0);

        if (targetTime <= now) {
            targetTime.setDate(targetTime.getDate() + 1);
        }

        return targetTime - now;
    };

    const triggerPushNotification = (message) => {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.ready.then(registration => {
                registration.active.postMessage({
                    action: 'triggerPush',
                    body: message
                });
            });
        }
    };

    const setLanguage = (newLanguage="en") => {
        if (languages.includes(newLanguage)) {
            localStorage.setItem("language", newLanguage)
            setLanguageState(newLanguage);
            document.documentElement.lang = newLanguage;
        } else {
            localStorage.setItem("language", "en")
            setLanguageState("en");
            document.documentElement.lang = "en";
        }
        setLanguageChangedByHeader(true);
    }

    const setZodiac = (zodiac) => {
        localStorage.setItem("zodiac", zodiac)
        setChoosedZodiac(zodiac)
    }

    const setPushNotificationTime = (time) => {
        localStorage.setItem("pushTime", time)
        setPushTime(time);
    }

    return (
        <StoreContext.Provider
            value={{language, setLanguage, languageChangedByHeader, isPwaMode, triggerPushNotification,
                pushNotification, setPushNotification, choosedZodiac, setZodiac, pushTime, setPushNotificationTime}}>
            {children}
        </StoreContext.Provider>
    )
}

