import React, {useEffect, Suspense} from 'react';
import {Navigate, Route, Routes, useLocation, useNavigate} from "react-router-dom";
import {publicRotes, pwaRotes} from "../rotes/urls";
import {useStore} from "../utils/store";

const AppRouter = () => {
    const {language, setLanguage, languageChangedByHeader, isPwaMode} = useStore();
    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        const pathParts = location.pathname.split("/");
        const currentLang = pathParts[1];
        
        if (currentLang !== language ) {
            if (languageChangedByHeader === true) {
                 const newPath = `/${language}` + location.pathname.slice(3);
                navigate(newPath, { replace: true });
            } else {
                setLanguage(currentLang)
            }
        }
    }, [language, navigate, location, languageChangedByHeader])

    return (
        <Suspense fallback={<></>}>
            <Routes>
                {publicRotes.map(route =>
                    <Route path={`/${language}${route.path}`} element={route.component} key={route.key}></Route>
                )}
                {isPwaMode && pwaRotes.map(route =>
                    <Route path={`/${language}${route.path}`} element={route.component} key={route.key}></Route>
                )}
                {languageChangedByHeader ? (
                    <Route path="*" element={<Navigate to="" replace />} key={"redirect"}/>
                ) : (
                    <Route path="*" element={<Navigate to={`/${language}/`} replace />} key={"redirect-to-home"} />
                )}
            </Routes>
        </Suspense>
    );
};

export default AppRouter;