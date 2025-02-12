import React, {useEffect, Suspense} from 'react';
import {Navigate, Route, Routes, useLocation, useNavigate} from "react-router-dom";
import {publicRotes, pwaRotes} from "../rotes/urls";
import {languages, useStore} from "../utils/store";

const AppRouter = () => {
    const {language, setLanguage, languageChangedByHeader, isPwaMode} = useStore();
    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        console.log(location.pathname)
    }, [navigate, location])

    useEffect(() => {
        if (!language) {
            const currentLang = location.pathname.split("/")[1];
            if (languages.includes(currentLang)) {
                setLanguage(currentLang)
            } else {
                const userLanguage = navigator.language.slice(0, 2);
                if (languages.includes(userLanguage)) {
                    setLanguage(userLanguage)
                } else {
                    setLanguage("en")
                }
            }
        }
    }, [])

    useEffect(() => { // редиректы делать тут
        const pathParts = location.pathname.split("/");
        const currentLang = pathParts[1] || language;
        console.log("croos0: ", currentLang, language, pathParts[1])
        if (currentLang !== null && language !== null) {
            console.log("croos1: ", currentLang, language, pathParts[1])
            if (currentLang !== language) {
                console.log("languag3es", currentLang, language)
                if (languages.includes(currentLang)) {
                    if (languageChangedByHeader) {
                        const newPath = `/${language}` + location.pathname.slice(currentLang.length + 1);
                        navigate(newPath, {replace: true});
                        console.log("case 1_0", languageChangedByHeader)
                    } else {
                        console.log("case 1_1", languageChangedByHeader)
                        setLanguage(currentLang)
                    }
                } else { // Если в URL херня то редирект на дефолтный язык
                    navigate(`/${language}/`, {replace: true});
                    console.log("case 2")
                }
            }
        }
    }, [language, location, navigate])

    return (
        <Suspense fallback={<></>}>
            <Routes>
                {publicRotes.map(route =>
                    <Route path={`/${language}${route.path}`} element={route.component} key={route.key}></Route>
                )}
                {isPwaMode && pwaRotes.map(route =>
                    <Route path={`/${language}${route.path}`} element={route.component} key={route.key}></Route>
                )}
                {language ? (
                    <Route path="*" element={<Navigate to="" replace />} key={"redirect"}/>
                ) : ( // редирект на начальную страницу если нет языка| сработает только если быть уже на сайте, очистить кэщ и перейти на другой язык
                    <Route path="*" element={<Navigate to="/en/" replace />} key={"redirect-to-default"}/>
                )}
            </Routes>
        </Suspense>
    );
};

export default AppRouter;