import { Box, Typography } from '@mui/material'
import { useAppDispatch, useAppSelector } from '../../app/hooks'
import { fetchWishlist } from './wishlistSlice'

const FetchWishlist = () => {
    const currentWishlist = useAppSelector(state => state.wishlist.current)
    const dispatch = useAppDispatch()

    const handleDoubleClick = () => {
        try {
            if (currentWishlist) {
                const wishlist_id = currentWishlist.wishlist_id || ''
                const link_permission_id = currentWishlist.permissions && currentWishlist.permissions.link && currentWishlist.permissions.link.link_permissions
                    ? currentWishlist.permissions.link.link_permissions.link_permission_id || ''
                    : ''

                // Dispatch fetchWishlist action
                dispatch(fetchWishlist({ wishlist_id, link_permission_id }))

                // Redirect to wishlist page with wishlist ID
                let url = `/wishlist/${wishlist_id}`
                if (link_permission_id) {
                    url += `/${link_permission_id}`
                }
                window.location.href = url // Redirect using window.location.href
            } else {
                console.error('Current wishlist is undefined.')
                window.location.href = '/error/404'
            }
        } catch (error) {
            console.error('Failed to fetch wishlist:', error)
            // Handle errors here - for example, redirect to an error page or display an error message
            if (error.response && error.response.status === 403) {
                // Redirect to a page indicating "No permission"
                window.location.href = '/error/403'
            } else if (error.response && error.response.status === 404) {
                // Redirect to a page indicating "Not found"
                window.location.href = '/error/404'
            } else {
                // Handle other types of errors
                console.error('An unexpected error occurred:', error)
            }
        }
    }

    return (
        <Box onDoubleClick={handleDoubleClick} sx={{ padding: '10px' }}>
            <Box sx={{ display: 'block' }}>
                <Typography variant='h5' sx={{ fontWeight: 'bold' }}>
                    {currentWishlist ? currentWishlist.name : 'None'}
                </Typography>
            </Box>
            <Box sx={{ display: 'block' }}>
                <Typography variant='subtitle1'>
                    {currentWishlist ? currentWishlist.description : 'None'}
                </Typography>
            </Box>
        </Box>
    )
}

export default FetchWishlist
