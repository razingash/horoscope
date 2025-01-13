import {createContext, useContext, useEffect, useState} from "react";


export const StoreContext = createContext(null);

export const useStore = () => {
    return useContext(StoreContext);
}

const languages = ["en", "ru", "pl"];

export const StoreProvider = ({children}) => {
    const [language, setLanguageState] = useState(localStorage.getItem("language") || "en");

    useEffect(() => {
        const userLanguage = navigator.language.slice(0, 2);

        setLanguage(userLanguage);
    }, [language])

    const setLanguage = (language="en") => {
        if (languages.includes(language)) {
            localStorage.setItem("language", language)
            setLanguageState(language);
        } else {
            localStorage.setItem("language", "en")
            setLanguageState("en");
        }
        document.documentElement.lang = language;
    }
    const setPushNotifications = (notifications=false) => {
        /*сделать доступным только в PWA*/
    }
    const setZodiac = (zodiac=null) => {
        /*сделать доступным только в PWA*/
    }

    return (
        <StoreContext.Provider
            value={{language, setPushNotifications, setZodiac}}>
            {children}
        </StoreContext.Provider>
    )
}

