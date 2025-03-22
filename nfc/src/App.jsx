import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation, Navigate } from 'react-router-dom';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import AddGuitar from './components/AddGuitar';
import ViewGuitar from './components/ViewGuitar';
import './App.css';

const App = ({ server }) => {
  const [guitarExists, setGuitarExists] = useState(null);
  const location = useLocation();

  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const nfcTagInt = queryParams.get('nfc');

    if (nfcTagInt) {
      const checkGuitarExists = async () => {
        try {
          const response = await axios.get(`${server}/instrument/${nfcTagInt}`);
          setGuitarExists(true);
        } catch (error) {
          if (error.response && error.response.status === 404) {
            setGuitarExists(false);
          } else {
            console.error('Error checking guitar:', error);
          }
        }
      };

      checkGuitarExists();
    }
  }, [location.search, server]);

  if (guitarExists === null) {
    return <div>Loading...</div>;
  }

  const nfcTagInt = new URLSearchParams(location.search).get('nfc');

  return (
    <div className='mainApp'>
      {guitarExists ? (
        <ViewGuitar server={server} tag_id={nfcTagInt} />
      ) : (
        <AddGuitar server={server} tag_id={nfcTagInt} />
      )}
    </div>
  );
};

const Home = () => (
  <div className='mainDiv'>
    <h1 className='urlHeader'>Please use a valid URL or Add/View an instrument.</h1>
    <a href="http://nfc.iotexperience.com/nfc_tag?nfc=1">Example link</a>
    

  </div>
);

const MainApp = () => (
  <Router>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/nfc_tag" element={<App server="http://127.0.0.1:3000" />} />
      <Route path="*" element={<Navigate to="/" />} /> {/* Catch-all route */}
    </Routes>
  </Router>
);

export default MainApp;


