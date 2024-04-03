import { Container, Typography, Box } from '@mui/material';

const ForbiddenErrorPage = () => {
  return (
    <Container>
      <Box mt={5}>
        <Typography variant="h3" align="center" gutterBottom>
          403 Forbidden
        </Typography>
        <Typography variant="body1" align="center">
          You don't have permission to access this page.
        </Typography>
      </Box>
    </Container>
  );
}

export default ForbiddenErrorPage;
