import { useNavigate } from "react-router-dom";
import "./Header.css";

function Header() {
  const navigate = useNavigate();

  return (
    <div className="header">

      {/* Left Logo */}
      <div className="header-btn" onClick={() => navigate("/")}>
        🎥 YouTube_Chatbot
      </div>

      {/* Center Compare Button */}
      <button
        className="header-btn"
        onClick={() => navigate("/compare")}
      >
        Compare Two Videos
      </button>

      {/* Right Login */}
      <button
        className="header-btn"
        onClick={() => alert("Login feature coming soon")}
      >
        Login
      </button>

    </div>
  );
}

export default Header;
