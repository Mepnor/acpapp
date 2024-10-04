import React, { useState } from "react";
import { TextField, Button, Box, Typography, Snackbar, Alert, Avatar } from "@mui/material";
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { useRouter } from "next/router";
import Head from "next/head";

export default function Login() {
  const [gmail, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState('error');
  const [factoryid, setFactoryid] = useState('');
  const router = useRouter();

  const handleLogin = async () => {
    if (!factoryid || !password) {
      setSnackbarMessage('Please enter both FactoryID and password');
      setSnackbarSeverity('warning');
      setOpenSnackbar(true);
      return;
    }
  
    try {
      const response = await fetch('/api/users/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          factory_id: factoryid,
          password_hash: password,
        }),
      });
  
      const data = await response.json();
  
      if (!response.ok) {
        const errorMessage = data.detail 
          ? typeof data.detail === 'string' 
            ? data.detail 
            : data.detail.msg || 'Login failed' 
          : 'Login failed';
        setSnackbarMessage(errorMessage);
        setSnackbarSeverity('error');
        setOpenSnackbar(true);
        return;
      }
  
      setSnackbarMessage('Login successful!');
      setSnackbarSeverity('success');
      setOpenSnackbar(true);
  
      setTimeout(() => {
        router.push("/main");
      }, 1000);
    } catch (error) {
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
            label="factory_ID"
            variant="outlined"
            fullWidth
            margin="normal"
            value={factoryid}
            onChange={(e) => setFactoryid(e.target.value)}
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

          <Typography variant="body2" color="text.secondary" align="center" sx={{ marginTop: 2 }}>
            Don't have an account?{" "}
            <a href="/register" style={{
              color: "#FFC107",
              textDecoration: "none",
              fontWeight: 'bold',
              fontSize: '1.2rem',
            }}>Sign Up</a>
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
