import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./Input.css";

export default function Input({ title, setTitle, description, setDescription }) {
  const navigate = useNavigate();

  const handleTitleChange = (e) => {
    setTitle(e.target.value);
  };

  const handleDescriptionChange = (e) => {
    setDescription(e.target.value);
  };

  // Submit the form
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/submit", {
        title,
        description,
      });
      if (response.status === 200) {
        document.getElementById("fetty-video").style.display = "block";
        document.getElementById("fetty-video").src = "https://www.youtube.com/watch?v=i_kF4zLNKio"; 

        navigate("/patent", { state: { title, description } });
      }
    } catch (error) {
      console.error("Error submitting patent:", error);
      alert("Error submitting patent: " + error.message);
    }
  };

  return (
    <div className="landing-wrapper">
      {/* 1) Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title animate-fade-in">
            Patent.io
            <span className="period-blink">_</span>
          </h1>
          <p className="hero-motto animate-fade-in-late">
            From Idea to Patent. It’s that simple.
          </p>
          <p className="hero-subtext animate-fade-in-late">
            We transform your innovations into robust, legally sound patents.
            Embrace the future of IP protection with next-level automation and
            expert-driven guidance.
          </p>
          <button
            className="cta-button animate-slide-up"
            onClick={() => {
              document
                .getElementById("invention-form")
                .scrollIntoView({ behavior: "smooth" });
            }}
          >
            Get Started
          </button>
        </div>
        {/* A subtle wave or shape illustration can go here if you want */}
      </section>

      {/* 2) Feature Highlights */}
      <section className="features-section">
        <h2 className="features-heading animate-fade-in">Why Patent.io?</h2>
        <div className="features-cards">
          <div className="feature-card animate-slide-up">
            <h3>Instant Document Generation</h3>
            <p>
              Quickly produce comprehensive, legally sound patent drafts with
              advanced AI generation.
            </p>
          </div>
          <div className="feature-card animate-slide-up">
            <h3>Powered by Innovation</h3>
            <p>
              Our platform combines expert legal knowledge with the latest tech
              to safeguard your ideas.
            </p>
          </div>
          <div className="feature-card animate-slide-up">
            <h3>Global Coverage</h3>
            <p>
              Secure patent protection across multiple jurisdictions all from
              one intuitive dashboard.
            </p>
          </div>
        </div>
      </section>

      {/* 3) The Actual Form */}
      <section className="form-section" id="invention-form">
        <div className="form-container">
          <h2 className="form-heading">Submit Your Invention</h2>
          <p className="form-subtext">
            Provide a brief overview of your invention, and let Patent.io handle
            the rest.
          </p>
          <form className="input-form" onSubmit={handleSubmit}>
            <label htmlFor="title" className="input-label">
              Patent Title
            </label>
            <input
              id="title"
              className="input-field"
              type="text"
              required
              value={title}
              onChange={handleTitleChange}
              placeholder="Enter your patent title here"
            />

            <label htmlFor="description" className="input-label">
              Patent Description
            </label>
            <textarea
              id="description"
              className="input-field textarea-field"
              rows="5"
              required
              value={description}
              onChange={handleDescriptionChange}
              placeholder="Describe your invention..."
            />

            <button type="submit" className="submit-button">
              Generate My Patent
            </button>
          </form>
          <iframe
            id="fetty-video"
            width="560"
            height="315"
            style={{ display: "none", marginTop: "20px" }}
            src=""
            frameBorder="0"
            allow="autoplay; encrypted-media"
            allowFullScreen
        ></iframe>

                </div>
            </section>
            </div>
  );
}
