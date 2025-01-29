import React, {useEffect} from 'react';
import {Link} from "react-router-dom";
import {useStore} from "../../utils/store";

const Header = () => {
    const {language, setLanguage} = useStore();
    console.log('header render')
    useEffect(() => {
        if (!language) {
            const userLanguage = navigator.language.slice(0, 2);
            console.log(language, userLanguage)
            setLanguage(userLanguage);
        }
    }, [])

    const changeLanguage = (newLang) => {
        console.log(language, newLang)
        if (language !== newLang) {
            console.log(language, newLang)
            setLanguage(newLang);
        }
    };

    return (
        <div className={"section__header"}>
            <div className={"header__items"}>
                <Link to={`/${language}/horoscope/daily/`} className={"header__item"}>Horoscope</Link>
                <Link to={`/${language}/moon/calendar/`} className="header__item">lunar calendar</Link>
                <Link to={"#"} className={"header__item"}>natal chart</Link>
                <Link to={`/${language}/info/`} className={"header__item"}>something</Link>
            </div>
            <div className={"header__button__language"}>
                <svg className={"svg__translator"}>
                    <use xlinkHref={"#translator"}></use>
                </svg>
                <div className={"change__language"}>
                    <Link onClick={() => setLanguage("en")} to={() => changeLanguage("en")}
                          className={`language__item ${language === "en" ? "choosed_lang" : ""}`}>English</Link>
                    <Link onClick={() => setLanguage("pl")} to={() => changeLanguage("pl")}
                          className={`language__item ${language === "pl" ? "choosed_lang" : ""}`}>Polski</Link>
                    <Link onClick={() => setLanguage("ru")} to={() => changeLanguage("ru")}
                          className={`language__item ${language === "ru" ? "choosed_lang" : ""}`}>Русский</Link>
                </div>
            </div>
        </div>
    );
};

export default Header;