import { Collapse, Grid, Button } from '@mui/material'

import {
    buildPermissions,
    canView,
    canEditWishlist,
    canEditItems,
    canEditTags,
    canSetTags,
    canComment,
} from '../permissionsValidation'
import { useAppDispatch } from '../../../app/hooks'
import {
    setUserPermissionComment,
    setUserPermissionEdit,
    setUserPermissionEditItems,
    setUserPermissionEditItemTags,
    setUserPermissionEditTags,
    setUserPermissionView,
    updateUserPermission,
} from '../../wishlist/wishlistSlice'

export const UserPermissionCollapse = (props: {
    opened: string
    editing: {
        view: boolean
        edit: boolean
        edit_items: boolean
        edit_tags: boolean
        edit_item_tags: boolean
        comment: boolean
    }
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
    const { opened, editing, user } = props

    const dispatch = useAppDispatch()

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
                    {/*The opened check below is seemingly unnecessary, but it is used
                    because opening/closing the collapse has a transition,
                    but the state is updated before the transition starts.
                    Without the check, the UI will flash a false state every time we close the collapse,
                    thus misleading the user.*/}
                    {(opened ? editing.view : canView(user.permissions)) ? (
                        <Button
                            variant='text'
                            color='primary'
                            onClick={() => {
                                dispatch(setUserPermissionView(false))
                            }}
                        >
                            Can View
                        </Button>
                    ) : (
                        <Button
                            variant='text'
                            color='error'
                            onClick={() => {
                                dispatch(setUserPermissionView(true))
                            }}
                        >
                            Cannot View
                        </Button>
                    )}
                </Grid>
                <Grid item xs={12}>
                    {(
                        opened
                            ? editing.edit
                            : canEditWishlist(user.permissions)
                    ) ? (
                        <Button
                            variant='text'
                            color='primary'
                            onClick={() => {
                                dispatch(setUserPermissionEdit(false))
                            }}
                        >
                            Can Edit
                        </Button>
                    ) : (
                        <Button
                            variant='text'
                            color='error'
                            onClick={() => {
                                dispatch(setUserPermissionEdit(true))
                            }}
                        >
                            Cannot Edit
                        </Button>
                    )}
                </Grid>
                <Grid item xs={12}>
                    {(
                        opened
                            ? editing.edit_items
                            : canEditItems(user.permissions)
                    ) ? (
                        <Button
                            variant='text'
                            color='primary'
                            onClick={() => {
                                dispatch(setUserPermissionEditItems(false))
                            }}
                        >
                            Can Edit Items
                        </Button>
                    ) : (
                        <Button
                            variant='text'
                            color='error'
                            onClick={() => {
                                dispatch(setUserPermissionEditItems(true))
                            }}
                        >
                            Cannot Edit Items
                        </Button>
                    )}
                </Grid>
                <Grid item xs={12}>
                    {(
                        opened
                            ? editing.edit_tags
                            : canEditTags(user.permissions)
                    ) ? (
                        <Button
                            variant='text'
                            color='primary'
                            onClick={() => {
                                dispatch(setUserPermissionEditTags(false))
                            }}
                        >
                            Can Edit Tags
                        </Button>
                    ) : (
                        <Button
                            variant='text'
                            color='error'
                            onClick={() => {
                                dispatch(setUserPermissionEditTags(true))
                            }}
                        >
                            Cannot Edit Tags
                        </Button>
                    )}
                </Grid>
                <Grid item xs={12}>
                    {(
                        opened
                            ? editing.edit_item_tags
                            : canSetTags(user.permissions)
                    ) ? (
                        <Button
                            variant='text'
                            color='primary'
                            onClick={() => {
                                dispatch(setUserPermissionEditItemTags(false))
                            }}
                        >
                            Can Edit Item Tags
                        </Button>
                    ) : (
                        <Button
                            variant='text'
                            color='error'
                            onClick={() => {
                                dispatch(setUserPermissionEditItemTags(true))
                            }}
                        >
                            Cannot Edit Item Tags
                        </Button>
                    )}
                </Grid>
                <Grid item xs={12}>
                    {(
                        opened ? editing.comment : canComment(user.permissions)
                    ) ? (
                        <Button
                            variant='text'
                            color='primary'
                            onClick={() => {
                                dispatch(setUserPermissionComment(false))
                            }}
                        >
                            Can Comment
                        </Button>
                    ) : (
                        <Button
                            variant='text'
                            color='error'
                            onClick={() => {
                                dispatch(setUserPermissionComment(true))
                            }}
                        >
                            Cannot Comment
                        </Button>
                    )}
                </Grid>
                <Grid item xs={8} />
                <Grid item xs={2}>
                    <Button
                        variant='contained'
                        size='small'
                        onClick={() => {
                            dispatch(
                                updateUserPermission({
                                    user_account_id: user.user_account.user_account_id,
                                    wishlist_id: user.wishlist_id,
                                    permissions: buildPermissions(editing),
                                })
                            )
                        }}
                    >
                        Save
                    </Button>
                </Grid>
                <Grid item xs={2}>
                    <Button
                        variant='contained'
                        color='error'
                        size='small'
                        onClick={() => {
                            dispatch(
                                setUserPermissionView(canView(user.permissions))
                            )
                            dispatch(
                                setUserPermissionEdit(
                                    canEditWishlist(user.permissions)
                                )
                            )
                            dispatch(
                                setUserPermissionEditItems(
                                    canEditItems(user.permissions)
                                )
                            )
                            dispatch(
                                setUserPermissionEditTags(
                                    canEditTags(user.permissions)
                                )
                            )
                            dispatch(
                                setUserPermissionEditItemTags(
                                    canSetTags(user.permissions)
                                )
                            )
                            dispatch(
                                setUserPermissionComment(
                                    canComment(user.permissions)
                                )
                            )
                        }}
                    >
                        Cancel
                    </Button>
                </Grid>
            </Grid>
        </Collapse>
    )
}
