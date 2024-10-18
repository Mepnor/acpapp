import React from 'react';
import Link from 'next/link';
import { AppBar, Toolbar, Typography, Button, Container, Paper, Box } from '@mui/material';
import LoginIcon from '@mui/icons-material/Login';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

const IndexPage = () => {
  return (
    <div style={styles.pageContainer}>
      {/* Header */}
      <AppBar position="static" style={styles.appBar}>
        <Toolbar style={styles.toolbar}>
          <Typography variant="h4" style={styles.headerTitle}>
            The Robot Simulation monitoring system
          </Typography>
        </Toolbar>
      </AppBar>

      {/* Main content */}
      <Container maxWidth="md" style={styles.contentContainer}>
        <Paper elevation={12} style={styles.paper}>
          <Typography variant="h3" align="center" gutterBottom style={styles.headerText}>
            Welcome!
          </Typography>
          <Typography variant="body1" align="center" style={styles.subText}>
            Click login/Register here to use our system!
          </Typography>
          <Box style={styles.buttonContainer}>
            <Link href="/login" passHref>
              <Button
                variant="contained"
                startIcon={<LoginIcon />}
                style={{ ...styles.button, backgroundColor: '#FFD700', color: '#000' }} // ปรับสีของปุ่ม Register ให้เหมือนกับ Login
              >
                Login
              </Button>
            </Link>

            <Link href="/register" passHref>
              <Button
                variant="contained"
                startIcon={<AccountCircleIcon />}
                style={{ ...styles.button, backgroundColor: '#FFD700', color: '#000' }} // ปรับสีให้ตรงกัน
              >
                Register
              </Button>
            </Link>
          </Box>
        </Paper>
      </Container>
    </div>
  );
};

// Styles for the page
const styles = {
  pageContainer: {
    display: 'flex',
    flexDirection: 'column',
    minHeight: '100vh',
    backgroundColor: '#1f1f1f', // Dark grey background for entire page
    justifyContent: 'center',
    alignItems: 'center',
    padding: '0 20px',
  },
  appBar: {
    backgroundColor: '#111', // Very dark background for header
    color: '#fff',
    padding: '10px 0',
    boxShadow: 'none', // Remove shadow for a flat design
  },
  toolbar: {
    display: 'flex',
    justifyContent: 'center',
  },
  headerTitle: {
    fontSize: '2rem',
    fontWeight: 'bold',
    color: '#FFD700', // Gold title color for more luxury feel
  },
  contentContainer: {
    marginTop: '60px',
    display: 'flex',
    justifyContent: 'center',
  },
  paper: {
    padding: '60px 40px',
    borderRadius: '20px',
    backgroundColor: '#292929', // Slightly lighter grey for the card
    color: '#fff', // White text for contrast
    maxWidth: '600px',
    textAlign: 'center',
    boxShadow: '0px 12px 24px rgba(0, 0, 0, 0.4)', // Add depth with shadow
  },
  headerText: {
    color: '#FFD700', // Gold header text
    fontWeight: 'bold',
    marginBottom: '20px',
  },
  subText: {
    color: '#CCC', // Light grey subtext
    marginBottom: '40px',
    fontSize: '1.1rem',
  },
  buttonContainer: {
    display: 'flex',
    justifyContent: 'space-around',
    marginTop: '20px',
  },
  button: {
    width: '160px',
    padding: '12px 0',
    fontSize: '16px',
    borderRadius: '30px',
    fontWeight: 'bold',
    textTransform: 'none',
    transition: 'transform 0.3s ease, background-color 0.3s ease',
    '&:hover': {
      transform: 'translateY(-3px)', // Move up on hover
    },
  },
};

export default IndexPage;
