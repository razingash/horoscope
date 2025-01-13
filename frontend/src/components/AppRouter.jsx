import React from 'react';
import {Navigate, Route, Routes} from "react-router-dom";
import {publicRotes} from "../rotes/urls";
import {useStore} from "../utils/store";

const AppRouter = () => {
    const {language} = useStore();

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