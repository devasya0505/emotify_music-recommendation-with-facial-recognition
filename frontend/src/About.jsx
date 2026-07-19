import React from "react";
import eye from "./components/ankh.png";

function About() {
  return (
    <div className="about-container">
      <nav className="custom-navbar">
        <a href="/home" className="logo">Emotify</a>
        <div className="nav-links">
          <a href="/home" className="nav-link-item">Home</a>
          <a href="/about" className="nav-link-item about-btn active">About-Us</a>
        </div>
      </nav>

      <main className="about-content">
        <div className="about-card">
          <div className="brand-section">
            <img src={eye} alt="ANKH logo" className="about-logo" />
            <h1 className="about-title">MoodTune</h1>
          </div>

          <p className="about-desc">
            This Project focuses on music for all emotions, whether you are happy, sad, or suffering a heartbreak.
            Our app doesn't need to be told anything; it reads your emotion like a friend and plays a song to soothe your heart.
          </p>

          <div className="team-section">
            <h3 className="team-title">Team Members</h3>
            <ul className="team-list">
              <li className="team-member">
                <span className="member-id">240173116003</span>
                <span className="member-name">Devasya Patel</span>
              </li>
              <li className="team-member">
                <span className="member-id">240173116005</span>
                <span className="member-name">Om Kapoor</span>
              </li>
              <li className="team-member">
                <span className="member-id">240173116012</span>
                <span className="member-name">Kamya Shah</span>
              </li>
              <li className="team-member">
                <span className="member-id">240173116013</span>
                <span className="member-name">Mahee Shah</span>
              </li>
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
}

export default About;

