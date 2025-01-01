import React from 'react';
import {Link} from "react-router-dom";

const Header = () => {
    return (
        <div className={"section__header"}>
            <div className={"header__items"}>
                    <Link to={"/horoscope/daily/"} className={"header__item"}>Horoscope</Link>
                    <Link to={"/moon/calendar/"} className="header__item">lunar calendar</Link>
                    <Link to={"#"} className={"header__item"}>natal chart</Link>
                    <Link to={"/info/"} className={"header__item"}>something</Link>
                </div>
            <div className={"header__field"}>

            </div>
        </div>
    );
};

export default Header;