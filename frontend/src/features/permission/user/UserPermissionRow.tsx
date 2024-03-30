import {
    KeyboardArrowUp,
    KeyboardArrowDown,
    ContentCopy,
    Delete,
} from '@mui/icons-material'
import { Grid, IconButton, Typography } from '@mui/material'
import { UserPermissionCollapse } from './UserPermissionCollapse'

import {
    setUserPermissionOpened,
    revokeUserPermission,
} from '../../wishlist/wishlistSlice'
import { useAppDispatch } from '../../../app/hooks'

const UserPermissionRow = (props: {
    wishlist_id: string
    opened: string
    user: {
        user_account: {
            user_account_id: string
            email: string
            username: string
        }
        wishlist_id: string
        permissions: number
    }
}) => {
    const { wishlist_id, opened, user } = props

    // used to dispatch reducer actions, namely to update and delete the current user permission
    const dispatch = useAppDispatch()

    return (
        <Grid
            container
            key={user.user_account.user_account_id}
            sx={{
                alignItems: 'center',
                justifyContent: 'center',
            }}
        >
            {/* a key is assigned mainly because React requires a unique key for each mapped object, otherwise it will generate a warning. */}
            <Grid item xs={2}>
                <IconButton
                    onClick={() => {
                        dispatch(
                            setUserPermissionOpened(user.user_account.user_account_id)
                        )
                    }}
                >
                    {/* the button that opens/closes the dropdown menu (which is called a Collapse in MUI) */}
                    {opened === user.user_account.user_account_id ? (
                        <KeyboardArrowUp />
                    ) : (
                        <KeyboardArrowDown />
                    )}
                </IconButton>
            </Grid>
            <Grid item xs={8}>
                <Typography key={user.user_account.user_account_id}>
                    {user.user_account.email}
                </Typography>
            </Grid>
            <Grid item xs={1}>
                <IconButton
                    onClick={() =>
                        navigator.clipboard.writeText(
                            `${user.user_account.email}`
                        )
                    }
                >
                    {/* copies the **email** of the user */}
                    {/* TODO: copy email instead of account_id */}
                    <ContentCopy />
                </IconButton>
            </Grid>
            <Grid item xs={1}>
                <IconButton
                    onClick={() =>
                        dispatch(
                            revokeUserPermission({
                                user_accout_id: user.user_account.user_account_id,
                                wishlist_id: wishlist_id,
                            })
                        )
                    }
                >
                    {/* deletes the current user permission */}
                    <Delete />
                </IconButton>
            </Grid>
            {/* The dropdown menu. It is hidden if opened does not correspond to the current link. */}
            <UserPermissionCollapse opened={opened} user={user} />
        </Grid>
    )
}

export default UserPermissionRow
