import MoonCalendar from "../pages/MoonCalendar";
import Main from "../pages/Main";
import Horoscope from "../pages/Horoscope";


export const publicRotes = [
    {path: "/", component: <Main/>, key: "main"},
    /*{path: "/info/", component: <Main/>, key: "info"},*/ /*???*/
    /*{path: "/horoscope/info/", component: <Main/>, key: "horoscope-info"}, ???*/
    /*возможно стоит добавить дату(сейчас будет братся локальное время), или сразу сделать чтобы nginx передавал дату
    * в зависимости от временной зоны*/
    {path: "/horoscope/daily/", component: <Horoscope type={1}/>, key: "horoscope-daily"},
    {path: "/horoscope/weekly/", component: <Horoscope type={2}/>, key: "horoscope-weekly"},
    {path: "/horoscope/monthly/", component: <Horoscope type={3}/>, key: "horoscope-monthly"},
    {path: "/horoscope/annual/", component: <Horoscope type={4}/>, key: "horoscope-annual"},
    {path: "/moon/calendar/", component: <MoonCalendar/>, key: "moon-calendar"},
    /*{path: "/solar-system/", component: <Main/>, key: "solar-system-now"},*/
    /*добавить url для настройки работы PWA (должен быть доступен только в PWA?)*/
]