import React, {useState} from 'react';
import './../styles/horoscope.css'

const Horoscope = () => {
    const [zodiacs, setZodiacs] = useState([...Array(12).keys()]);


    return (
        <div className={"section__main"}>
            <h1>Daily horoscope</h1>
            <div className={"area__horoscope"}>
                {zodiacs.map(zodiac => (
                    <div className={"field__prediction"} key={zodiac}>
                        <hr />
                        <svg className={"svg__zodiac"}>
                            <use xlinkHref={`#zodiac_${zodiac + 1}`}></use>
                        </svg>
                        <div className={"container__prediction"}>
                            Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibu
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Horoscope;