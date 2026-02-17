import { useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function Result() {
  const location = useLocation();
  const url = location.state?.url;

  const [videoId, setVideoId] = useState("");
  const [transcript, setTranscript] = useState("");
  const [summary, setSummary] = useState("");
  const [activeTab, setActiveTab] = useState("transcript");
  const [loadingSummary, setLoadingSummary] = useState(false);

  // Chat States
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loadingChat, setLoadingChat] = useState(false);

  // Fetch Transcript
  useEffect(() => {
    if (!url) return;

    const fetchTranscript = async () => {
      const response = await axios.post(
        "http://127.0.0.1:8000/get-transcript",
        { url }
      );

      setVideoId(response.data.video_id);
      setTranscript(response.data.transcript);
    };

    fetchTranscript();
  }, [url]);

  // Fetch Summary
  useEffect(() => {
    if (activeTab === "summary" && transcript && !summary) {
      const fetchSummary = async () => {
        try {
          setLoadingSummary(true);

          const response = await axios.post(
            "http://127.0.0.1:8000/summary",
            { transcript }
          );

          setSummary(response.data.summary);
        } catch (error) {
          console.error("Summary error:", error);
        } finally {
          setLoadingSummary(false);
        }
      };

      fetchSummary();
    }
  }, [activeTab, transcript]);

  // Chat Handler
  const handleChat = async () => {
    if (!question) return;

    const userMessage = { sender: "user", text: question };
    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");

    try {
      setLoadingChat(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/chat",
        {
          video_id: videoId,
          transcript: summary || transcript,
          question: userMessage.text
        }
      );

      const aiMessage = {
        sender: "ai",
        text: response.data.response
      };

      setMessages((prev) => [...prev, aiMessage]);

    } catch (err) {
      console.error("Chat error:", err);
    } finally {
      setLoadingChat(false);
    }
  };

  if (!url) return <h2>No URL provided</h2>;

  return (
    <div className="page-container">

      {/* Video */}
      <div className="video-container">
        {videoId && (
          <iframe
            width="100%"
            height="400"
            src={`https://www.youtube.com/embed/${videoId}`}
            title="YouTube video"
            allowFullScreen
          />
        )}
      </div>

      {/* Tabs */}
      <div className="tab-buttons">
        <button
          className={activeTab === "transcript" ? "active" : ""}
          onClick={() => setActiveTab("transcript")}
        >
          Transcript
        </button>

        <button
          className={activeTab === "summary" ? "active" : ""}
          onClick={() => setActiveTab("summary")}
        >
          Summary
        </button>

        <button
          className={activeTab === "chat" ? "active" : ""}
          onClick={() => setActiveTab("chat")}
        >
          Chat with AI
        </button>
      </div>

      {/* Content */}
      <div className="content-card">

        {activeTab === "transcript" && (
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {transcript}
          </ReactMarkdown>
        )}

        {activeTab === "summary" && (
          <>
            {loadingSummary && <p>Generating summary...</p>}
            {!loadingSummary && summary && (
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {summary}
              </ReactMarkdown>
            )}
          </>
        )}

        {activeTab === "chat" && (
          <div className="chat-wrapper">

            <div className="chat-box">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`chat-message ${
                    msg.sender === "user" ? "chat-user" : "chat-ai"
                  }`}
                >
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {msg.text}
                  </ReactMarkdown>
                </div>
              ))}

              {loadingChat && (
                <div className="chat-message chat-ai">
                  Thinking...
                </div>
              )}
            </div>

            <div className="chat-input-container">
              <input
                type="text"
                placeholder="Ask something about this video..."
                className="chat-input"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleChat()}
              />

              <button
                className="chat-send-btn"
                onClick={handleChat}
              >
                Send
              </button>
            </div>

          </div>
        )}

      </div>
    </div>
  );
}

export default Result;
