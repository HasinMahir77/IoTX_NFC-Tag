import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Form, Button, Modal, Alert, Spinner } from 'react-bootstrap';
import axios from 'axios';
import './GuitarApp.css';
import instrument_icon from '../assets/guitar_circle.png';
import getCroppedImg from './cropImage';
import Cropper from 'react-easy-crop';

// Constants
const INITIAL_INSTRUMENT_STATE = {
  tag_id: '',
  name: '',
  manufacturer: '',
  model: '',
  serial: '',
  manufacture_date: ''
};

const InstrumentApp = ({ server, tag_id, guitarExists }) => {
  // State Management
  const [instrument, setInstrument] = useState({ ...INITIAL_INSTRUMENT_STATE, tag_id: tag_id || '' });
  const [serialInput, setSerialInput] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // Image Upload State
  const [imageUrl, setImageUrl] = useState(null);
  const [instrumentImage, setInstrumentImage] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [croppedAreaPixels, setCroppedAreaPixels] = useState(null);
  const fileInputRef = useRef(null);

  // Data Fetching
  const fetchInstrument = useCallback(async () => {
    try {
      const response = await axios.get(`${server}/instrument_by_tag/${tag_id}`);
      setInstrument({
        ...response.data,
        tag_id: tag_id,
        name: response.data.name || '',
        manufacturer: response.data.manufacturer || '',
        model: response.data.model || '',
        serial: response.data.serial || '',
        manufacture_date: response.data.manufacture_date || ''
      });
    } catch (error) {
      console.error('Error fetching instrument:', error);
      setInstrument({ ...INITIAL_INSTRUMENT_STATE, tag_id: tag_id || '' });
    }
  }, [server, tag_id]);

  const checkImage = useCallback(async () => {
    try {
      const response = await axios.get(`${server}/check_image/${tag_id}`, { responseType: 'blob' });
      if (response.status === 200) {
        const imageUrl = URL.createObjectURL(response.data);
        setInstrumentImage(imageUrl);
        console.log('Image found');
      }
    } catch (error) {
      if (error.response?.status === 404) {
        console.log('Image not found');
      } else {
        console.error('Error checking image:', error);
      }
      setInstrumentImage(null);
    }
  }, [server, tag_id]);

  // Event Handlers
  const handleSerialChange = (e) => {
    setSerialInput(e.target.value);
    if (error) setError(null);
  };

  const handlePairSubmit = async (e) => {
    e.preventDefault();
    
    if (!serialInput.trim()) {
      setError('Please enter a serial number');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      await axios.post(`${server}/pair_instrument`, {
        tag_id: tag_id,
        serial: serialInput.trim()
      });
      
      alert('Instrument paired successfully!');
      window.location.reload();
    } catch (error) {
      console.error('Error pairing instrument:', error);
      if (error.response?.data?.error) {
        setError(error.response.data.error);
      } else if (error.response?.status === 404) {
        setError('No instrument found with this serial number. Please check and try again.');
      } else {
        setError('Failed to pair the instrument. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  // Image Upload Handlers
  const handleImageClick = () => setShowModal(true);
  const handleCloseModal = () => setShowModal(false);
  const handleCaptureClick = () => {
    fileInputRef.current.setAttribute('capture', 'environment');
    fileInputRef.current.click();
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setImageUrl(reader.result);
      reader.readAsDataURL(file);
    }
  };

  const onCropComplete = (_, croppedAreaPixels) => {
    setCroppedAreaPixels(croppedAreaPixels);
  };

  const handleImageSave = async () => {
    if (!imageUrl || !croppedAreaPixels) {
      alert('No image selected or cropped area is not defined.');
      return;
    }

    try {
      const croppedImage = await getCroppedImg(imageUrl, croppedAreaPixels);
      const formData = new FormData();
      formData.append('file', croppedImage, `${tag_id}.png`);
      
      await axios.post(`${server}/upload_image/${tag_id}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      alert('Image uploaded successfully!');
      setShowModal(false);
      window.location.reload();
    } catch (error) {
      console.error('Error cropping or uploading image:', error);
      alert('Failed to upload image.');
    }
  };

  // Effects
  useEffect(() => {
    if (guitarExists) {
      fetchInstrument();
    }
    checkImage();
  }, [server, tag_id, guitarExists, fetchInstrument, checkImage]);

  // Render Helpers
  const renderPairingForm = () => (
    <Form onSubmit={handlePairSubmit}>
      <Form.Group className="mb-3" controlId="formTagId">
        <Form.Label>Tag ID</Form.Label>
        <Form.Control type="text" value={tag_id || ''} readOnly disabled />
      </Form.Group>

      {error && <Alert variant="danger">{error}</Alert>}
      
      <Form.Group className="mb-3" controlId="formInstrumentSerial">
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
    </Form>
  );

  const renderInstrumentDetails = () => (
    <Form>
      <Form.Group className="mb-3" controlId="formTagId">
        <Form.Label>Tag ID</Form.Label>
        <Form.Control type="text" value={instrument.tag_id || ''} readOnly disabled />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formInstrumentName">
        <Form.Label>Name</Form.Label>
        <Form.Control type="text" value={instrument.name || ''} readOnly />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formInstrumentManufacturer">
        <Form.Label>Manufacturer</Form.Label>
        <Form.Control type="text" value={instrument.manufacturer || ''} readOnly />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formInstrumentModel">
        <Form.Label>Model</Form.Label>
        <Form.Control type="text" value={instrument.model || ''} readOnly />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formInstrumentSerial">
        <Form.Label>Serial</Form.Label>
        <Form.Control type="text" value={instrument.serial || ''} readOnly />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formManufactureYear">
        <Form.Label>Manufacture Date</Form.Label>
        <Form.Control type="text" value={instrument.manufacture_date || ''} readOnly />
      </Form.Group>
    </Form>
  );

  const renderImageUploadModal = () => (
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
        {imageUrl && (
          <div className="controls">
            <input
              type="range"
              min={1}
              max={3}
              step={0.1}
              value={zoom}
              onChange={(e) => setZoom(e.target.value)}
            />
          </div>
        )}
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
  );

  return (
    <div className="instrument-info">
      <h2 className='myHeader'>
        {guitarExists ? 'View Instrument' : 'Pair Instrument'}
      </h2>
      
      <img
        src={instrumentImage || instrument_icon}
        alt="Instrument Icon"
        className="instrument-icon"
        onClick={handleImageClick}
      />
      
      <div className='form-container'>
        {guitarExists ? renderInstrumentDetails() : renderPairingForm()}
      </div>

      {renderImageUploadModal()}
    </div>
  );
};

export default InstrumentApp;