import {BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./screens/Home";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route exact={true} path="/home" element={<Home />}>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
