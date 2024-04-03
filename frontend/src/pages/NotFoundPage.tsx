import { Container, Typography, Box } from '@mui/material'

const NotFoundErrorPage = () => {
    return (
        <Container>
            <Box mt={5}>
                <Typography variant='h3' align='center' gutterBottom>
                    404 Not Found
                </Typography>
                <Typography variant='body1' align='center'>
                    The page you're looking for does not exist.
                </Typography>
            </Box>
        </Container>
    )
}

export default NotFoundErrorPage
