import React, { useEffect, useState, useCallback } from "react";
import { useLocation } from 'react-router-dom';

import Card from "../../../components/Card";

const CandidateList = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [isStorageData, setIsStorageData] = useState(false);
  const [data, setData] = useState([]);
  let { state } = useLocation();
  if (state == null) {
    state = {};
  }
  let { selectedFiles = [], title = null, description = null } = state;

  const checkstorageData = () => {
    setIsLoading(true);
    const storedData = localStorage.getItem("candidates");
    if (storedData !== null) {
      setIsStorageData(true);
      const data = JSON.parse(storedData);
      setData(data);
    }
    setIsLoading(false);
  };

  const handleSubmit = useCallback(() => {
    setIsLoading(true);
    if (selectedFiles.length && title && description) {
      const formData = new FormData();
      selectedFiles.forEach((file, _) => {
        formData.append('files', file, file.name);
      });
      formData.append('job_title', title);
      formData.append('job_description', description);
  
      const reqData = {
        method: 'POST',
        body: formData,
        redirect: 'follow'
      }
  
      fetch('http://127.0.0.1:8080/resume-parser/process', reqData)
        .then(response => {
          if (response.ok) {
            return response.json().then((data) => {
              setData(data);
              localStorage.setItem('candidates', JSON.stringify(data))
            });
          } else {
            console.error('Form submission failed.', response.text());
          }
        })
        .catch((error) => {
          console.error('Error:', error);
        })
        .finally(() => {
          setIsLoading(false);
          window.history.replaceState({}, document.title);
        });;
    } else {
      console.log('Please fill in all the fields before submitting.');
      setIsLoading(false);
    }
  }, [description, selectedFiles, title]);

  useEffect(() => {
    if (!selectedFiles || !title || !description) {
      checkstorageData();
    } else {
      handleSubmit();
    }
  }, []);

  return (
    <div>
      {isLoading && (
        <p>loading data</p>
      )}
      <div className="my-4">
        <h3 className="mb-0">Candidates</h3>
        {isStorageData && (
          <span className="text-muted">
            showing candidates from your last processed resume(s)
          </span>
        )}
      </div>
      <div>
        {data.length ? (
          <div className="row">
            {data.map((item, key) => (
              <div key={key} className="col-4 d-flex align-items-stretch">
                <Card data={item}/>
              </div>
            ))}
          </div>
        ) : (
          <p>No data to show</p>
        )}
      </div>
    </div>
  )
};

export default CandidateList;
