import React, {useEffect, Suspense} from 'react';
import {Navigate, Route, Routes, useLocation, useNavigate} from "react-router-dom";
import {publicRotes, pwaRotes} from "../rotes/urls";
import {languages, useStore} from "../utils/store";

const AppRouter = () => {
    const {language, setLanguage, languageChangedByHeader, isPwaMode} = useStore();
    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => { // REDO
        const pathParts = location.pathname.split("/");
        const currentLang = pathParts[1];
        if (!languages.includes(currentLang)) { // Если в URL херня то редирект на дефолтный язык
            navigate(`/${language}/`, { replace: true });
            console.log("case 1")
            return;
        }

        if (currentLang !== language) {
            if (languageChangedByHeader) {
                const newPath = `/${language}` + location.pathname.slice(currentLang.length + 1);
                navigate(newPath, { replace: true });
            } else {
                setLanguage(currentLang);
            }
        }
    }, [language, navigate, location, languageChangedByHeader]);

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