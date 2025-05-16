import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation, Navigate } from 'react-router-dom';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import GuitarApp from './components/GuitarApp';
import './App.css';

// Define server URL outside components
const SERVER_URL = "http://localhost:7100";

const App = ({ server }) => {
  const [guitarExists, setGuitarExists] = useState(null);
  const location = useLocation();

  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const nfcTagInt = queryParams.get('nfc');
  
    if (nfcTagInt) {
      const checkGuitarExists = async () => {
        try {
          const response = await axios.get(`${server}/instrument_exists/${nfcTagInt}`);
          setGuitarExists(response.data.exists);
        } catch (error) {
          console.error('Error checking instrument:', error);
          // Set to false on error to allow adding new instruments
          setGuitarExists(false);
        }
      };
      checkGuitarExists();
    } else {
      setGuitarExists(false);
    }
  }, [location.search, server]);

  if (guitarExists === null) {
    return <div>Loading...</div>;
  }

  const nfcTagInt = new URLSearchParams(location.search).get('nfc');
  return (
    <div className='mainApp'>
      <GuitarApp server={server} tag_id={nfcTagInt} guitarExists={guitarExists} />
    </div>
  );
};

const Home = () => (
  <div className='mainDiv'>
    <h1 className='urlHeader'>Please use a valid URL or Add/View an instrument.</h1>
    <a href={`${SERVER_URL.replace('7100', '5173')}/nfc_tag?nfc=1`}>Example link</a>
  </div>
);

const MainApp = () => (
  <Router>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/nfc_tag" element={<App server={`${SERVER_URL}/nfc`} />} />
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  </Router>
);

export default MainApp;


