import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [variable, setvariable] = useState({});

  useEffect(() => {
    // Connect to the FastAPI WebSocket
    const socket = new WebSocket('ws://localhost:8000/ws/game_stats');

    // Listen for messages from the WebSocket
    socket.onmessage = function (event) {
      const data = JSON.parse(event.data);
      console.log("Received data:", data);  // Debug message
      setvariable(data);
    };

    // Cleanup WebSocket connection on component unmount
    return () => socket.close();
  }, []);

  return (
    <div>
      <h1>Game Dashboard</h1>
      <p>quantity: {variable.quantitys}</p>
      <p>Time_spent: {variable.time_spent}</p>
    </div>
  );
}
