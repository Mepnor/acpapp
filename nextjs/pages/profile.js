import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Cookies from 'js-cookie';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  CircularProgress,
  IconButton,
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import styles from './Profile.module.css';

const Profile = () => {
  const router = useRouter();
  const [userData, setUserData] = useState(null);
  const [editedData, setEditedData] = useState({});
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [saving, setSaving] = useState(false);

  // Fetch user data from the backend (based on session token)
  const fetchUserData = async (token) => {
    try {
      const response = await fetch('http://localhost:8000/api/users/me', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setUserData(data);
        setEditedData(data); // Initialize editedData with fetched user data
      } else {
        console.error('Error fetching user data:', response.statusText);
        // Remove the token and redirect to login if unauthorized
        if (response.status === 401 || response.status === 403) {
          Cookies.remove('session_token');
          router.push('/login');
        }
      }
    } catch (error) {
      console.error('Error fetching user data:', error);
      Cookies.remove('session_token');
      router.push('/login');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const token = Cookies.get('session_token');
    if (!token) {
      router.push('/login');
    } else {
      fetchUserData(token);
    }
  }, [router]);

  const handleInputChange = (e) => {
    setEditedData({
      ...editedData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSaveChanges = async () => {
    // Basic validation for password change
    if (newPassword && newPassword !== confirmNewPassword) {
      alert("New passwords don't match");
      return;
    }

    setSaving(true);
    const token = Cookies.get('session_token');
    if (!token) {
      router.push('/login');
      return;
    }

    try {
      const formData = new FormData();
      formData.append('first_name', editedData.first_name);
      formData.append('last_name', editedData.last_name);
      formData.append('gmail', editedData.gmail);
      formData.append('dob', editedData.dob);

      // Only send password data if a change is requested
      if (oldPassword && newPassword) {
        formData.append('old_password', oldPassword);
        formData.append('new_password', newPassword);
      }

      const response = await fetch('http://localhost:8000/api/users/update', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        const updatedData = await response.json();
        setUserData(updatedData);
        setEditedData(updatedData);
        setIsEditing(false);
        console.log('Profile updated successfully:', updatedData);
      } else {
        console.error('Error updating profile:', response.statusText);
      }
    } catch (error) {
      console.error('Error updating profile:', error);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh" sx={{ bgcolor: "#424242" }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!userData) {
    return <p>Failed to load user data. Please try again later.</p>;
  }

  return (
    <Box
      className={styles.profileContainer}
      sx={{
        bgcolor: "#424242", // Darker grey background for the full page
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Paper
        className={styles.profileCard}
        sx={{
          padding: 4,
          bgcolor: "#FFFFFF", // White background for the box
          borderRadius: 2,
          boxShadow: 3,
          width: "100%",
          maxWidth: "500px",
          position: "relative",
        }}
      >
        {/* Return to Menu Button */}
        <IconButton
          aria-label="Return to Menu"
          onClick={() => router.push('/main')}
          sx={{
            position: 'absolute',
            top: 16,
            left: 16,
            backgroundColor: '#FBC02D', // Yellow background for the button
            '&:hover': { backgroundColor: '#F9A825' }, // Darker yellow on hover
          }}
        >
          <ArrowBackIcon />
        </IconButton>

        <Typography
          variant="h4"
          align="center"
          gutterBottom
          sx={{ color: "#1E90FF" }} // Blue title color to match dashboard theme
        >
          Profile Information
        </Typography>

        {/* Displaying User Information */}
        <Box className={styles.profileInfo}>
          <TextField
            label="First Name"
            name="first_name"
            value={editedData.first_name || ''}
            onChange={handleInputChange}
            InputProps={{
              readOnly: !isEditing,
            }}
            variant="outlined"
            fullWidth
            margin="normal"
          />
          <TextField
            label="Last Name"
            name="last_name"
            value={editedData.last_name || ''}
            onChange={handleInputChange}
            InputProps={{
              readOnly: !isEditing,
            }}
            variant="outlined"
            fullWidth
            margin="normal"
          />
          <TextField
            label="Factory ID"
            name="factory_id"
            value={editedData.factory_id || ''}
            InputProps={{
              readOnly: true,
            }}
            variant="outlined"
            fullWidth
            margin="normal"
          />
          <TextField
            label="Email"
            name="gmail"
            value={editedData.gmail || ''}
            onChange={handleInputChange}
            InputProps={{
              readOnly: !isEditing,
            }}
            variant="outlined"
            fullWidth
            margin="normal"
          />
          <TextField
            label="Date of Birth"
            name="dob"
            type="date"
            value={editedData.dob || ''}
            onChange={handleInputChange}
            InputLabelProps={{
              shrink: true,
            }}
            InputProps={{
              readOnly: !isEditing,
            }}
            variant="outlined"
            fullWidth
            margin="normal"
          />

          {/* Password Fields */}
          {isEditing && (
            <>
              <TextField
                label="Old Password"
                type="password"
                value={oldPassword}
                onChange={(e) => setOldPassword(e.target.value)}
                variant="outlined"
                fullWidth
                margin="normal"
              />
              <TextField
                label="New Password"
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                variant="outlined"
                fullWidth
                margin="normal"
              />
              <TextField
                label="Confirm New Password"
                type="password"
                value={confirmNewPassword}
                onChange={(e) => setConfirmNewPassword(e.target.value)}
                variant="outlined"
                fullWidth
                margin="normal"
              />
            </>
          )}
        </Box>

        {/* Edit and Save Buttons */}
        <Box display="flex" justifyContent="center" mt={2}>
          {isEditing ? (
            <>
              <Button
                variant="contained"
                sx={{
                  backgroundColor: "#FBC02D", // Yellow button to match the theme
                  '&:hover': { backgroundColor: '#F9A825' }, // Darker yellow on hover
                  marginRight: 2,
                }}
                onClick={handleSaveChanges}
                disabled={saving}
              >
                {saving ? 'Saving...' : 'Save Changes'}
              </Button>
              <Button
                variant="outlined"
                color="secondary"
                onClick={() => {
                  setIsEditing(false);
                  setEditedData(userData);
                }}
              >
                Cancel
              </Button>
            </>
          ) : (
            <Button
              variant="contained"
              sx={{
                backgroundColor: "#FBC02D", // Yellow button to match the theme
                '&:hover': { backgroundColor: '#F9A825' }, // Darker yellow on hover
              }}
              onClick={() => setIsEditing(true)}
            >
              Edit Profile
            </Button>
          )}
        </Box>
      </Paper>
    </Box>
  );
};

export default Profile;
