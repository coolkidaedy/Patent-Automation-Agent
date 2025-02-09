import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Input from "./components/Input";
import Main from "./components/Main";

export default function App() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  return (
    <Router>
      <Routes>
        {/* Pass title, setTitle, description, and setDescription as props to Input */}
        <Route
          path="/"
          element={<Input title={title} setTitle={setTitle} description={description} setDescription={setDescription} />}
        />
        {/* Main component should receive the lifted state if needed */}
        <Route path="/patent" element={<Main title={title} description={description} />} />
      </Routes>
    </Router>
  );
}
