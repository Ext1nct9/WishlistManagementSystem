import { Button, Dialog, Grid, IconButton, Input, TextField, Typography } from '@mui/material'
import { newUserPermissionId } from '../permissionState'
import { useAppDispatch } from '../../../app/hooks'
import {
    createLinkPermission,
    createUserPermission,
    revokeLinkPermission,
    setUserPermissionComment,
    setUserPermissionEdit,
    setUserPermissionEditItems,
    setUserPermissionEditItemTags,
    setUserPermissionEditTags,
    setUserPermissionOpened,
    setUserPermissionView,
} from '../../wishlist/wishlistSlice'
import { buildPermissions } from '../permissionsValidation'
import { ContentCopy, Delete } from '@mui/icons-material'

import { client_base_url } from '../../../appsettings.json'

type AddUserPermissionDialogProps = {
    wishlist_id: string
    opened: string
    editing: {
        view: boolean
        edit: boolean
        edit_items: boolean
        edit_tags: boolean
        edit_item_tags: boolean
        comment: boolean
    }
}

const AddUserPermissionDialog = (props: AddUserPermissionDialogProps) => {
    const { wishlist_id, opened, editing } = props

    const dispatch = useAppDispatch()
    return (
        <Dialog
            open={opened === newUserPermissionId}
            onClose={() => {
                dispatch(setUserPermissionOpened(null))
            }}
        >
            <Grid
                container
                sx={{
                    padding: 2,
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
            >
                {/* TODO: Consider adding if also added for link permissions
                <Grid item xs={12}>
                    <Typography variant='h6'>Add User Permission</Typography>
                </Grid>
                */}
                <Grid item xs={12}>
                    <TextField
                        id = 'user_account_email'
                        label = 'User Account Email'
                        fullWidth
                    />
                </Grid>
                <Grid item xs={12}>
                    {editing.view ? (
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
                    {editing.edit ? (
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
                    {editing.edit_items ? (
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
                    {editing.edit_tags ? (
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
                    {editing.edit_item_tags ? (
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
                    {editing.comment ? (
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
                            const userAccountEmail = document.getElementById('user_account_email') as HTMLInputElement
                            dispatch(
                                createUserPermission({
                                    user_account_email: userAccountEmail.value,
                                    wishlist_id: wishlist_id,
                                    permissions: buildPermissions(editing),
                                })
                            )
                        }}
                    >
                        Create
                    </Button>
                </Grid>
                <Grid item xs={2}>
                    <Button
                        variant='contained'
                        color='error'
                        size='small'
                        onClick={() => {
                            dispatch(setUserPermissionOpened(null))
                        }}
                    >
                        Close
                    </Button>
                </Grid>
            </Grid>
        </Dialog>
    )
}

export default AddUserPermissionDialog
