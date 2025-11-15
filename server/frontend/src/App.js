import { Routes, Route } from "react-router-dom";
import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register";
import Dealers from "./components/Dealers/Dealers";
import Dealer from "./components/Dealers/Dealer";
import PostReview from "./components/Dealers/PostReview";

function App() {
  return (
    <Routes>
      {/* Login page */}
      <Route path="/login" element={<LoginPanel />} />

      {/* Registration page */}
      <Route path="/register" element={<Register />} />

      {/* Dealers page */}
      <Route path="/dealers" element={<Dealers />} />

      {/* Dealer details page */}
      <Route path="/dealer/:id" element={<Dealer />} />

      {/* Post review page */}
      <Route path="/postreview/:id" element={<PostReview />} />
    </Routes>
  );
}

export default App;
