import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
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
    const nfcTag = queryParams.get('nfc');

    if (nfcTag) {
      const checkGuitarExists = async () => {
        try {
          const response = await axios.get(`${server}/guitar/${nfcTag}`);
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

  const nfcTag = new URLSearchParams(location.search).get('nfc');

  return (
    <div>
      {guitarExists ? (
        <ViewGuitar server={server} tag_id={nfcTag} />
      ) : (
        <AddGuitar server={server} tag_id={nfcTag} />
      )}
    </div>
  );
};

const Home = () => (
  <div>
    <h1>Please use a valid URL or Add/View a guitar</h1>
  </div>
);

const MainApp = () => (
  <Router>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/nfc_tag" element={<App server="http://192.168.0.137:2000" />} />
    </Routes>
  </Router>
);

export default MainApp;