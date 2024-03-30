import { Box, Button, Grid, Typography } from '@mui/material'
import { useAppDispatch, useAppSelector } from '../app/hooks'
import {
    setCurrentWishlist,
    setMockCurrentWishlist,
    setPermissionOpened,
} from '../features/wishlist/wishlistSlice'
import mockWishlist from '../features/wishlist/mockWishlist.json'
import Permissions from '../features/permission/Permissions'

const DevPage = () => {
    const state = useAppSelector(state => state)

    const dispatch = useAppDispatch()

    return (
        <Grid container p={10}>
            <Grid item xs={12}>
                <Typography variant='h1'>Dev Page</Typography>
            </Grid>
            <Grid item xs={12}>
                <Typography variant='body1'>This is the dev page.</Typography>
            </Grid>
            <Grid item xs={12}>
                <Typography variant='body1'>
                    The dev page is hidden from the user and will be removed for
                    production.
                </Typography>
            </Grid>
            <Grid item xs={12}>
                <Typography variant='body1'>
                    On the dev page, any developer can test new features by
                    either adding components to see how it looks like, or add
                    functionality buttons to do some test actions.
                </Typography>
            </Grid>

            <Grid item xs={12}>
                <Typography variant='h6'>Redux State</Typography>
            </Grid>
            <Grid item xs={12}>
                <Typography variant='subtitle1'>
                    Current Redux State:
                </Typography>
            </Grid>
            <Grid item xs={12}>
                <Box component='pre'>{JSON.stringify(state, null, 2)}</Box>
            </Grid>
            <Grid item xs={12}>
                <Button
                    variant='contained'
                    onClick={() =>
                        dispatch(setMockCurrentWishlist(mockWishlist))
                    }
                >
                    Set Current Wishlist To A Mock WishList
                </Button>
            </Grid>
            <Grid item xs={12}>
                <Button
                    variant='contained'
                    onClick={() => dispatch(setCurrentWishlist(null))}
                >
                    Set Current Wishlist To null
                </Button>
            </Grid>
            <Grid item xs={12}>
                <Typography variant='h6'>Permissions Component</Typography>
            </Grid>
            <Grid item xs={12}>
                {state.wishlist?.current ? (
                    <>
                        <Button
                            onClick={() => {
                                dispatch(setPermissionOpened(true))
                            }}
                        >
                            Open Permission Dialog
                        </Button>
                        <Permissions
                            open={state.wishlist?.current.permissions?.open}
                            wishlist_id={state.wishlist?.current.wishlist_id}
                            user={state.wishlist?.current.permissions?.user}
                            link={state.wishlist?.current.permissions?.link}
                        />
                    </>
                ) : (
                    <Typography variant='body1'>
                        The component cannot be displayed because there's no
                        current wishlist.
                    </Typography>
                )}
            </Grid>
        </Grid>
    )
}

export default DevPage
