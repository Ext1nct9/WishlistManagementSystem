import { Typography, Button, Grid } from '@mui/material';
import { Link } from 'react-router-dom';

const DefaultErrorPage = () => {
  return (
    <Grid
      container
      spacing={2}
      direction="column"
      justifyContent="center"
      alignItems="center"
      style={{ height: '100vh' }}
    >
      <Grid item>
        <Typography variant="h4" gutterBottom>
          Oops! Something went wrong.
        </Typography>
      </Grid>
      <Grid item>
        <Typography variant="body1" paragraph>
          We apologize for the inconvenience. Please try again later.
        </Typography>
      </Grid>
      <Grid item>
        <Button variant="contained" color="primary" component={Link} to="/">
          Go to Home
        </Button>
      </Grid>
    </Grid>
  );
};

export default DefaultErrorPage;
