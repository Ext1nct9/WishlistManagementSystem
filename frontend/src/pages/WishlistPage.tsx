import { Button, CircularProgress, Fab, Grid } from '@mui/material'
import WishlistUpdateDialog from '../features/wishlist/wishlistUpdateDialog'
import WishlistInfo from '../features/wishlist/wishlistInfo'
import AddIcon from '@mui/icons-material/Add'
import { useLocation, useParams } from 'react-router-dom'
import { useEffect } from 'react'
import { fetchLinkPermissions, fetchUserPermissions, fetchWishlist, setCurrentWishlist } from '../features/wishlist/wishlistSlice'
import { useAppDispatch, useAppSelector } from '../app/hooks'
import Permissions from '../features/permission/Permissions'
import { setPermissionOpened } from '../features/wishlist/wishlistSlice'
import { Item } from '../features/item/item'
import { ItemState } from '../features/item/itemState'

export const Wishlist = () => {
    const { wishlist_id } = useParams()
    // to get the link_permission_id
    const location = useLocation()
    const queryParams = new URLSearchParams(location.search)
    const link_permission_id = queryParams.get('link_permission_id')

    const dispatch = useAppDispatch()

    const loading = useAppSelector(state => state.wishlist.loading) // Fetch loading state
    const current = useAppSelector(state => state.wishlist.current) // Fetch current state
    const errorCode = useAppSelector(state => state.wishlist.errorCode) // Fetch error state
    const userWaiting = useAppSelector(state => state.wishlist?.current?.permissions?.user?.waiting) // Fetch user waiting state
    const linkWaiting = useAppSelector(state => state.wishlist?.current?.permissions?.link?.waiting) // Fetch link waiting state

    useEffect(() => {
        // Update wishlist state based on URL parameters
        dispatch(fetchWishlist({ wishlist_id, link_permission_id }))
    }, [wishlist_id, link_permission_id, dispatch])

    useEffect(() => {
        if (userWaiting) dispatch(fetchUserPermissions(wishlist_id))
        if (linkWaiting) dispatch(fetchLinkPermissions(wishlist_id))
    }, [userWaiting, linkWaiting, dispatch])

    // Handle redirection to error pages if necessary
    useEffect(() => {
        if (!loading && current === null) {
            // Fetch completed but nothing to display

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
    }, [loading, current, errorCode])

    const permissions_open = current?.permissions?.open
    const user_permissions = current?.permissions?.user
    const link_permissions = current?.permissions?.link

    const items: ItemState[] = [
        {
            item_id: '1',
            name: 'Item 1',
            description: 'Description 1',
            status: 'Status 1',
            link: 'https://www.google.com',
            comments: [],
        },
        {
            item_id: '2',
            name: 'Item 2',
            description: 'Description 2',
            status: 'Status 2',
            link: 'https://www.google.com',
            comments: [],
        },
        {
            item_id: '3',
            name: 'Item 3',
            description: 'Description 3',
            status: 'Status 3',
            link: 'https://www.google.com',
            comments: [],
        },
        {
            item_id: '4',
            name: 'Item 4',
            description: 'Description 4',
            status: 'Status 4',
            link: 'https://www.google.com',
            comments: [],
        },
        {
            item_id: '5',
            name: 'Item 5',
            description: 'Description 5',
            status: 'Status 5',
            link: 'https://www.google.com',
            comments: [],
        },
        {
            item_id: '6',
            name: 'Item 6',
            description: 'Description 6',
            status: 'Status 6',
            link: 'https://www.google.com',
            comments: [],
        },
    ]

    return (
        <Grid container spacing={2} p={4}>
            <Grid item xs={8}>
                {/* Wishlist Info */}
                {/* Conditionally render WishlistInfo or CircularProgress based on loading state */}
                {loading ? (
                    <div
                        style={{
                            display: 'flex',
                            justifyContent: 'center',
                            alignItems: 'center',
                            height: '200px',
                        }}
                    >
                        <CircularProgress />
                    </div>
                ) : (
                    <WishlistInfo />
                )}
            </Grid>
            <Grid item xs={4} flexShrink={-1}>
                <Grid container>
                    <Grid item xs={6}>
                        {/* button for tag */}
                        <Button variant='contained'>edit tags</Button>
                    </Grid>
                    <Grid item xs={6}>
                        {/* button for permission */}
                        <Button
                            variant='contained'
                            onClick={() => {
                                dispatch(setPermissionOpened(true))
                            }}
                        >
                            edit permission
                        </Button>
                    </Grid>
                </Grid>
            </Grid>
            <Grid
                item
                xs={12}
                style={{ marginLeft: '30px', marginRight: '30px' }}
            >
                {/* Items */}
                <Grid container spacing={2}>
                    {items.map(item => (
                        <Grid item xs={4}>
                            <Item {...item} />
                        </Grid>
                    ))}
                </Grid>
            </Grid>

            {/* Dialog to update wishlist name and description */}
            <WishlistUpdateDialog link_permission_id={link_permission_id} />

            {/* Dialog to manage permissions */}
            <Permissions
                wishlist_id={wishlist_id}
                open={permissions_open}
                user={user_permissions}
                link={link_permissions}
            />

            {/* Floating Action Button for adding items */}
            <Fab
                color='primary'
                aria-label='add'
                style={{ position: 'fixed', bottom: '16px', right: '16px' }}
            >
                <AddIcon />
            </Fab>
        </Grid>
    )
}

export default Wishlist
