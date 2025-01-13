import {BrowserRouter} from "react-router-dom";
import "./styles/index.css"
import AppRouter from "./components/AppRouter";
import Header from "./components/UI/Header";
import {StoreProvider} from "./utils/store";

function App() {
    // скорее всего тут будет проблема с индексацие поскольку в html по умолчанию язык en, и поисковым ботам будет
    //пофиг на то что спустя пару милисекунд оно меняется на нужное
    //поэтому нужно найти способ(кроме серверного рендеринга) чтобы обойти эту проблему
  return (
    <StoreProvider>
      <BrowserRouter>
        <Header/>
        <AppRouter/>
      </BrowserRouter>
    </StoreProvider>
  );
}

export default App;
