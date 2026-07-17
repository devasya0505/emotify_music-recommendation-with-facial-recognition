import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import Bgm from "./components/bgm.mp4";

function Garlic() {
  return (
    <div>
      <nav
        className="navbar navbar-expand-lg navbar-light bg-dark"
        style={{ paddingLeft: "20px" }}
      >
        <h1 className="navbar-brand logo">Emotify</h1>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav">
            <li className="nav-item active">
              <a className="nav-link" id="home" href="/home">
                Home
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" id="abt-us" href="/about">
                About-Us
              </a>
            </li>
          </ul>
        </div>
      </nav>
      <video loop autoPlay muted id="myvideo">
        <source src={Bgm}></source>
      </video>
      <div>
        <h1 id="abt">Introducing Emotify</h1>
        <p id="abt2">
          We trained a model called Emotify that reads facial expressions and
          recommends songs to match the mood.
        </p>
      </div>
      <a
        href="http://127.0.0.1:5000/"
        id="abt3"
        target="_blank"
        rel="noreferrer"
      >
        Try Emotify
      </a>
    </div>
  );
}

export default Garlic;

//C:\Users\urvas\OneDrive\Desktop\Arithemania-2.0\Emotify_ANKH-master\public\app.py
