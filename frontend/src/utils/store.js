import {createContext, useContext, useEffect, useState} from "react";


export const StoreContext = createContext(null);

export const useStore = () => {
    return useContext(StoreContext);
}

const languages = ["en", "ru", "pl"];

export const StoreProvider = ({children}) => {
    const [language, setLanguageState] = useState(localStorage.getItem("language"));
    console.log('store render')
    /*useEffect(() => {
        // тяжеленький случай
        const userLanguage = navigator.language.slice(0, 2);

        setLanguage(userLanguage);
    }, [])*/

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
    }
    const setPushNotifications = (notifications=false) => {
        /*сделать доступным только в PWA*/
    }
    const setZodiac = (zodiac=null) => {
        /*сделать доступным только в PWA*/
    }

    return (
        <StoreContext.Provider
            value={{language, setLanguage, setPushNotifications, setZodiac}}>
            {children}
        </StoreContext.Provider>
    )
}

