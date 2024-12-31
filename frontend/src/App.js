import {BrowserRouter} from "react-router-dom";
import "./styles/index.css"
import AppRouter from "./components/AppRouter";
import Header from "./components/UI/Header";

function App() {
  return (
    <BrowserRouter>
      <Header/>
      <AppRouter/>
    </BrowserRouter>
  );
}

export default App;
