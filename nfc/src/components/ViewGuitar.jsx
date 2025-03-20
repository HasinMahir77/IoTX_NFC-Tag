import React, { useState, useEffect } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';
import './ViewGuitar.css'; // Import the CSS file
import guitar_icon from '../assets/guitar_circle.png';

const ViewGuitar = ({ server, tag_id }) => {
  const [guitar, setGuitar] = useState({
    tag_id: tag_id,
    name: '',
    model: '',
    manufacture_year: ''
  });

  useEffect(() => {
    const fetchGuitar = async () => {
      try {
        const response = await axios.get(`${server}/guitar/${tag_id}`);
        setGuitar(response.data);
      } catch (error) {
        console.error('Error fetching guitar:', error);
        alert('Failed to fetch guitar.');
      }
    };

    fetchGuitar();
  }, [server, tag_id]);

  return (
    <div className="guitar-info">
        <h2>Guitar Info</h2>
        <img src={guitar_icon} alt="Guitar Icon" className="guitar-icon" />

      <div className='form-container'>
      <Form>
        <Form.Group className="mb-3" controlId="formTagId">
          <Form.Label>Tag ID</Form.Label>
          <Form.Control type="text" value={guitar.tag_id} readOnly />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formGuitarName">
          <Form.Label>Guitar Name</Form.Label>
          <Form.Control
            type="text"
            value={guitar.name}
            readOnly
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formGuitarModel">
          <Form.Label>Guitar Model</Form.Label>
          <Form.Control
            type="text"
            value={guitar.model}
            readOnly
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formManufactureYear">
          <Form.Label>Manufacture Year</Form.Label>
          <Form.Control
            type="text"
            value={guitar.manufacture_year}
            readOnly
          />
        </Form.Group>
      </Form>
      </div>
    </div>
  );
};

export default ViewGuitar;