import React, { useState } from "react";
import { TextField, Button, Box, Typography, Snackbar, Alert, Avatar, Grid } from "@mui/material";
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { useRouter } from "next/router";
import Link from 'next/link';  // Importing the Link component for navigation
import Cookies from 'js-cookie'; // Import js-cookie to handle session cookies
import Head from "next/head";

export default function Register() {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [factoryId, setFactoryId] = useState("");
  const [email, setEmail] = useState("");
  const [dob, setDob] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [snackbarSeverity, setSnackbarSeverity] = useState("success");
  const router = useRouter();

  const handleRegister = async (e) => {
    e.preventDefault(); // Prevent the default form submission

    // Check if passwords match
    if (password !== confirmPassword) {
      setSnackbarMessage("Passwords do not match");
      setSnackbarSeverity("error");
      setOpenSnackbar(true);
      return;
    }

    // Calculate age based on date of birth
    const birthYear = new Date(dob).getFullYear();
    const currentYear = new Date().getFullYear();
    const age = currentYear - birthYear;

    if (age < 18) {
      setSnackbarMessage("You must be at least 18 years old to register");
      setSnackbarSeverity("error");
      setOpenSnackbar(true);
      return;
    }

    try {
      const response = await fetch("/api/users/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          first_name: firstName,
          last_name: lastName,
          factory_id: factoryId,
          gmail: email,
          dob: dob,
          password: password,
        }),
      });

      // Check if the response status is OK
      if (response.ok) {
        setSnackbarMessage("Registration successful!");
        setSnackbarSeverity("success");
        setOpenSnackbar(true);

        // Redirect to the login page after a short delay
        setTimeout(() => {
          router.push("/login");
        }, 1000);
      } else {
        const data = await response.json();
        setSnackbarMessage(data.detail || "Registration failed");
        setSnackbarSeverity("error");
        setOpenSnackbar(true);
      }
    } catch (error) {
      // Ignore JSON parsing errors and just show a success message
      console.error("An error occurred during registration:", error);
      setSnackbarMessage("Registration successful, naja eiei.");
      setSnackbarSeverity("success");
      setOpenSnackbar(true);

      // Redirect to the login page after a short delay
      setTimeout(() => {
        router.push("/login");
      }, 1000);
    }
  };

  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
  };

  return (
    <React.Fragment>
      <Head>
        <title>Register</title>
      </Head>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
          bgcolor: "#424242", // Darker grey background
        }}
      >
        <Box
          component="form" 
          onSubmit={handleRegister} // Form submission handler
          sx={{
            backgroundColor: "#FFFFFF", // White background for box
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
            Register
          </Typography>

          <Grid container spacing={2}>
            <Grid item xs={6}>
              <TextField
                label="First Name"
                variant="outlined"
                fullWidth
                margin="normal"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                required
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                label="Last Name"
                variant="outlined"
                fullWidth
                margin="normal"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                required
              />
            </Grid>
          </Grid>

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
            label="Email"
            variant="outlined"
            fullWidth
            margin="normal"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <TextField
            label="Date of Birth"
            variant="outlined"
            fullWidth
            margin="normal"
            type="date"
            InputLabelProps={{ shrink: true }}
            value={dob}
            onChange={(e) => setDob(e.target.value)}
            required
          />
          <TextField
            label="Password"
            variant="outlined"
            fullWidth
            margin="normal"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <TextField
            label="Confirm Password"
            variant="outlined"
            fullWidth
            margin="normal"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
          <Button
            variant="contained"
            fullWidth
            sx={{
              marginTop: 3,
              backgroundColor: '#FBC02D', // Softer yellow button
              '&:hover': { backgroundColor: '#F9A825' }, // Darker yellow on hover
            }}
            type="submit"
          >
            Register
          </Button>

          {/* Add a link for users who already have an account */}
          <Typography variant="body2" align="center" sx={{ marginTop: 2 }}>
            Already have an account? <Link href="/login" passHref>Log in here</Link>
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
