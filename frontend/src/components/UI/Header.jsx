import React, {useEffect} from 'react';
import {Link} from "react-router-dom";
import {useStore} from "../../utils/store";

const Header = () => {
    const {language, setLanguage} = useStore();

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
                                <div className="arrow"></div>
                            </label>
                            <div className="dropdown__item_hidden">
                                <div>Daily</div>
                                <div>Weekly</div>
                                <div>Monthly</div>
                                <div>Annual</div>
                            </div>
                        </div>
                        <div className="header__dropdown__item">
                            <input id="arrow__dropdown_2" type="checkbox" className="arrow__dropdown_input"/>
                            <label htmlFor="arrow__dropdown_2" className="arrow__dropdown">
                                <div>Languages</div>
                                <div className="arrow"></div>
                            </label>
                            <div className="dropdown__item_hidden">
                                <div>English</div>
                                <div>Polish</div>
                                <div>Русский</div>
                            </div>
                        </div>
                        <div className="header__dropdown__item">
                            <div>Lunar Phases</div>
                        </div>
                        <div className="header__dropdown__item">
                            <div>Solar System</div>
                        </div>
                        <div className="header__dropdown__item">
                            <div>Natal Chart</div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="header__big">
                <Link to={`/${language}/horoscope/daily/`} className="header__item">Horoscope</Link>
                <Link to={`/${language}/moon/calendar/`} className="header__item">lunar calendar</Link>
                <Link to={"#"} className={"header__item"}>natal chart</Link>
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