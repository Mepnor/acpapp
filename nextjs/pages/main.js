import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import Cookies from 'js-cookie';
import { useRouter } from 'next/router';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Container,
  Paper,
  Box,
  Grid,
  IconButton,
  Avatar,
} from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import LogoutIcon from '@mui/icons-material/Logout';

const Homepage = () => {
  const router = useRouter();
  const [userData, setUserData] = useState(null);

  // Handle Logout by clearing session or token
  const handleLogout = () => {
    Cookies.remove('session_token');
    router.push('/login');
  };

  useEffect(() => {
    const token = Cookies.get('session_token');
    if (!token) {
      router.push('/login');
    } else {
      fetch('/api/users/me', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
        .then(response => response.json())
        .then(data => {
          if (data) {
            setUserData(data);
          } else {
            Cookies.remove('session_token');
            router.push('/login');
          }
        })
        .catch(error => {
          console.error('Error fetching user data:', error);
          Cookies.remove('session_token');
          router.push('/login');
        });
    }
  }, [router]);

  return (
    <div style={styles.pageContainer}>
      {/* Header */}
      <AppBar position="static" style={{ backgroundColor: '#1a1a1a', color: '#fff' }}>
        <Toolbar>
          {/* Profile Icon with Link to Profile Page */}
          <IconButton
            edge="start"
            onClick={() => router.push('/profile')} // Navigates to the profile page on click
          >
            <Avatar
              alt={userData ? `${userData.first_name} ${userData.last_name}` : 'Profile Image'}
              src={userData && userData.avatar ? userData.avatar : '/default-avatar.jpg'}
              style={styles.profileImage}
            />
          </IconButton>

          {userData && (
            <Typography variant="h6" style={{ marginLeft: '10px' }}>
              Welcome {`${userData.first_name}`}!
            </Typography>
          )}

          <Typography variant="h5" style={{ flexGrow: 1 }}></Typography>

          <Button sx={{ color: 'white' }} startIcon={<LogoutIcon />} onClick={handleLogout}>
            Log Out
          </Button>
        </Toolbar>
      </AppBar>

      {/* Main content */}
      <Container style={{ marginTop: '40px', flexGrow: 1 }}>
        <Grid container spacing={4} style={{ height: '100%' }}>
          {/* Section for Pygame Overview */}
          <Grid item xs={12} md={6} style={{ display: 'flex', flexDirection: 'column' }}>
            <Paper elevation={4} style={styles.sectionPaper}>
              <Typography variant="h4" align="center" gutterBottom style={styles.sectionTitle}>
                Pygame Overview
              </Typography>
              {/* Inserted Pygame overview with spacing */}
              <Typography variant="body1" align="center" style={styles.sectionText}>
                This project implements a Python script using Pygame to simulate a maze-solving
                scenario, where multiple robots navigate through a grid-based environment. The goal
                is to demonstrate pathfinding and robot navigation using the A* search algorithm.
              </Typography>
              <Typography variant="body1" align="center" style={styles.sectionText}>
                <strong>Key elements of the Pygame simulation include:</strong>
              </Typography>
              <Typography variant="body1" align="center" style={styles.sectionText}>
                <strong>A* Search Algorithm:</strong> This algorithm is used to calculate the most
                efficient path for each robot to reach their respective targets. It takes into
                account the grid structure and obstacles in the environment, ensuring that robots
                avoid barriers while finding the shortest path.
              </Typography>
              <Typography variant="body1" align="center" style={styles.sectionText}>
                <strong>Robot Simulation:</strong> Each robot is assigned to specific tasks such as
                collecting boxes or covering a certain distance. Performance metrics such as the
                number of boxes collected and the distance covered are tracked.
              </Typography>
              <Typography variant="body1" align="center" style={styles.sectionText}>
                <strong>Real-time Game Stats:</strong> The Pygame simulation sends real-time data via
                WebSockets, including robot statistics and a visual feed. These stats are displayed
                on the dashboard in the form of charts, showing the robots’ performance in terms of
                both box collection and distance walked.
              </Typography>
              <Typography variant="body1" align="center" style={styles.sectionText}>
                <strong>Visualization and Game Display:</strong> The dashboard allows users to see
                real-time robot actions within the maze, displayed as an image. The performance of
                each robot is visualized through pie charts and ranking tables, highlighting the
                top-performing robots in various categories (e.g., most boxes collected, longest
                distance walked).
              </Typography>
              <Typography variant="body1" align="center" style={styles.sectionText}>
                This simulation showcases how algorithms like A* can be applied in practical
                robotics scenarios and how performance metrics can be tracked and analyzed in
                real-time.
              </Typography>
            </Paper>
            <Box style={{ flexGrow: 1 }} /> {/* This helps push the Pygame Overview box down */}
          </Grid>

          {/* Access Dashboard and New Box */}
          <Grid item xs={12} md={6} style={{ display: 'flex', flexDirection: 'column' }}>
            <Grid container direction="column" spacing={4} style={{ flexGrow: 1 }}>
              <Grid item>
                <Paper elevation={4} style={styles.sectionPaper}>
                  <Typography variant="h5" align="center" gutterBottom style={styles.sectionTitle}>
                    Access Dashboard / Pygame viewer
                  </Typography>
                  <Box style={styles.dashboardButtonContainer}>
                    <IconButton
                      style={styles.dashboardButton}
                      onClick={() => router.push('/DASHBOARD')}
                    >
                      <DashboardIcon fontSize="large" />
                    </IconButton>
                  </Box>
                </Paper>
              </Grid>

              {/* New Box Below Access Dashboard */}
              <Grid item>
                <Paper elevation={4} style={styles.additionalInfoPaper}>
                  <Typography variant="h4" align="center" gutterBottom style={styles.sectionTitle}>
                    Additional Information
                  </Typography>
                  <Typography variant="body1" align="center" style={styles.sectionText}>
                    <strong>Performance Metrics:</strong> In the dashboard, the performance metrics
                    for each robot are displayed through pie charts and rankings. These metrics include
                    boxes collected and the distance covered by each robot. It offers real-time insight
                    into how effectively the robots are performing their tasks.
                  </Typography>
                  <Typography variant="body1" align="center" style={styles.sectionText}>
                    <strong>Real-time WebSocket Communication:</strong> The Pygame simulation sends
                    live data updates to the dashboard using WebSocket communication. This allows the
                    dashboard to update continuously and display the latest robot performance data
                    without the need for manual refreshes.
                  </Typography>
                  <Typography variant="body1" align="center" style={styles.sectionText}>
                    <strong>Data Submission:</strong> Once the simulation completes, the collected
                    data, including game statistics and top-performing robots, can be submitted
                    directly to a backend server for further analysis or reporting.
                  </Typography>
                  <Typography variant="body1" align="center" style={styles.sectionText}>
                    <strong>Learning Outcome:</strong> This project not only demonstrates the power
                    of algorithms like A* for solving real-world problems but also showcases how data
                    visualization and live updates can enhance user experience in interactive applications.
                  </Typography>
                </Paper>
              </Grid>
            </Grid>
            <Box style={{ flexGrow: 1 }} /> {/* This helps push the Additional Information box down */}
          </Grid>
        </Grid>
      </Container>

      {/* Footer */}
      <Box style={styles.footer}>
        <Paper elevation={4} style={styles.sectionPaper}>
          <Typography variant="h6" align="center" gutterBottom>
            Contact Us
          </Typography>
          <Typography align="center">Email: info@example.com | Phone: (123) 456-7890</Typography>
          <Typography align="center">123 Game Street, Python City, PY 12345</Typography>
        </Paper>
      </Box>
    </div>
  );
};

// Styles
const styles = {
  pageContainer: {
    display: 'flex',
    flexDirection: 'column',
    minHeight: '100vh',
    backgroundColor: '#1e1e1e',
    color: '#ffffff',
  },
  profileImage: {
    width: 40,
    height: 40,
  },
  sectionPaper: {
    padding: '30px',
    backgroundColor: '#2b2b2b',
    color: '#fff',
    borderRadius: '40px',
    textAlign: 'center',
  },
  additionalInfoPaper: {
    padding: '82px',
    backgroundColor: '#2b2b2b',
    color: '#fff',
    borderRadius: '40px',
    textAlign: 'center',
  },
  sectionTitle: {
    fontSize: '24px',
    color: '#FFBF00',
    fontWeight: 'bold',
  },
  sectionText: {
    marginTop: '30px',
    color: '#ccc',
  },
  dashboardButtonContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  dashboardButton: {
    margin: '20px',
    backgroundColor: '#FFBF00',
    color: '#fff',
    borderRadius: '80%',
    padding: '20px',
    transition: 'transform 0.3s ease',
  },
  footer: {
    marginTop: 'auto',
    backgroundColor: '#1e1e1e',
    padding: '8px',
    color: '#fff',
  },
};

export default Homepage;
