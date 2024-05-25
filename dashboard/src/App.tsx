import React, { useEffect, useState } from 'react';
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
      console.log('event');
        setEvents({
          ...events,
          ...data
        });
    }
    function ping() {
      socket.emit('ping');
    }
    socket.on('dashEvent', dashEvent);

    socket.on('connect', ping);

    return () => {
      socket.off('dashEvent', dashEvent)
      socket.off('connect', ping)
    }
  }, [])
  return (
    <div className="App" style={{  minHeight: '100vh'}}>
        <Dash events = { events } />
    </div>
  );
}

export default App;
