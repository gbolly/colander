import React, { useState } from 'react';
import { Link } from "react-router-dom";

import "./styles.scss";

const Home = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const handleFileChange = (event) => {
    event.preventDefault();
    const files = event.target.files;
    const selectedFilesArray = Array.from(files);
    setSelectedFiles(selectedFilesArray);
  };

  const handleTitleChange = (event) => {
    event.preventDefault();
    setTitle(event.target.value);
  };

  const handleDescriptionChange = (event) => {
    event.preventDefault();
    setDescription(event.target.value);
  };

  return (
    <div className='home'>
      <div className="row d-flex align-items-start pageRow">
        <div className="col text-left headlineContainer">
          <div>
            <span
              style={{
                background: 'linear-gradient(135deg, #ebe7ff4d, #dad0ff4d)',
                color: '#6A65FF',
                borderRadius: '2rem',
                textTransform: 'uppercase',
                fontSize: '14px',
                fontWeight: '700',
                padding: '0.5rem 1rem',
              }}
            >
              My name is Twinkle
            </span>
          </div>
          <div>
            <span className="typewriter" style={{ "--n": 47 }}>
              I can help you select the best candidate faster.
            </span>
          </div>
        </div>
        <div className="col my-3">
          <div className="card ms-5">
            <div className="container py-3">
              <div className="card-body">
                <h3 className="card-title headerTextsColor text-center">Upload Your Resumes</h3>
                <form className='mt-4'>
                  <div className="form-group">
                    <label htmlFor="title">Job Title</label>
                    <input
                      type="text"
                      className="form-control"
                      id="title"
                      value={title}
                      onChange={handleTitleChange}
                    />
                  </div>
                  <div className="form-group mt-3">
                    <label htmlFor="description">Job Description</label>
                    <textarea
                      className="form-control"
                      id="description"
                      rows="3"
                      value={description}
                      onChange={handleDescriptionChange}
                    />
                  </div>
                  <div className="form-group mt-3">
                    <label htmlFor="formFile" className="form-label">Select Resumes to Process</label>
                    <input
                      type="file"
                      name="files"
                      id="formFile"
                      className="form-control"
                      accept=".pdf, .doc, .docx"
                      onChange={handleFileChange}
                      multiple
                    />
                  </div>
                  <div className="text-center mt-5">
                    <Link
                      to="candidates"
                      state={{ selectedFiles, title, description }}
                    >
                      <button className="btn w-75 uploadBtn rounded">Upload Resume</button>
                    </Link>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
