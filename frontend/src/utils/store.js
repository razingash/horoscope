import {createContext, useContext, useEffect, useState} from "react";

export const StoreContext = createContext(null);

export const useStore = () => {
    return useContext(StoreContext);
}

export const languages = ["en", "ru", "pl"];

export const StoreProvider = ({children}) => {
    const [language, setLanguageState] = useState(localStorage.getItem("language"));
    const [pushNotification, setPushNotification] = useState(localStorage.getItem("notifications") === "true");
    const [choosedZodiac, setChoosedZodiac] = useState(localStorage.getItem("zodiac"));
    const [languageChangedByHeader, setLanguageChangedByHeader] = useState(false);

    const [isPwaMode, setIsPwaMode] = useState(null);
    useEffect(() => {
        const isPwa =  window.matchMedia('(display-mode: window-controls-overlay)').matches ||
            window.matchMedia('(display-mode: standalone)').matches ||
            window.matchMedia('(display-mode: minimal-ui)').matches ||
            window.matchMedia('(display-mode: fullscreen)').matches;

        setIsPwaMode(isPwa);
    }, [])

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
    const setPushNotifications = (notifications) => {
        localStorage.setItem("notifications", notifications)
        setPushNotification(notifications)
    }
    const setZodiac = (zodiac) => {
        localStorage.setItem("zodiac", zodiac)
        setChoosedZodiac(zodiac)
    }

    return (
        <StoreContext.Provider
            value={{language, setLanguage, languageChangedByHeader, isPwaMode,
                pushNotification, setPushNotifications, choosedZodiac, setZodiac}}>
            {children}
        </StoreContext.Provider>
    )
}

