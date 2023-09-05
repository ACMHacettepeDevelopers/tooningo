import { useState } from "react";
import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { Home } from "./Pages/home";
import { Login } from "./Pages/login";
import { Translator } from "./Pages/translator";
import { Contact } from "./Pages/contact";
import { Acm } from "./Pages/acm";
import { Navbar } from "./Components/Navbar/navbar";

function App() {
  return (
    <div className="App">
      <Router>
        <Navbar/>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login/>} />
          <Route path="/translator" element={<Translator/>} /> 
          <Route path="/contact" element={<Contact/>} />
          <Route path="/about_acm" element={<Acm/>} />

        </Routes>
      </Router>
    </div>
  );
}

export default App;
