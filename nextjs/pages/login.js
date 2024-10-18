import React, { useState } from "react";
import { TextField, Button, Box, Typography, Snackbar, Alert, Avatar } from "@mui/material";
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { useRouter } from "next/router";
import Head from "next/head";
import Cookies from "js-cookie";  // Using js-cookie to handle authentication token
import Link from 'next/link';  // Import Link from next.js for navigation

export default function Login() {
  const [factoryId, setFactoryId] = useState('');  // Updated variable name
  const [password, setPassword] = useState("");
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState('error');
  const [captchaAnswer, setCaptchaAnswer] = useState('');
  const [captchaQuestion, setCaptchaQuestion] = useState('');
  const [captchaSolution, setCaptchaSolution] = useState(null);
  const router = useRouter();

  // Generate a simple math-based CAPTCHA
  const generateCaptcha = () => {
    const num1 = Math.floor(Math.random() * 100) + 1;
    const num2 = Math.floor(Math.random() * 100) + 1;
    setCaptchaQuestion(`What is ${num1} plus ${num2}?`);
    setCaptchaSolution(num1 + num2);
  };

  // When the page loads, generate a CAPTCHA question
  React.useEffect(() => {
    generateCaptcha();
  }, []);

  const handleLogin = async () => {
    // Validate client-side input first
    if (!factoryId) {
      setSnackbarMessage('Please input factory ID');
      setSnackbarSeverity('error');
      setOpenSnackbar(true);
      return;
    }
  
    if (!password) {
      setSnackbarMessage('Please input a password');
      setSnackbarSeverity('error');
      setOpenSnackbar(true);
      return;
    }
  
    // Check CAPTCHA answer on the frontend only
    if (captchaAnswer !== captchaSolution.toString()) {
      setSnackbarMessage('Incorrect CAPTCHA answer');
      setSnackbarSeverity('error');
      setOpenSnackbar(true);
      return;
    }
  
    try {
      // If CAPTCHA is correct, proceed with the login request
      const response = await fetch('/api/users/LoginWithToken', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          'username': factoryId,
          'password': password,
        }),
      });
  
      const data = await response.json();
      console.log('Login Response Data:', data); // Log for debugging
  
      if (!response.ok) {
        setSnackbarMessage(data.detail || 'Login failed');
        setSnackbarSeverity('error');
        setOpenSnackbar(true);
        return;
      }
  
      // Success Case: Save token and redirect
      Cookies.set('session_token', data.access_token, { expires: 1, path: '/' });
      setSnackbarMessage('Login successful!');
      setSnackbarSeverity('success');
      setOpenSnackbar(true);
  
      setTimeout(() => {
        router.push("/main");  // Redirect to the main page after login
      }, 1000);
  
    } catch (error) {
      console.error('Login error:', error);  // Log the actual error for debugging
      setSnackbarMessage('An error occurred during login');
      setSnackbarSeverity('error');
      setOpenSnackbar(true);
    }
  };
  
  
  
  

  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
  };

  return (
    <React.Fragment>
      <Head>
        <title>Login</title>
      </Head>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
          bgcolor: "#424242",
        }}
      >
        <Box
          sx={{
            backgroundColor: "#FFFFFF",
            padding: 4,
            borderRadius: 2,
            boxShadow: 3,
            width: "100%",
            maxWidth: "400px",
            textAlign: "center",
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: '#FFC107', margin: '0 auto' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography variant="h5" align="center" gutterBottom>
            Login
          </Typography>

          <TextField
            label="Factory ID"
            variant="outlined"
            fullWidth
            margin="normal"
            value={factoryId}
            onChange={(e) => setFactoryId(e.target.value)}
            required
          />

          <TextField
            label="Password"
            variant="outlined"
            type="password"
            fullWidth
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          {/* CAPTCHA Challenge */}
          <Typography variant="body1" align="center" gutterBottom>
            {captchaQuestion}
          </Typography>
          <TextField
            label="Answer"
            variant="outlined"
            fullWidth
            margin="normal"
            value={captchaAnswer}
            onChange={(e) => setCaptchaAnswer(e.target.value)}
            required
          />

          <Button
            variant="contained"
            fullWidth
            sx={{
              marginTop: 3,
              backgroundColor: '#FBC02D',
              '&:hover': { backgroundColor: '#F9A825' },
            }}
            onClick={handleLogin}
          >
            Login
          </Button>

          {/* Add a link for registration if the user doesn't have an account */}
          <Typography variant="body2" align="center" sx={{ marginTop: 2 }}>
            Don't have an account? <Link href="/register" passHref>Register here</Link>
          </Typography>
        </Box>
      </Box>

      <Snackbar
        open={openSnackbar}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbarSeverity} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </React.Fragment>
  );
}
