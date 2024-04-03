import React from 'react'
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    Button,
} from '@mui/material'
import { red } from '@mui/material/colors'
import { useAppDispatch, useAppSelector } from '../../app/hooks'
import {
    setDialogOpen,
    updateDescription,
    updateName,
    updateWishlist,
} from './wishlistSlice'

const UpdateDialog = (props) => {
    const { link_permission_id } = props
    const currentWishlist = useAppSelector(state => state.wishlist.current)
    const dialogOpen = currentWishlist ? currentWishlist.openDialog : false
    const dispatch = useAppDispatch()

    let tempName = currentWishlist ? currentWishlist.name : ''
    let tempDescription = currentWishlist ? currentWishlist.description : ''
    const errorCode = useAppSelector(state => state.wishlist.errorCode)

    const handleCancelClick = () => {
        dispatch(setDialogOpen(false))
    }

    const handleDialogClose = () => {
        dispatch(setDialogOpen(false))
    }

    const handleSaveClick = () => {
        dispatch(
            updateWishlist({
                wishlist_id: currentWishlist ? currentWishlist.wishlist_id : '',
                name: tempName,
                description: tempDescription,
                link_permission_id: link_permission_id,
            })
        )
        console.log(errorCode)
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
        }
        // these need to be removed before submission
        dispatch(setDialogOpen(false))
        window.alert('Wishlist successfully updated')

    }

    const handleNameChange = e => {
        console.log('Name has been changed to:', e.target.value)
        tempName = e.target.value
    }

    const handleDescriptionChange = e => {
        console.log('Description has been changed to:', e.target.value)
        tempDescription = e.target.value
    }

    return (
        <Dialog open={dialogOpen} onClose={handleDialogClose}>
            <DialogTitle>Update Wishlist</DialogTitle>
            <DialogContent>
                <TextField
                    style={{ marginTop: '10px' }}
                    label='name'
                    fullWidth
                    defaultValue={
                        currentWishlist ? currentWishlist.name : 'None'
                    }
                    onChange={handleNameChange}
                />
                <TextField
                    style={{ marginTop: '10px' }}
                    label='description'
                    fullWidth
                    multiline
                    defaultValue={
                        currentWishlist ? currentWishlist.description : 'None'
                    }
                    onChange={handleDescriptionChange}
                />
            </DialogContent>
            <DialogActions>
                <Button
                    variant='contained'
                    onClick={handleCancelClick}
                    style={{ backgroundColor: red[700], color: 'white' }}
                >
                    Cancel
                </Button>
                <Button
                    variant='contained'
                    onClick={handleSaveClick}
                    color='primary'
                >
                    Save
                </Button>
            </DialogActions>
        </Dialog>
    )
}

export default UpdateDialog
