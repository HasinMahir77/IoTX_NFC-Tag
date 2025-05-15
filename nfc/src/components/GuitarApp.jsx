import React, { useState, useEffect, useRef } from 'react';
import { Form, Button, Modal, Alert, Spinner } from 'react-bootstrap';
import axios from 'axios';
import heic2any from 'heic2any';
import './GuitarApp.css'; // Import the CSS file
import guitar_icon from '../assets/guitar_circle.png';
import getCroppedImg from './cropImage'; // Utility function to crop the image
import Cropper from 'react-easy-crop';

const GuitarApp = ({server, tag_id, guitarExists }) => {
  const [imageUrl, setImageUrl] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showCropper, setShowCropper] = useState(false);
  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [croppedAreaPixels, setCroppedAreaPixels] = useState(null);
  const [croppedImage, setCroppedImage] = useState(null);
  const fileInputRef = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [guitarImage, setGuitarImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [guitar, setGuitar] = useState({
    tag_id: tag_id,
    name: '',
    manufacturer: '',
    model: '',
    serial: '',
    manufacture_date: ''
  });
  const [serialInput, setSerialInput] = useState('');

  const handleSerialChange = (e) => {
    setSerialInput(e.target.value);
    if (error) setError(null); // Clear any previous errors
  };

  const handleImageClick = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setShowCropper(false);
  };

  const handleCaptureClick = () => {
    fileInputRef.current.setAttribute('capture', 'environment');
    fileInputRef.current.click();
  };

  const handleUploadClick = () => {
    fileInputRef.current.removeAttribute('capture');
    fileInputRef.current.click();
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImageUrl(reader.result);
        setShowCropper(true); // Show the cropper when an image is selected
      };
      reader.readAsDataURL(file);
      setSelectedFile(file);
    }
  };
  
  const fetchGuitar = async () => {
    try {
      const response = await axios.get(`${server}/instrument_by_tag/${tag_id}`);
      setGuitar(response.data);
    } catch (error) {
      console.error('Error fetching guitar:', error);
    }
  };
  
  const onCropComplete = (croppedArea, croppedAreaPixels) => {
    setCroppedAreaPixels(croppedAreaPixels);
  };

  const handleCropSave = async () => {
    try {
      const croppedImage = await getCroppedImg(imageUrl, croppedAreaPixels);
      setCroppedImage(croppedImage);
      setShowCropper(false);
      alert('Image cropped successfully!');
    } catch (error) {
      console.error('Error cropping image:', error);
    }
  };
  
  const checkImage = async () => {
    try {
      const response = await axios.get(`${server}/check_image/${tag_id}`, { responseType: 'blob' });
      if (response.status === 200) {
        const imageUrl = URL.createObjectURL(response.data);
        setGuitarImage(imageUrl);
        console.log('Image found');
      }
    } catch (error) {
      if (error.response && error.response.status === 404) {
        console.log('Image not found');
      } else {
        console.error('Error checking image:', error);
      }
    }
  };
  
  useEffect(() => {
    if (guitarExists) {
      fetchGuitar();
      checkImage();
    }
  }, [server, tag_id, guitarExists]);

  const handlePairSubmit = async (e) => {
    e.preventDefault();
    
    if (!serialInput.trim()) {
      setError('Please enter a serial number');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      // Call the new pair_by_serial endpoint
      const response = await axios.post(`${server}/pair_by_serial`, {
        tag_id: tag_id,
        serial: serialInput.trim()
      });
      
      if (response.status === 200) {
        alert('Instrument paired successfully!');
        window.location.reload(); // Refresh the page to show the paired instrument
      }
    } catch (error) {
      console.error('Error pairing instrument:', error);
      if (error.response && error.response.data && error.response.data.message) {
        setError(error.response.data.message);
      } else if (error.response && error.response.status === 404) {
        setError('No instrument found with this serial number. Please check and try again.');
      } else {
        setError('Failed to pair the instrument. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };
  
  const handleImageSave = async () => {
    if (imageUrl && croppedAreaPixels) {
      try {
        // Crop the image first
        const croppedImage = await getCroppedImg(imageUrl, croppedAreaPixels);
        setCroppedImage(croppedImage);
  
        // Prepare the cropped image for upload
        const formData = new FormData();
        formData.append('file', croppedImage, `${tag_id}.png`);
        console.log('Uploading cropped image:', croppedImage);
  
        // Upload the cropped image
        const response = await axios.post(`${server}/upload_image/${tag_id}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
  
        alert('Image uploaded successfully!');
        setShowModal(false);
        window.location.reload(); // Refresh the page
      } catch (error) {
        console.error('Error cropping or uploading image:', error);
        alert('Failed to upload image.');
      }
    } else {
      alert('No image selected or cropped area is not defined.');
    }
  };


  return (
    <div className="guitar-info">
      {guitarExists===false ? <h2 className='myHeader'>Pair Instrument</h2> : <h2 className='myHeader'>View Instrument</h2>}
      <img
        src={guitarImage || guitar_icon}
        alt="Guitar Icon"
        className="guitar-icon"
        onClick={handleImageClick}
      />
      <div className='form-container'>
        {guitarExists===false ? 
              <Form onSubmit={handlePairSubmit}>
              <Form.Group className="mb-3" controlId="formTagId">
                <Form.Label>Tag ID</Form.Label>
                <Form.Control type="text" value={tag_id} readOnly disabled />
              </Form.Group>
      
              {error && <Alert variant="danger">{error}</Alert>}
              
              <Form.Group className="mb-3" controlId="formGuitarSerial">
                <Form.Label>Serial Number</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter serial"
                  value={serialInput}
                  onChange={handleSerialChange}
                  disabled={loading}
                />
              </Form.Group>
      
              <Button variant="primary" type="submit" disabled={loading}>
                {loading ? (
                  <>
                    <Spinner animation="border" size="sm" className="me-2" />
                    Pairing...
                  </>
                ) : (
                  'Pair Instrument'
                )}
              </Button>
            </Form>:
            <Form>
                    <Form.Group className="mb-3" controlId="formTagId">
                      <Form.Label>Tag ID</Form.Label>
                      <Form.Control type="text" value={guitar.tag_id} readOnly disabled />
                    </Form.Group>
            
                    <Form.Group className="mb-3" controlId="formGuitarName">
                      <Form.Label>Name</Form.Label>
                      <Form.Control
                        type="text"
                        value={guitar.name}
                        readOnly
                      />
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formGuitarManufacturer">
                              <Form.Label>Manufacturer</Form.Label>
                              <Form.Control
                                type="text"
                                value={guitar.manufacturer}
                                readOnly
                              />
                            </Form.Group>
            
                    <Form.Group className="mb-3" controlId="formGuitarModel">
                      <Form.Label>Model</Form.Label>
                      <Form.Control
                        type="text"
                        value={guitar.model}
                        readOnly
                      />
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formGuitarSerial">
                      <Form.Label>Serial</Form.Label>
                      <Form.Control
                        type="text"
                        value={guitar.serial}
                        readOnly
                      />
                    </Form.Group>
            
                    <Form.Group className="mb-3" controlId="formManufactureYear">
                      <Form.Label>Manufacture Date</Form.Label>
                      <Form.Control
                        type="text"
                        value={guitar.manufacture_date}
                        readOnly
                      />
                    </Form.Group>
                  </Form>}

      </div>
      <Modal centered show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>Upload Photo</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {imageUrl ? (
                <div className="cropper-container">
                <Cropper
                  image={imageUrl}
                  crop={crop}
                  zoom={zoom}
                  aspect={1}
                  cropShape="round"
                  showGrid={false}
                  onCropChange={setCrop}
                  onZoomChange={setZoom}
                  onCropComplete={onCropComplete}
                />
              </div>
              ) : (
                'Capture or upload a photo of your instrument.'
              )}
        </Modal.Body>
        <Modal.Footer>
        {imageUrl? <div className="controls">
                <input
                  type="range"
                  min={1}
                  max={3}
                  step={0.1}
                  value={zoom}
                  onChange={(e) => setZoom(e.target.value)}
                />
        </div>: <></>}
        {/* <Button variant="success" onClick={handleCropSave}>
                Save Cropped Image
              </Button> */}
          <Button variant="primary" onClick={handleCaptureClick}>
            Capture
          </Button>
          <Button variant="primary" onClick={() => fileInputRef.current.click()}>
            Upload
          </Button>
          <input
            type="file"
            accept="image/*"
            ref={fileInputRef}
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
          <Button variant="success" onClick={handleImageSave}>
            Save
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default GuitarApp;