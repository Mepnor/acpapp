import { useRouter } from "next/router";
import { Button } from "@mui/material";
import LogoutIcon from '@mui/icons-material/Logout';
import { useEffect } from 'react';

const LogoutButton = () => {
  const router = useRouter();

  const handleLogout = () => {
    const token = localStorage.getItem("authToken");
    
    // Check if token exists
    if (token) {
      localStorage.removeItem("authToken");
      console.log("Token removed, user logged out.");
    } else {
      console.log("No token found.");
    }

    // Redirect to login page after 100ms delay
    setTimeout(() => {
      router.push("/login");
    }, 100);
  };

  return (
    <Button
      startIcon={<LogoutIcon />}
      onClick={handleLogout}
      sx={{
        color: 'black', // Set normal text color
        textTransform: 'none', // Disable uppercase transformation
      }}
    >
      Log Out
    </Button>
  );
};

export default LogoutButton;
