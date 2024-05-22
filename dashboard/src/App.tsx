import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import { socket } from './socket';
import Dash from './Components/Dash';
import { DashEvent } from './types';

function App() {
  const [events, setEvents] = useState<DashEvent>({
    speed: 0,
    rpm: 0,
    coolant: 0,
    afr: 0,
    boost: 0,
    airTemp: 0
  });
  useEffect(() => {
    function dashEvent (data: DashEvent) {
        setEvents({
          ...events,
          ...data
        });
    }
    socket.on('dashEvent', dashEvent);

    return () => {
      socket.off('dashEvent', dashEvent)
    }
  }, [])
  return (
    <div className="App" style={{  minHeight: '100vh'}}>
        <Dash events = { events } />
    </div>
  );
}

export default App;
