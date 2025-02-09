import React, { useState, useEffect } from "react";
import axios from "axios";
import { useLocation } from "react-router-dom";
import "./Main.css";

export default function Main() {
  const [checkNovelty, setCheckNovelty] = useState(true);
  const [patentData, setPatentData] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [showVideo, setShowVideo] = useState(false); // <-- NEW: Controls video visibility

  const location = useLocation();
  const { title, description } = location.state || {};

  useEffect(() => {
    const getPatentData = async () => {
      try {
        setIsLoading(true);
        const response = await axios.post("http://localhost:5000/generate", {
          title: title,
          description: description,
        });
        if (response.status === 200) {
          setPatentData(response.data.generated_patent_section);
        }
      } catch (error) {
        console.error("Error fetching patent data:", error);
      } finally {
        setIsLoading(false);
      }
    };
    getPatentData();
  }, [title, description]);

  const novelty = async () => {
    try {
      const response = await axios.post("http://localhost:5000/search", {
        query: description,
      });
      if (response.status === 200) {
        setCheckNovelty(response.data.isNovel);
      }
    } catch (error) {
      alert("Error during novelty check: " + error.message);
    }
  };

  return (
    <div className="main-page-background">
      <div className="main-container">
        <div className="header-section">
          <h1 className="page-title">Patent Details</h1>
          {title && (
            <p className="submission-info">
              <strong>Title:</strong> {title}
            </p>
          )}
          {description && (
            <p className="submission-info">
              <strong>Description:</strong> {description}
            </p>
          )}
        </div>

        <div className="novelty-section">
          {checkNovelty ? (
            <h2 className="novelty-indicator novelty-yes">
              Your patent is novel.
            </h2>
          ) : (
            <h2 className="novelty-indicator novelty-no">
              There are too many similarities to your patent.
            </h2>
          )}
        </div>

        <div className="content-heading">Generated Patent Document</div>
        <div className="patent-content-wrapper">
          {isLoading ? (
            <div className="spinner-container">
              <div className="spinner"></div>
              <p>Generating your patent... Please wait.</p>
            </div>
          ) : (
            <div
              className="patent-content"
              dangerouslySetInnerHTML={{ __html: patentData }}
            />
          )}
        </div>

        <div className="button-container">
          <button className="primary-button" onClick={novelty}>
            Check Novelty
          </button>
        </div>

        {/* YouTube Video Button */}
        {!isLoading && patentData && (
          <div className="fetty-section">
            <button
              className="fetty-button"
              onClick={() => setShowVideo(true)}
            >
              Celebrate with Fetty Wap!
            </button>

            {showVideo && (
                <iframe
                className="fetty-video"
                width="560"
                height="315"
                src="https://www.youtube-nocookie.com/embed/i_kF4zLNKio?autoplay=1"
                title="Fetty Wap - No Cookie Version"
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              ></iframe>
              
            )}
          </div>
        )}
      </div>
    </div>
  );
}
