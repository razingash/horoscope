import {createContext, useContext, useState} from "react";


export const StoreContext = createContext(null);

export const useStore = () => {
    return useContext(StoreContext);
}

const languages = ["en", "ru", "pl"];

export const StoreProvider = ({children}) => {
    const [language, setLanguageState] = useState(localStorage.getItem("language"));
    const [languageChangedByHeader, setLanguageChangedByHeader] = useState(false);

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
    const setPushNotifications = (notifications=false) => {
        /*сделать доступным только в PWA*/
    }
    const setZodiac = (zodiac=null) => {
        /*сделать доступным только в PWA*/
    }

    const resetLanguageChangeFlag = () => {
        setLanguageChangedByHeader(false);
    }

    return (
        <StoreContext.Provider
            value={{language, setLanguage, languageChangedByHeader, resetLanguageChangeFlag, setPushNotifications, setZodiac}}>
            {children}
        </StoreContext.Provider>
    )
}

