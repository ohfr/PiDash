import React, { useEffect, useState } from 'react';
import './App.css';
import { socket } from './socket';
import Dash from './Components/Dash';
import { DashEvent } from './types';

function App() {
  const [afr, setAfr] = useState(0);
  const [boost, setBoost] = useState(0);
  const [coolant, setCoolant] = useState(0);
  const [rpm, setRpm] = useState(0);
  const [airTemp, setAirTemp] = useState(0);
  const [speed, setSpeed] = useState(0);

  useEffect(() => {
    function dashEvent (data: DashEvent) {
        for (const [key, value] of Object.entries(data)) {
          switch (key){
              case 'boost': {
                  setBoost(value)
                  break;
              }
              case 'afr': {
                  setAfr(value)
                  break;
              }
              case 'coolant': {
                  setCoolant(value);
                  break;
              }
              case 'rpm': {
                  setRpm(value);
                  break;
              }
              case 'airTemp': {
                setAirTemp(value);
                break;
              }
              case 'speed': {
                setSpeed(value);
                break;
              }
              default:
                  return;
          }
      }
    }

    socket.on('dashEvent', dashEvent);

    return () => {
      socket.off('dashEvent', dashEvent)
    }
  }, [rpm, boost, afr, speed, airTemp, coolant])
  return (
    <div className="App" style={{  minHeight: '100vh'}}>
        <Dash events = { { boost, afr, coolant, rpm, airTemp, speed } } />
    </div>
  );
}

export default App;
