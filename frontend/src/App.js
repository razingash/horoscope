import {BrowserRouter} from "react-router-dom";
import "./styles/index.css"
import './/styles/core.css'
import AppRouter from "./components/AppRouter";
import Header from "./components/UI/Header";
import {StoreProvider} from "./utils/store";

function App() {
    return (
        <StoreProvider>
            <BrowserRouter>
                <Header />
                <AppRouter />
            </BrowserRouter>
        </StoreProvider>
    );
}

export default App;
