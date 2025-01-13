import React from 'react';
import {Link} from "react-router-dom";
import {useStore} from "../../utils/store";

const Header = () => {
    const {language} = useStore();

    return (
        <div className={"section__header"}>
            <div className={"header__items"}>
                <Link to={`/${language}/horoscope/daily/`} className={"header__item"}>Horoscope</Link>
                <Link to={`/${language}/moon/calendar/`} className="header__item">lunar calendar</Link>
                <Link to={"#"} className={"header__item"}>natal chart</Link>
                <Link to={`/${language}/info/`} className={"header__item"}>something</Link>
            </div>
            <div className={"header__field"}>

            </div>
        </div>
    );
};

export default Header;