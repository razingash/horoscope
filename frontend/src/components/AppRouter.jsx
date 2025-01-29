import React, {useEffect} from 'react';
import {Navigate, Route, Routes, useLocation, useNavigate} from "react-router-dom";
import {publicRotes} from "../rotes/urls";
import {useStore} from "../utils/store";

const AppRouter = () => {
    const {language} = useStore();
    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        const pathParts = location.pathname.split("/");
        const currentLang = pathParts[1];
        if (currentLang !== language) {
            const newPath = `/${language}` + location.pathname.slice(3);
            navigate(newPath, { replace: true });
        }
    }, [language, location, navigate]);

    return (
        <Routes>
            {publicRotes.map(route =>
                <Route path={`/${language}${route.path}`} element={route.component} key={route.key}></Route>
            )}
            <Route path="*" element={<Navigate to="" replace />} key={"redirect"}/>
        </Routes>
    );
};

export default AppRouter;