import React, {useEffect} from 'react';
import {Link} from "react-router-dom";
import {useStore} from "../../utils/store";

const Header = () => {
    const {language, setLanguage} = useStore();
    const closeMenu = () => {
        const checkbox = document.getElementById("menu__toggle");
        document.body.style.overflow = '';
        checkbox.checked = false;
    };

    const setHiddenLanguage = (language) => {
        setLanguage(language)
        closeMenu()
    }

    useEffect(() => {
        if (!language) {
            const userLanguage = navigator.language.slice(0, 2);
            setLanguage(userLanguage);
        }
    }, [language])

    const changeLanguage = (newLang) => {
        if (language !== newLang) {
            setLanguage(newLang);
        }
    };

    return (
        <div className={"section__header"}>
            <div className={"header__small"}>
                <input id="menu__toggle" onChange={(e) => (document.body.style.overflow = e.target.checked ? 'hidden' : 'auto')} type="checkbox"/>
                <label htmlFor="menu__toggle" className={"menu__button"}>
                    <span className="toggle__bar"></span>
                    <span className="toggle__bar"></span>
                    <span className="toggle__bar"></span>
                </label>
                <div className="header__dropdown">
                    <div className="dropdown__field">
                        <label htmlFor="menu__toggle" className="dropdown__closing">
                            <div className={"cross"}></div>
                        </label>
                        <div className="header__dropdown__item">
                            <input id="arrow__dropdown_1" type="checkbox" className="arrow__dropdown_input"/>
                            <label htmlFor="arrow__dropdown_1" className="arrow__dropdown">
                                <div>Horoscope</div>
                                <div className="arrow_list"></div>
                            </label>
                            <ul className="dropdown__item_hidden">
                                <li><Link onClick={closeMenu} to={`/${language}/horoscope/daily/`} className="header__item">Daily</Link></li>
                                <li><Link onClick={closeMenu} to={`/${language}/horoscope/weekly/`} className="header__item">Weekly</Link></li>
                                <li><Link onClick={closeMenu} to={`/${language}/horoscope/monthly/`} className="header__item">Monthly</Link></li>
                                <li><Link onClick={closeMenu} to={`/${language}/horoscope/annual/`} className="header__item">Annual</Link></li>
                            </ul>
                        </div>
                        <div className="header__dropdown__item">
                            <input id="arrow__dropdown_2" type="checkbox" className="arrow__dropdown_input"/>
                            <label htmlFor="arrow__dropdown_2" className="arrow__dropdown">
                                <div>Languages</div>
                                <div className="arrow_list"></div>
                            </label>
                            <ul className="dropdown__item_hidden">
                                <li className={language === "en" ? "choosed_lang_2" : ""}>
                                    <Link onClick={() => setHiddenLanguage("en")} to={() => changeLanguage("en")}
                                      className={`language__item_2`}>English</Link>
                                </li>
                                <li className={language === "pl" ? "choosed_lang_2" : ""}>
                                    <Link onClick={() => setHiddenLanguage("pl")} to={() => changeLanguage("pl")}
                                      className={`language__item_2`}>Polski</Link>
                                </li>
                                <li className={language === "ru" ? "choosed_lang_2": ""}>
                                    <Link onClick={() => setHiddenLanguage("ru")} to={() => changeLanguage("ru")}
                                      className={`language__item_2`}>Русский</Link>
                                </li>
                            </ul>
                        </div>
                        <Link onClick={closeMenu} to={`/${language}/moon/calendar/`} className="header__dropdown__item">
                            Lunar Phases
                        </Link>
                        <Link onClick={closeMenu} to={`${language}/solar-system/`} className="header__dropdown__item">
                            Solar System
                        </Link>
                    </div>
                </div>
            </div>
            <div className="header__big">
                <div className={"header__item"} id={"horoscope_dropdown"}>
                    <Link to={`/${language}/horoscope/daily/`} className="header__item">Horoscope</Link>
                    <div className={"header__horoscope_dropdown"}>
                        <span className={"dropdown__line"}></span>
                        <Link to={`/${language}/horoscope/daily/`} className="header__item">daily</Link>
                        <Link to={`/${language}/horoscope/weekly/`} className="header__item">weekly</Link>
                        <Link to={`/${language}/horoscope/monthly/`} className="header__item">monthly</Link>
                        <Link to={`/${language}/horoscope/annual/`} className="header__item">annual</Link>
                    </div>
                </div>
                <Link to={`/${language}/moon/calendar/`} className="header__item">lunar calendar</Link>
                <Link to={`${language}/solar-system/`} className="header__item">solar system</Link>
            </div>
            <div className="header__button__language">
                <input id="checkbox_translate" type="checkbox"/>
                <label htmlFor="checkbox_translate" className={"default__label"}>
                   <svg className="svg__translator">
                        <use xlinkHref="#translator"></use>
                    </svg>
                </label>
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