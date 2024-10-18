// Dashboard.js
import { useEffect, useState, useRef } from 'react';
import { Button } from '@mui/material'; // Import Button from MUI
import styles from './Dashboard.module.css'; // Import the CSS module
import Cookies from 'js-cookie'; // Import js-cookie to handle session cookies
import { useRouter } from 'next/router';

export default function Dashboard() {
  const router = useRouter();
  const [variable, setVariable] = useState({});
  const [imageSrc, setImageSrc] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(false); // Add state to check authentication
  const boxCanvasRef = useRef(null); // Reference for the "Boxes Collected" pie chart
  const distanceCanvasRef = useRef(null); // Reference for the "Distance Walked" pie chart
  const topBoxCanvasRef = useRef(null); // Reference for the "Top 3 Boxes Collected" pie chart
  const topDistanceCanvasRef = useRef(null); // Reference for the "Top 3 Longest Distance Walked" pie chart

  // Define colors for each robot globally so it can be used across the component
  const colors = ['#FFBF00', '#FF4500', '#32CD32', '#1E90FF', '#FFD700', '#4B0082', '#00FF7F', '#8B0000', '#FF1493', '#8A2BE2'];

  // Check authentication status on component mount
  useEffect(() => {
    const token = Cookies.get('session_token'); // Get the session token from cookies
    if (!token) {
      router.push('/login'); // Redirect to login if no token found
    } else {
      setIsAuthenticated(true); // Set the user as authenticated if token exists
    }
  }, [router]);

  useEffect(() => {
    if (!isAuthenticated) return; // Only run WebSocket if authenticated

    const socket = new WebSocket('ws://localhost:8000/ws/game_stats');

    socket.onmessage = function (event) {
      try {
        const data = JSON.parse(event.data);
        setVariable(data.stats); // Store game stats in the variable

        // Decode the image data
        const imageData = data.frame;
        setImageSrc('data:image/jpeg;base64,' + imageData); // Set image source
      } catch (error) {
        console.error('Error parsing JSON data:', error);
      }
    };

    socket.onerror = function (error) {
      console.error('WebSocket error:', error);
    };

    return () => socket.close();
  }, [isAuthenticated]);

  // Prepare data for the charts
  const robotNumbers = [...Array(10)].map((_, index) => index + 1);
  const boxesCollected = robotNumbers.map(
    (num) => variable[`Robot${num}C`] || 0
  );
  const pathsWalked = robotNumbers.map(
    (num) => variable[`Robot${num}P`] || 0
  );

  // Get the top 3 robots for most boxes collected
  const top3BoxesCollected = boxesCollected
    .map((collected, index) => ({ robot: `Robot${robotNumbers[index]}`, value: collected, color: colors[index] }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 3);

  // Get the top 3 robots for longest distance walked
  const top3DistancesWalked = pathsWalked
    .map((distance, index) => ({ robot: `Robot${robotNumbers[index]}`, value: distance, color: colors[index] }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 3);

  // Function to render pie chart based on data
  const drawPieChart = (ctx, data) => {
    let total = data.reduce((acc, cur) => acc + cur.value, 0);
    let startAngle = 0;
    data.forEach(({ value, color }) => {
      if (value > 0) {
        const sliceAngle = (value / total) * 2 * Math.PI;
        const endAngle = startAngle + sliceAngle;

        // Draw the pie slice
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.moveTo(150, 75); // Center of the pie chart
        ctx.arc(150, 75, 70, startAngle, endAngle);
        ctx.fill();

        // Move to the next slice
        startAngle = endAngle;
      }
    });
  };

  useEffect(() => {
    if (!isAuthenticated) return; // Only draw charts if authenticated

    // Draw the pie chart for Boxes Collected
    const boxCanvas = boxCanvasRef.current;
    const boxCtx = boxCanvas.getContext('2d');
    boxCtx.clearRect(0, 0, boxCanvas.width, boxCanvas.height);
    drawPieChart(boxCtx, robotNumbers.map((_, index) => ({
      value: boxesCollected[index],
      color: colors[index]
    })));
  }, [boxesCollected, isAuthenticated]);

  useEffect(() => {
    if (!isAuthenticated) return; // Only draw charts if authenticated

    // Draw the pie chart for Distance Walked
    const distanceCanvas = distanceCanvasRef.current;
    const distanceCtx = distanceCanvas.getContext('2d');
    distanceCtx.clearRect(0, 0, distanceCanvas.width, distanceCanvas.height);
    drawPieChart(distanceCtx, robotNumbers.map((_, index) => ({
      value: pathsWalked[index],
      color: colors[index]
    })));
  }, [pathsWalked, isAuthenticated]);

  useEffect(() => {
    if (!isAuthenticated) return; // Only draw charts if authenticated

    // Draw the pie chart for Top 3 Boxes Collected
    const topBoxCanvas = topBoxCanvasRef.current;
    const topBoxCtx = topBoxCanvas.getContext('2d');
    topBoxCtx.clearRect(0, 0, topBoxCanvas.width, topBoxCanvas.height);
    drawPieChart(topBoxCtx, top3BoxesCollected);
  }, [top3BoxesCollected, isAuthenticated]);

  useEffect(() => {
    if (!isAuthenticated) return; // Only draw charts if authenticated

    // Draw the pie chart for Top 3 Longest Distance Walked
    const topDistanceCanvas = topDistanceCanvasRef.current;
    const topDistanceCtx = topDistanceCanvas.getContext('2d');
    topDistanceCtx.clearRect(0, 0, topDistanceCanvas.width, topDistanceCanvas.height);
    drawPieChart(topDistanceCtx, top3DistancesWalked);
  }, [top3DistancesWalked, isAuthenticated]);

  // Function to submit data to the backend
  const handleSubmit = async () => {
    try {
      const token = Cookies.get('session_token'); // Get the session token from cookies
      if (!token) {
        alert('You need to be logged in to submit data');
        router.push('/login'); // Redirect to login if no token found
        return;
      }

      // Prepare the top 3 robots for "Box Collected"
      const top3BoxesCollectedData = boxesCollected
        .map((collected, index) => ({
          robot_id: index + 1,
          ranking: index + 1,  // Set ranking here
          rtype: "Box Collected",  // Set type of ranking (Box Collected)
          robottime: collected,
          robotpath: pathsWalked[index],
        }))
        .sort((a, b) => b.robottime - a.robottime)
        .slice(0, 3);

      // Prepare the top 3 robots for "Longest Distance"
      const top3DistancesWalkedData = pathsWalked
        .map((distance, index) => ({
          robot_id: index + 1,
          ranking: index + 1,  // Set ranking here
          rtype: "Longest Distance",  // Set type of ranking (Longest Distance)
          robottime: boxesCollected[index],
          robotpath: distance,
        }))
        .sort((a, b) => b.robotpath - a.robotpath)
        .slice(0, 3);

      const payload = {
        gameStats: {
          quantitys: variable.quantitys,
          time_spent: variable.time_spent,
          time_when_end: variable.time_when_end,
          target1: variable.target1,
          target2: variable.target2,
          Robot1C: variable.Robot1C || 0,
          Robot1P: variable.Robot1P || 0,
          Robot2C: variable.Robot2C || 0,
          Robot2P: variable.Robot2P || 0,
          Robot3C: variable.Robot3C || 0,
          Robot3P: variable.Robot3P || 0,
          Robot4C: variable.Robot4C || 0,
          Robot4P: variable.Robot4P || 0,
          Robot5C: variable.Robot5C || 0,
          Robot5P: variable.Robot5P || 0,
          Robot6C: variable.Robot6C || 0,
          Robot6P: variable.Robot6P || 0,
          Robot7C: variable.Robot7C || 0,
          Robot7P: variable.Robot7P || 0,
          Robot8C: variable.Robot8C || 0,
          Robot8P: variable.Robot8P || 0,
          Robot9C: variable.Robot9C || 0,
          Robot9P: variable.Robot9P || 0,
          Robot10C: variable.Robot10C || 0,
          Robot10P: variable.Robot10P || 0,
        },
        topPerformance: [...top3BoxesCollectedData, ...top3DistancesWalkedData],  // Send 6 top robots
      };

      // Send POST request with token in headers
      const response = await fetch("http://localhost:8000/api/submit_game_stats", {
        method: "POST",  // POST method
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`, // Add token for authentication
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        const result = await response.json();
        console.log("Submission success:", result);
        alert("Data submitted successfully!");
      } else {
        const errorData = await response.json();
        console.error("Error in submission:", JSON.stringify(errorData, null, 2));
        alert(`Error in submission: ${JSON.stringify(errorData, null, 2)}`);
      }
    } catch (error) {
      console.error("Error during fetch:", error);
      alert("An error occurred during data submission.");
    }
  };

  // Add a return to main button
  const handleReturnToMain = () => {
    router.push('/main');  // Navigate to main.js page
  };

  if (!isAuthenticated) {
    return null; // Don't render dashboard if not authenticated
  }

  return (
    <div className={styles.dashboardContainer}>
      <header className={styles.dashboardHeader}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Button
            variant="contained"
            color="primary"
            onClick={handleReturnToMain}
            sx={{ 
              backgroundColor: 'inherit', 
              '&:hover': { backgroundColor: '#444' },
              color: '#fff',
              marginRight: 'auto', // Push to the left side
            }}
          >
            Return to Main Menu
          </Button>
          <h1 style={{ textAlign: 'center', flexGrow: 1 }}>Game Dashboard</h1>
        </div>
      </header>

      {/* Game Display */}
      <div className={styles.gameDisplay}>
        <h2 className={styles.gameDisplayTitle}>
          Current Game Running Display
        </h2>
        {imageSrc && <img src={imageSrc} alt="Game Display" />}
        <div className={styles.gameStats}>
          <div>
            <h2>Current Quantity:</h2>
            <p>{variable.quantitys}/{variable.ObjectC}</p>
          </div>
          <div>
            <h2>Current TimeRun</h2>
            <p>{variable.time_spent} seconds</p>
          </div>
          <div>
            <h2>Time Spent To Finish</h2>
            <p>{variable.time_when_end} seconds</p>
          </div>
        </div>
      </div>

      {/* New container to hold the stats on the left and charts on the right */}
      <div className={styles.statsAndChartsContainer}>
        <div className={styles.statsContainer}>
          {/* Target 1 Supplied above Robot1 */}
          <div className={styles.statItem}>
            <h2>Target 1 Supplied</h2>
            <p>{variable.target1} blocks</p>
          </div>

          {/* Robot 1 */}
          <div className={styles.statItem}>
            <h2>Robot1</h2>
            <p>
              Box collected: {variable.Robot1C || 0} boxes | Path walked: {variable.Robot1P || 0} steps
            </p>
          </div>

          {/* Target 2 Supplied above Robot2 */}
          <div className={styles.statItem}>
            <h2>Target 2 Supplied</h2>
            <p>{variable.target2} blocks</p>
          </div>

          {/* Robot 2 */}
          <div className={styles.statItem}>
            <h2>Robot2</h2>
            <p>
              Box collected: {variable.Robot2C || 0} boxes | Path walked: {variable.Robot2P || 0} steps
            </p>
          </div>

          {/* The rest of the robots */}
          {robotNumbers.slice(2).map((robotNumber) => (
            <div key={robotNumber} className={styles.statItem}>
              <h2>{`Robot${robotNumber}`}</h2>
              <p>
                Box collected: {variable[`Robot${robotNumber}C`] || 0} boxes | Path walked: {variable[`Robot${robotNumber}P`] || 0} steps
              </p>
            </div>
          ))}
        </div>

        <div className={styles.chartsContainer}>
          {/* Chart 1: Boxes Collected (Pie Chart) */}
          <div className={styles.chartBox}>
            <h2 className={styles.chartTitle}>Robot Performance: Boxes Collected</h2>
            <canvas ref={boxCanvasRef} width="300" height="150" />
            <div className={styles.pieLegend}>
              {robotNumbers.map((robotNumber, index) => (
                <div key={robotNumber}>
                  <span style={{ color: colors[index] }}>■</span> Robot{robotNumber}: {boxesCollected[index]} boxes
                </div>
              ))}
            </div>
          </div>

          {/* Chart 2: Distance Walked (Pie Chart) */}
          <div className={styles.chartBox}>
            <h2 className={styles.chartTitle}>Robot Performance: Distance Walked</h2>
            <canvas ref={distanceCanvasRef} width="300" height="150" />
            <div className={styles.pieLegend}>
              {robotNumbers.map((robotNumber, index) => (
                <div key={robotNumber}>
                  <span style={{ color: colors[index] }}>■</span> Robot{robotNumber}: {pathsWalked[index]} steps
                </div>
              ))}
            </div>
          </div>

          {/* Combined Top 3 Chart for both Most Box Collected and Longest Distance Walked */}
          <div className={styles.chartBox}>
            <h2 className={styles.chartTitle}>Top Performance</h2>
            <div className={styles.topChartsContainer}>
              {/* Top 3 Boxes Collected */}
              <div className={styles.topChart}>
                <h3>Top 3 Most Boxes Collected</h3>
                <canvas ref={topBoxCanvasRef} width="150" height="150" />
                <div className={styles.pieLegend}>
                  {top3BoxesCollected.map((robotData, index) => (
                    <div key={index}>
                      <span style={{ color: robotData.color }}>■</span> {robotData.robot}: {robotData.value} boxes
                    </div>
                  ))}
                </div>
              </div>

              {/* Top 3 Longest Distance Walked */}
              <div className={styles.topChart}>
                <h3>Top 3 Longest Distance Walked</h3>
                <canvas ref={topDistanceCanvasRef} width="150" height="150" />
                <div className={styles.pieLegend}>
                  {top3DistancesWalked.map((robotData, index) => (
                    <div key={index}>
                      <span style={{ color: robotData.color }}>■</span> {robotData.robot}: {robotData.value} steps
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Submit Button for sending data to the database */}
      <button className={styles.submitButton} onClick={handleSubmit}>
        Submit Data
      </button>
    </div>
  );
}
