import React, {useEffect, Suspense, useState} from 'react';
import {Navigate, Route, Routes, useLocation, useNavigate} from "react-router-dom";
import {publicRotes, pwaRotes} from "../rotes/urls";
import {languages, useStore} from "../utils/store";

const AppRouter = () => {
    const {language, setLanguage, languageChangedByHeader, isPwaMode} = useStore();
    const [redirectToDefault, setRedirectToDefault] = useState(false);
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
        setRedirectToDefault(true)
        if (currentLang !== null && language !== null) {
            if (currentLang !== language) {
                setRedirectToDefault(false)
                if (languages.includes(currentLang)) {
                    if (languageChangedByHeader) {
                        const newPath = `/${language}` + location.pathname.slice(currentLang.length + 1);
                        navigate(newPath, {replace: true});
                    } else {
                        setLanguage(currentLang)
                    }
                } else {
                    navigate(`/${language}/`, {replace: true});
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
                {language ? ( redirectToDefault ? (
                        <Route path="*" element={<Navigate to={`/${language}/`} replace />} key={"redirect-to-user-language"}/>
                    ) : (
                        <Route path="*" element={<Navigate to="" replace />} key={"redirect"}/>
                    )
                ) : (
                    <Route path="*" element={<Navigate to="/en/" replace />} key={"redirect-to-default"}/>
                )}
            </Routes>
        </Suspense>
    );
};

export default AppRouter;