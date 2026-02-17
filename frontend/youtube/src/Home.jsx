import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const [url, setUrl] = useState("");
  const navigate = useNavigate();

  const handleSubmit = () => {
    if (!url) return;
    navigate("/result", { state: { url } });
  };

  return (
    <div className="home-container">
      <div className="home-card">
        <h2>Paste YouTube Link</h2>

        <input
          className="input-field"
          type="text"
          placeholder="Enter YouTube URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />

        <button className="primary-btn" onClick={handleSubmit}>
          Generate Transcript
        </button>
      </div>
    </div>
  );
}

export default Home;
