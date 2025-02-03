import {lazy} from "react";

const Main = lazy(() => import("../pages/Main"));
const MoonCalendar = lazy(() => import("../pages/MoonCalendar"));
const Horoscope = lazy(() => import("../pages/Horoscope"));
const MoonEventsDescription = lazy(() => import("../pages/MoonEventsDescription"));
const SolarSystem = lazy(() => import("../pages/SolarSystem"))

export const publicRotes = [
    {path: "/", component: <Main/>, key: "main"},
    /*{path: "/info/", component: <Main/>, key: "info"},*/ /*???*/
    /*{path: "/horoscope/", component: <Main/>, key: "horoscope-info"}, ???*/
    {path: "/horoscope/daily/", component: <Horoscope type={1}/>, key: "horoscope-daily"},
    {path: "/horoscope/weekly/", component: <Horoscope type={2}/>, key: "horoscope-weekly"},
    {path: "/horoscope/monthly/", component: <Horoscope type={3}/>, key: "horoscope-monthly"},
    {path: "/horoscope/annual/", component: <Horoscope type={4}/>, key: "horoscope-annual"},
    {path: "/moon/calendar/", component: <MoonCalendar/>, key: "moon-calendar"},
    {path: "/moon-events/", component: <MoonEventsDescription/>, key: "moon-events"},
    {path: "/solar-system/", component: <SolarSystem/>, key: "solar-system-now"}, /*main page*/
    /*добавить url для настройки работы PWA (должен быть доступен только в PWA?)*/
]