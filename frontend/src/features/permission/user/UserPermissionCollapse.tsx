import { Collapse, Grid, Button } from '@mui/material'

import {
    canView,
    canEditWishlist,
    canEditItems,
    canEditTags,
    canSetTags,
    canComment,
} from '../permissionsValidation'

export const UserPermissionCollapse = (props: {
    opened: string
    user: {
        wishlist_id: string
        user_account: {
            user_account_id: string
            email: string
            username: string
        }
        permissions: number
    }
}) => {
    const { opened, user } = props

    return (
        <Collapse
            in={opened === user.user_account.user_account_id}
            timeout='auto'
            unmountOnExit
        >
            <Grid
                container
                sx={{
                    padding: 2,
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
            >
                <Grid item xs={12}>
                    **PLACEHOLDER** Can View Wishlist {canView(user.permissions) ? 'Yes' : 'No'}
                </Grid>
                <Grid item xs={12}>
                    **PLACEHOLDER** Can Edit Wishlist {canEditWishlist(user.permissions) ? 'Yes' : 'No'}
                </Grid>
                <Grid item xs={12}>
                    **PLACEHOLDER** Can Edit Wishlist Items {canEditItems(user.permissions) ? 'Yes' : 'No'}
                </Grid>
                <Grid item xs={12}>
                    **PLACEHOLDER** Can Configure Tags {canEditTags(user.permissions) ? 'Yes' : 'No'}
                </Grid>
                <Grid item xs={12}>
                    **PLACEHOLDER** Can Edit Item Tags {canSetTags(user.permissions) ? 'Yes' : 'No'}
                </Grid>
                <Grid item xs={12}>
                    **PLACEHOLDER** Can Comment {canComment(user.permissions) ? 'Yes' : 'No'}
                </Grid>
                <Grid item xs={8} />
                {/* Placeholder buttons, later will map to the component that allows updating and deleting the current link permission. */}
                <Grid item xs={2}>
                    <Button variant='contained' size='small'>
                        Save
                    </Button>
                </Grid>
                <Grid item xs={2}>
                    <Button variant='contained' color='error' size='small'>
                        Cancel
                    </Button>
                </Grid>
            </Grid>
        </Collapse>
    )
}
