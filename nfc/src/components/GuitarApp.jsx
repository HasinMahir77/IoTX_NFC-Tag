import React, { useState, useEffect, useRef } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';
import './GuitarApp.css'; // Import the CSS file
import guitar_icon from '../assets/guitar_circle.png';

const GuitarApp = ({server, tag_id, guitarExists }) => {
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
    manufacture_year: '',
    serial:''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setGuitarInput((prevGuitar) => ({
      ...prevGuitar,
      [name]: value
    }));
  };

  useEffect(() => {
    const fetchGuitar = async () => {
      try {
        const response = await axios.get(`${server}/instrument/${tag_id}`);
        setGuitar(response.data);
      } catch (error) {
        console.log('Error fetching guitar:', error);
      }
    };

    fetchGuitar();
  }, [server, tag_id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(server+'/add_instrument', guitarInput);
      alert('Instrument added successfully!');
      window.location.reload(); // Refresh the page
    } catch (error) {
      console.error('Error adding Instrument:', error);
      alert('Failed to add instrument.');
    }
  };

  return (
    <div className="guitar-info">
      <h2>Add Instrument</h2>
      <img src={guitar_icon} alt="Guitar Icon" className="guitar-icon" />
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
    </div>
  );
};

export default GuitarApp;