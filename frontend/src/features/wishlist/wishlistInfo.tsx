import React from 'react'
import { Typography, Container, Grid, Box, IconButton } from '@mui/material'
import { useAppDispatch, useAppSelector } from '../../app/hooks'
import { deleteWishlist, setDialogOpen } from './wishlistSlice'
import EditOutlinedIcon from '@mui/icons-material/EditOutlined'
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined'

const WishlistInfo = () => {
    const currentWishlist = useAppSelector(state => state.wishlist.current)
    const errorCode = useAppSelector(state => state.wishlist.errorCode)
    const dispatch = useAppDispatch()

    const handleUpdateClick = () => {
        dispatch(setDialogOpen(true))
    }

    const handleDeleteClick = () => {
        dispatch(
            deleteWishlist({
                wishlist_id: currentWishlist ? currentWishlist.wishlist_id : '',
            })
        )
        console.error (errorCode)
        if (errorCode !== null) {
            console.log('Error code:', errorCode)
            let redirectPath
            if (errorCode === '403') {
                redirectPath = '/error/403'
            } else if (errorCode === '404') {
                redirectPath = '/error/404'
            } else {
                redirectPath = '/error/default' // You can define a default error page if needed
            }
            window.location.href = redirectPath
        }else{
            window.alert('Wishlist successfully deleted')
            window.location.href = '/'
        }
        
    }


    return (
        <Container
            maxWidth='md'
            style={{ marginLeft: '30px' }}
        >
            <Grid container spacing={2}>
                <Grid item xs={12} style={{ padding: '10px' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Typography
                            variant='h5'
                            sx={{ flexGrow: 0.1, fontWeight: 'bold' }}
                        >
                            {currentWishlist ? currentWishlist.name : 'None'}
                        </Typography>
                        <IconButton onClick={handleUpdateClick}>
                            <EditOutlinedIcon />
                        </IconButton>
                        <IconButton onClick={handleDeleteClick}>
                            <DeleteOutlinedIcon />
                        </IconButton>
                    </Box>
                    <Typography variant='subtitle1' style={{ marginTop: '8px' }}>
                        {currentWishlist ? currentWishlist.description : 'None'}
                    </Typography>
                </Grid>
            </Grid>
        </Container>
    )
}

export default WishlistInfo
