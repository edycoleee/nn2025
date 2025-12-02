import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE = 'http://localhost:5000/api';

function App() {
  // State management
  const [classes, setClasses] = useState([]);
  const [newClassName, setNewClassName] = useState('');
  const [selectedClass, setSelectedClass] = useState('');
  const [images, setImages] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [training, setTraining] = useState(false);
  const [models, setModels] = useState([]);
  
  // Refs untuk webcam
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);

  // Fetch initial data
  useEffect(() => {
    fetchClasses();
    fetchModels();
  }, []);

  // API Functions
  const fetchClasses = async () => {
    try {
      const response = await axios.get(`${API_BASE}/classes`);
      setClasses(response.data);
    } catch (error) {
      console.error('Error fetching classes:', error);
    }
  };

  const fetchModels = async () => {
    try {
      const response = await axios.get(`${API_BASE}/models`);
      setModels(response.data);
    } catch (error) {
      console.error('Error fetching models:', error);
    }
  };

  const addClass = async () => {
    if (!newClassName.trim()) return;
    
    try {
      const response = await axios.post(`${API_BASE}/classes`, {
        class_name: newClassName
      });
      
      if (response.data.success) {
        setNewClassName('');
        fetchClasses();
      }
    } catch (error) {
      console.error('Error adding class:', error);
    }
  };

  const deleteClass = async (classId) => {
    if (window.confirm('Are you sure you want to delete this class and all its images?')) {
      try {
        await axios.delete(`${API_BASE}/classes?id=${classId}`);
        fetchClasses();
      } catch (error) {
        console.error('Error deleting class:', error);
      }
    }
  };

  // Webcam Functions
  const startWebcam = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 }
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        setStream(mediaStream);
      }
    } catch (error) {
      console.error('Error accessing webcam:', error);
    }
  };

  const stopWebcam = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
  };

  const captureImage = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    
    if (video && canvas) {
      const context = canvas.getContext('2d');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      
      return canvas.toDataURL('image/jpeg');
    }
    return null;
  };

  const saveCapturedImage = async () => {
    if (!selectedClass) {
      alert('Please select a class first');
      return;
    }
    
    const imageData = captureImage();
    if (!imageData) return;
    
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/images`, {
        class_id: selectedClass,
        image: imageData,
        filename: `capture_${Date.now()}.jpg`
      });
      
      alert('Image saved for training!');
    } catch (error) {
      console.error('Error saving image:', error);
      alert('Failed to save image');
    } finally {
      setLoading(false);
    }
  };

  const trainModel = async () => {
    setTraining(true);
    try {
      const response = await axios.post(`${API_BASE}/train`, {
        epochs: 15
      });
      
      if (response.data.success) {
        alert(`Model trained successfully! Accuracy: ${response.data.accuracy.toFixed(2)}%`);
        fetchModels();
      } else {
        alert(`Training failed: ${response.data.error}`);
      }
    } catch (error) {
      console.error('Error training model:', error);
      alert('Training failed');
    } finally {
      setTraining(false);
    }
  };

  const predictImage = async () => {
    const imageData = captureImage();
    if (!imageData) return;
    
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE}/predict`, {
        image: imageData
      });
      
      if (response.data.success) {
        setPrediction(response.data);
      } else {
        alert(`Prediction failed: ${response.data.error}`);
      }
    } catch (error) {
      console.error('Error predicting:', error);
      alert('Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>AI Image Classification System</h1>
      
      <div className="dashboard">
        {/* Left Panel - Class Management */}
        <div className="panel left-panel">
          <h2>Class Management</h2>
          
          <div className="add-class-form">
            <input
              type="text"
              value={newClassName}
              onChange={(e) => setNewClassName(e.target.value)}
              placeholder="Enter class name"
            />
            <button onClick={addClass}>Add Class</button>
          </div>
          
          <div className="class-list">
            <h3>Existing Classes</h3>
            {classes.map(cls => (
              <div key={cls.id} className="class-item">
                <span>{cls.class_name}</span>
                <button 
                  onClick={() => deleteClass(cls.id)}
                  className="delete-btn"
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
          
          <div className="model-training">
            <h3>Model Training</h3>
            <button 
              onClick={trainModel} 
              disabled={training || classes.length < 2}
              className="train-btn"
            >
              {training ? 'Training...' : 'Train New Model'}
            </button>
            
            <div className="model-list">
              <h4>Trained Models</h4>
              {models.map(model => (
                <div key={model.id} className="model-item">
                  <div>{model.model_name}</div>
                  <div className="model-accuracy">
                    Accuracy: {(model.accuracy * 100).toFixed(2)}%
                  </div>
                  <div className="model-date">
                    {new Date(model.created_at).toLocaleDateString()}
                  </div>
                  {model.status === 'active' && (
                    <span className="active-badge">Active</span>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
        
        {/* Middle Panel - Webcam & Capture */}
        <div className="panel middle-panel">
          <h2>Webcam Capture</h2>
          
          <div className="webcam-container">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              className="webcam-view"
            />
            <canvas ref={canvasRef} style={{ display: 'none' }} />
          </div>
          
          <div className="webcam-controls">
            <button onClick={startWebcam} disabled={!!stream}>
              Start Webcam
            </button>
            <button onClick={stopWebcam} disabled={!stream}>
              Stop Webcam
            </button>
            
            <select 
              value={selectedClass}
              onChange={(e) => setSelectedClass(e.target.value)}
              className="class-select"
            >
              <option value="">Select Class</option>
              {classes.map(cls => (
                <option key={cls.id} value={cls.id}>
                  {cls.class_name}
                </option>
              ))}
            </select>
            
            <button 
              onClick={saveCapturedImage} 
              disabled={!stream || !selectedClass || loading}
            >
              {loading ? 'Saving...' : 'Capture & Save for Training'}
            </button>
            
            <button 
              onClick={predictImage} 
              disabled={!stream || models.length === 0}
              className="predict-btn"
            >
              Capture & Predict
            </button>
          </div>
          
          {prediction && (
            <div className="prediction-result">
              <h3>Prediction Result</h3>
              <div className="prediction-details">
                <div className="prediction-class">
                  <strong>Class:</strong> {prediction.prediction}
                </div>
                <div className="prediction-confidence">
                  <strong>Confidence:</strong> {prediction.confidence.toFixed(2)}%
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;