import React, { useState } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';

const App = () => {
  const [name, setName] = useState('');
  const [image, setImage] = useState(null);
  const [message, setMessage] = useState('');

  const webcamRef = React.useRef(null);

  const captureImage = () => {
    const screenshot = webcamRef.current.getScreenshot();
    setImage(screenshot);
  };

  const handleRegister = async () => {
    try {
      if (!name) {
        setMessage('Name is required');
        return;
      }
      const blob = await fetch(image).then((res) => res.blob());
      const formData = new FormData();
      formData.append('name', name); // Ensure 'name' is being appended
      formData.append('file', blob, 'image.jpg');
      const response = await axios.post('http://localhost:8000/api/faces/register-face', formData);
      setMessage(response.data.message);
    } catch (err) {
      console.error(err);
      setMessage('Error registering face');
    }
  };
  

  const handleVerify = async () => {
    try {
      const blob = await fetch(image).then((res) => res.blob());
      const formData = new FormData();
      formData.append('file', blob, 'image.jpg');
      const response = await axios.post('http://localhost:8000/api/faces/verify-face', formData);
      setMessage(response.data.message);
    } catch (err) {
      setMessage('Error verifying face');
    }
  };

  return (
    <div>
      <h1>Face Verification System</h1>
      <Webcam audio={false} ref={webcamRef} screenshotFormat="image/jpeg" />
      <button onClick={captureImage}>Capture Image</button>
      {image && <img src={image} alt="Captured" />}
      <div>
        <input
          type="text"
          placeholder="Enter your name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <button onClick={handleRegister}>Register Face</button>
        <button onClick={handleVerify}>Verify Face</button>
      </div>
      {message && <p>{message}</p>}
    </div>
  );
};

export default App;

