import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import { useLocation } from 'react-router-dom';

export default function ButtonAppBar() {
  const location = useLocation();

return (
    <Box sx={{ flexGrow: 1 } }>
        <AppBar position="static">
            <Toolbar sx={{ justifyContent: 'space-between' }}>
                <Button color="inherit" href="/">Listful</Button>
                {location.pathname === '/login' ? ( // To be changed to check if logged in or not TBD
                    <Button color="inherit">Logout</Button>
                ) : (
                    <Button color="inherit">Login</Button>
                )}
            </Toolbar>
        </AppBar>
    </Box>
);
}