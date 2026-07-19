import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import Bgm from "./components/bgm.mp4";

function Garlic() {
  return (
    <div className="app-container">
      <nav className="custom-navbar">
        <a href="/home" className="logo">Emotify</a>
        <div className="nav-links">
          <a href="/home" className="nav-link-item active">Home</a>
          <a href="/about" className="nav-link-item about-btn">About-Us</a>
        </div>
      </nav>

      <main className="main-content">
        <div className="video-container">
          <video loop autoPlay muted id="myvideo">
            <source src={Bgm}></source>
          </video>
        </div>

        <div className="text-container">
          <h1 className="hero-title">Introducing Emotify</h1>
          <p className="hero-desc">
            We trained a model called Emotify that reads facial expressions and
            recommends songs to match the mood.
          </p>
          <a
            href="http://127.0.0.1:5000/"
            className="cta-button"
            target="_blank"
            rel="noreferrer"
          >
            Try Emotify
          </a>
        </div>
      </main>
    </div>
  );
}

export default Garlic;

