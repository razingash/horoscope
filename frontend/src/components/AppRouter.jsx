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

    useEffect(() => { // редиректы делать тут
        const pathParts = location.pathname.split("/");
        const currentLang = pathParts[1] || language;
        console.log("croos0: ", currentLang, language, pathParts[1])
        if (currentLang !== null && language !== null) {
            console.log("croos1: ", currentLang, language, pathParts[1])
            if (currentLang !== language) {
                if (languageChangedByHeader) {
                    const newPath = `/${language}` + location.pathname.slice(currentLang.length + 1);
                    navigate(newPath, {replace: true});
                    console.log("case 1", language)
                } else {
                    setLanguage(currentLang);
                    console.log("case 2", currentLang, language)
                }
            } else if (!languages.includes(currentLang)) { // Если в URL херня то редирект на дефолтный язык
                navigate(`/${language}/`, {replace: true});
                console.log("case 3", language)
            }
        }
    }, [language, location, languageChangedByHeader, navigate])

    return (
        <Suspense fallback={<></>}>
            <Routes>
                {publicRotes.map(route =>
                    <Route path={`/${language}${route.path}`} element={route.component} key={route.key}></Route>
                )}
                {isPwaMode && pwaRotes.map(route =>
                    <Route path={`/${language}${route.path}`} element={route.component} key={route.key}></Route>
                )}
                {language && (languageChangedByHeader ? (
                    <Route path="*" element={<Navigate to="" replace />} key={"redirect"}/>
                ) : (
                    <Route path="*" element={<Navigate to={`/${language}/`} replace />} key={"redirect-to-home"} />
                ))}
                <Route path="*" element={<Navigate to="" replace />} key={"redirect"}/>
            </Routes>
        </Suspense>
    );
};

export default AppRouter;