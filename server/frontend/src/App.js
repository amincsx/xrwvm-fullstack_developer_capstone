import { Routes, Route } from "react-router-dom";
import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register";
import Dealers from "./components/Dealers/Dealers";

function App() {
  return (
    <Routes>
      {/* Login page */}
      <Route path="/login" element={<LoginPanel />} />

      {/* Registration page */}
      <Route path="/register" element={<Register />} />

      {/* Dealers page */}
      <Route path="/dealers" element={<Dealers />} />
    </Routes>
  );
}

export default App;
