import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';
import './AddGuitar.css'; // Import the CSS file

const AddGuitar = ({server, tag_id }) => {
  const [guitar, setGuitar] = useState({
    tag_id: tag_id,
    name: '',
    model: '',
    manufacture_year: ''
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
      await axios.post(server+'/add_guitar', guitar);
      alert('Guitar added successfully!');
      window.location.reload(); // Refresh the page
    } catch (error) {
      console.error('Error adding guitar:', error);
      alert('Failed to add guitar.');
    }
  };

  return (
    <div className="guitar-info">
      <h2>Add Guitar</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="formTagId">
          <Form.Label>Tag ID</Form.Label>
          <Form.Control type="text" value={guitar.tag_id} readOnly />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formGuitarName">
          <Form.Label>Guitar Name</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter guitar name"
            name="name"
            value={guitar.name}
            onChange={handleChange}
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formGuitarModel">
          <Form.Label>Guitar Model</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter guitar model"
            name="model"
            value={guitar.model}
            onChange={handleChange}
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formManufactureYear">
          <Form.Label>Manufacture Year</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter manufacture year"
            name="manufacture_year"
            value={guitar.manufacture_year}
            onChange={handleChange}
          />
        </Form.Group>

        <Button variant="primary" type="submit">
          Save
        </Button>
      </Form>
    </div>
  );
};

export default AddGuitar;