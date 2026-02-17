import { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

function Compare() {
  const [url1, setUrl1] = useState("");
  const [url2, setUrl2] = useState("");
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleCompare = async () => {
    try {
      setLoading(true);

      const response = await axios.post(
        "http://localhost:8000/compare",
        {
          url1,
          url2,
          question,
        }
      );

      setResult(response.data.result);
      setLoading(false);
    } catch (error) {
      console.error(error);
      setLoading(false);
    }
  };

  return (
    <div className="compare-container">
  <div className="compare-card">

    <h2>Compare Two Videos</h2>

    <input
      type="text"
      placeholder="Video 1 URL"
      className="input-field"
      value={url1}
      onChange={(e) => setUrl1(e.target.value)}
    />

    <input
      type="text"
      placeholder="Video 2 URL"
      className="input-field"
      value={url2}
      onChange={(e) => setUrl2(e.target.value)}
    />

    <input
      type="text"
      placeholder="What do you want to compare?"
      className="input-field"
      value={question}
      onChange={(e) => setQuestion(e.target.value)}
    />

    <button className="primary-btn" onClick={handleCompare}>
      Compare
    </button>

    {result && (
      <div className="compare-result">
        <div className="content-card">
          <ReactMarkdown>{result}</ReactMarkdown>
        </div>
      </div>
    )}

  </div>
</div>
);
}

export default Compare;
