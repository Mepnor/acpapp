import React from 'react';
import Link from 'next/link';
import { AppBar, Toolbar, Typography, Button, Container, Paper, Box, Grid, IconButton } from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import LogoutIcon from '@mui/icons-material/Logout';

const Homepage = () => {
  const handleLogout = () => {
    // Handle Log Out by clearing session or token
    console.log('User logged out');
    // Optionally redirect to login page
    window.location.href = '/login';
  };

  return (
    <div style={styles.pageContainer}>
      {/* Header */}
      <AppBar position="static" style={{ backgroundColor: '#1a1a1a', color: '#fff' }}>
        <Toolbar>
          <Typography variant="h5" style={{ flexGrow: 1 }}>
            Skiddadle
          </Typography>
          <Button sx={{ color: 'white' }} startIcon={<LogoutIcon />} onClick={handleLogout}>
            Log Out
          </Button>
        </Toolbar>
      </AppBar>

      {/* Main content */}
      <Container style={{ marginTop: '40px', flexGrow: 1 }}>
        <Grid container spacing={4}>
          {/* Section for Pygame Overview */}
          <Grid item xs={12} md={6}>
            <Paper elevation={4} style={styles.sectionPaper}>
              <Typography variant="h4" align="center" gutterBottom style={styles.sectionTitle}>
                Pygame Overview
              </Typography>
              <Typography variant="body1" align="center" gutterBottom style={{ fontStyle: 'italic' }}>
              </Typography>

              {/* Placeholder for Image */}
              <Box style={styles.imagePlaceholder}>
                <Typography>Placeholder for Pygame Image</Typography>
              </Box>

              {/* Description */}
              <Typography variant="body1" align="center" style={styles.sectionText}>
                This Python script implements the A* search algorithm to navigate robots through a grid-based environment, efficiently finding the shortest path between a source and destination while avoiding obstacles. The grid is represented as a 2D array where cells are either passable or blocked, and the algorithm calculates the optimal path using both the actual movement cost (g) and a heuristic estimate (h) of the distance to the target. Key features include a Cell class to store movement costs, validation functions to check cell states, and a path tracing method to reconstruct the final route. Additionally, the script provides a function for determining the shortest paths for robots to collect objects, making it ideal for applications in game development, robotics simulations, and AI learning scenarios.
              </Typography>
            </Paper>
          </Grid>

          {/* Access Dashboard and New Box */}
          <Grid item xs={12} md={6}>
            <Grid container direction="column" spacing={4}>
              <Grid item>
                <Paper elevation={4} style={styles.sectionPaper}>
                  <Typography variant="h5" align="center" gutterBottom style={styles.sectionTitle}>
                    Access Dashboard
                  </Typography>
                  <Box style={styles.dashboardButtonContainer}>
                    <IconButton
                      style={styles.dashboardButton}
                      onClick={() => window.location.href = '/DASHBOARD'}
                    >
                      <DashboardIcon fontSize="large" />
                    </IconButton>
                    <Typography variant="h6" align="center">
                      Go to Dashboard
                    </Typography>
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
                    This section can be used to provide any additional information or features that you want to highlight. It could contain useful resources, links to tutorials, or anything that complements the dashboard and overview sections.
                  </Typography>
                </Paper>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Container>

      {/* Footer */}
      <Box style={styles.footer}>
        <Paper elevation={4} style={styles.sectionPaper}>
          <Typography variant="h6" align="center" gutterBottom>
            Contact Us
          </Typography>
          <Typography align="center">
            Email: info@example.com | Phone: (123) 456-7890
          </Typography>
          <Typography align="center">
            123 Game Street, Python City, PY 12345
          </Typography>
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
    backgroundColor: '#1e1e1e', // Set a dark background color matching the sections
    color: '#ffffff',
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
  imagePlaceholder: {
    height: '200px',
    backgroundColor: '#3d3d3d',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: '20px',
    borderRadius: '30px',
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
