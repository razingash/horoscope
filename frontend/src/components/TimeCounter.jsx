import React, {useEffect, useState} from 'react';

const TimeCounter = () => {
    const [time, setTime] = useState(new Date());

    useEffect(() => {
        const timerId = setInterval(() => {
            setTime(new Date());
        }, 1000);
        return () => clearInterval(timerId);
    }, [])

    return (
        <div>{time.toLocaleTimeString()}</div>
    );
};

export default TimeCounter;