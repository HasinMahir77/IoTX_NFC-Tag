import React, { useState, useEffect, useRef } from 'react';
import { Form, Button, Modal } from 'react-bootstrap';
import axios from 'axios';
import heic2any from 'heic2any';
import './GuitarApp.css'; // Import the CSS file
import guitar_icon from '../assets/guitar_circle.png';

const GuitarApp = ({server, tag_id, guitarExists }) => {
  const [imageUrl, setImageUrl] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const fileInputRef = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [guitarImage, setGuitarImage] = useState(null);

  const [guitar, setGuitar] = useState({
    tag_id: tag_id,
    name: '',
    manufacturer: '',
    model: '',
    serial: '',
    manufacture_date: ''
  });
  const [guitarInput, setGuitarInput] = useState({
    tag_id: tag_id,
    name: '',
    manufacturer: '',
    model: '',
    manufacture_date: '',
    serial: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setGuitarInput((prevGuitar) => ({
      ...prevGuitar,
      [name]: value
    }));
  };

  const handleImageClick = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
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
      const fileType = file.type;
      const fileName = file.name;
      const fileExtension = fileName.split('.').pop().toLowerCase();
      console.log(`Selected file type: ${fileType}`);
      console.log(`Selected file name: ${fileName}`);
      console.log(`Selected file extension: ${fileExtension}`);
      
      if (fileType === 'image/heic' || fileType === 'image/heif' || fileExtension === 'heic' || fileExtension === 'heif') {
        try {
          console.log('Converting HEIC image...');
          const convertedBlob = await heic2any({ blob: file, toType: 'image/jpeg' });
          console.log('Converted Blob:', convertedBlob);
          const reader = new FileReader();
          reader.onloadend = () => {
            setImageUrl(reader.result);
            const convertedFile = new File([convertedBlob], `${tag_id}.jpg`, { type: 'image/jpeg' });
            setSelectedFile(convertedFile);
            console.log('HEIC image converted and set:', convertedFile);
          };
          reader.readAsDataURL(convertedBlob);
        } catch (error) {
          console.error('Error converting HEIC image:', error);
        }
      } else {
        const reader = new FileReader();
        reader.onloadend = () => {
          setImageUrl(reader.result);
          setSelectedFile(file);
          console.log('Non-HEIC image selected and set:', file);
        };
        reader.readAsDataURL(file);
      }
    }
  };
  const fetchGuitar = async () => {
    try {
      const response = await axios.get(`${server}/instrument/${tag_id}`);
      setGuitar(response.data);
    } catch (error) {
      console.error('Error fetching guitar:', error);
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
    fetchGuitar();
    checkImage();
  }, [server, tag_id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Submitting guitar input:', guitarInput); // Debugging payload
    try {
      await axios.post(`${server}/add_instrument`, guitarInput, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      alert('Instrument added successfully!');
      window.location.reload(); // Refresh the page
    } catch (error) {
      console.error('Error adding Instrument:', error);
      if (error.response) {
        console.error('Response data:', error.response.data); // Log server response
      }
      alert('Failed to add instrument.');
    }
  };
  const handleImageSave = async () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append('file', selectedFile);
      console.log('Uploading file:', selectedFile);
      try {
        const response = await axios.post(`${server}/upload_image/${tag_id}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        alert('Image uploaded successfully!');
        setShowModal(false);
        window.location.reload(); // Refresh the page
      } catch (error) {
        console.error('Error uploading image:', error);
        alert('Failed to upload image.');
      }
    } else {
      alert('No image selected.');
    }
  };

  return (
    <div className="guitar-info">
      <h2>Add Instrument</h2>
      <img
        src={guitarImage || guitar_icon}
        alt="Guitar Icon"
        className="guitar-icon"
        onClick={handleImageClick}
      />
      <div className='form-container'>
        {guitarExists===false ? 
              <Form onSubmit={handleSubmit}>
              <Form.Group className="mb-3" controlId="formTagId">
                <Form.Label>Tag ID</Form.Label>
                <Form.Control type="text" value={guitarInput.tag_id} readOnly disabled />
              </Form.Group>
      
              <Form.Group className="mb-3" controlId="formGuitarName">
                <Form.Label>Name</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter guitar name"
                  name="name"
                  value={guitarInput.name}
                  onChange={handleChange}
                />
              </Form.Group>
              <Form.Group className="mb-3" controlId="formGuitarManufacturer">
                <Form.Label>Manufacturer</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Manufacturer"
                  name="manufacturer"
                  value={guitarInput.manufacturer}
                  onChange={handleChange}
                />
              </Form.Group>
      
              <Form.Group className="mb-3" controlId="formGuitarModel">
                <Form.Label>Model</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter guitar model"
                  name="model"
                  value={guitarInput.model}
                  onChange={handleChange}
                />
              </Form.Group>
              <Form.Group className="mb-3" controlId="formGuitarModel">
                <Form.Label>Serial No.</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter serial"
                  name="serial"
                  value={guitarInput.serial}
                  onChange={handleChange}
                />
              </Form.Group>
      
              <Form.Group className="mb-3" controlId="formManufactureYear">
                <Form.Label>Manufacture Date</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter manufacture date"
                  name="manufacture_date"
                  value={guitarInput.manufacture_date}
                  onChange={handleChange}
                />
              </Form.Group>
      
              <Button variant="primary" type="submit">
                Save
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
            <img src={imageUrl} alt="Uploaded" style={{ width: '100%' }} />
          ) : (
            'Capture or upload a photo of your instrument.'
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" onClick={handleCaptureClick}>
            Capture
          </Button>
          <Button variant="primary" onClick={handleUploadClick}>
            Upload
          </Button>
          <input
            type="file"
            accept="image/*"
            capture="environment"
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