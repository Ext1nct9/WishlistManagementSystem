import { Grid, Input, Typography } from '@mui/material'
import { Search } from '@mui/icons-material'

const HomePage = () => {
    return (
        <Grid container p={10} height='calc(100vh - 64px)' direction='column'>
            {/* Page height: 100vh (100% of the viewport's height) - 64px (app bar height) */}
            <Grid item xs={6}>
                <Typography
                    variant='h1'
                    align='center'
                    sx={{
                        fontWeight: 'bold',
                        color: '#1976d2',
                    }}
                >
                    Listful
                </Typography>
            </Grid>
            <Grid item xs={6}>
                <Input
                    fullWidth
                    placeholder='Search for a wishlist...'
                    startAdornment={<Search />}
                    onKeyDown={e => {
                        if (e.key === 'Enter') {
                            // enter key is pressed
                            // redirect to the wishlist page with the search query
                            window.location.href = `/wishlist/${e.target.value}`
                        }
                    }}
                />
            </Grid>
        </Grid>
    )
}

export default HomePage
