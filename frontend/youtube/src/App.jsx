import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Home from "./pages/Home";
import Compare from "./pages/Compare";
import Result from "./pages/Result";

function App() {
  return (
    <Router>
      <Header />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/compare" element={<Compare />} />
        <Route path="/result" element={<Result />} />
      </Routes>

    </Router>
  );
}

export default App;
