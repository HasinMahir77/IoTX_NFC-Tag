import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';
import './ViewGuitar.css'; // Import the CSS file
import guitar_icon from '../assets/guitar_circle.png';

const AddGuitar = ({server, tag_id }) => {
  const [guitar, setGuitar] = useState({
    tag_id: tag_id,
    name: '',
    manufacturer: '',
    model: '',
    manufacture_year: '',
    serial:''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setGuitar((prevGuitar) => ({
      ...prevGuitar,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(server+'/add_instrument', guitar);
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
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="formTagId">
          <Form.Label>Tag ID</Form.Label>
          <Form.Control type="text" value={guitar.tag_id} readOnly disabled />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formGuitarName">
          <Form.Label>Name</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter guitar name"
            name="name"
            value={guitar.name}
            onChange={handleChange}
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formGuitarManufacturer">
          <Form.Label>Manufacturer</Form.Label>
          <Form.Control
            type="text"
            placeholder="Manufacturer"
            name="manufacturer"
            value={guitar.manufacturer}
            onChange={handleChange}
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formGuitarModel">
          <Form.Label>Model</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter guitar model"
            name="model"
            value={guitar.model}
            onChange={handleChange}
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formGuitarModel">
          <Form.Label>Serial No.</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter serial"
            name="serial"
            value={guitar.serial}
            onChange={handleChange}
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formManufactureYear">
          <Form.Label>Manufacture Date</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter manufacture date"
            name="manufacture_date"
            value={guitar.manufacture_date}
            onChange={handleChange}
          />
        </Form.Group>

        <Button variant="primary" type="submit">
          Save
        </Button>
      </Form>
      </div>
    </div>
  );
};

export default AddGuitar;