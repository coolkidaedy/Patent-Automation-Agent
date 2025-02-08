import React, { useState } from 'react';
import './Input.css'; 

export default function Input() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const handleTitleChange = (e) => {
    setTitle(e.target.value);
  };

  const handleDescriptionChange = (e) => {
    setDescription(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: Handle form submission logic
    console.log("Title:", title);
    console.log("Description:", description);
  };

  return (
    <form className="input-form" onSubmit={handleSubmit}>
      <h2 className="form-heading">Submit Your Info</h2>

      <label htmlFor="title" className="input-label">Title</label>
      <input
        id="title"
        className="input-field"
        type="text"
        required
        value={title}
        onChange={handleTitleChange}
        placeholder="Enter a title..."
      />

      <label htmlFor="description" className="input-label">Description</label>
      <textarea
        id="description"
        className="input-field textarea-field"
        rows="4"
        required
        value={description}
        onChange={handleDescriptionChange}
        placeholder="Enter a description..."
      />

      <button type="submit" className="submit-button">Submit</button>
    </form>
  );
}
