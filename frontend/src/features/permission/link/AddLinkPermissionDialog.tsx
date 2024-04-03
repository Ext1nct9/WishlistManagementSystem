import { Button, Dialog, Grid, IconButton, Typography } from '@mui/material'
import { newLinkPermissionId } from '../permissionState'
import { useAppDispatch } from '../../../app/hooks'
import {
    createLinkPermission,
    revokeLinkPermission,
    setLinkPermissionComment,
    setLinkPermissionEdit,
    setLinkPermissionEditItems,
    setLinkPermissionEditItemTags,
    setLinkPermissionEditTags,
    setLinkPermissionOpened,
    setLinkPermissionView,
} from '../../wishlist/wishlistSlice'
import { buildPermissions } from '../permissionsValidation'
import { ContentCopy, Delete } from '@mui/icons-material'

import { client_base_url } from '../../../appsettings.json'

type AddLinkPermissionDialogProps = {
    wishlist_id: string
    opened: string
    editing: {
        link_permission_id: string
        view: boolean
        edit: boolean
        edit_items: boolean
        edit_tags: boolean
        edit_item_tags: boolean
        comment: boolean
    }
}

const AddLinkPermissionDialog = (props: AddLinkPermissionDialogProps) => {
    const { wishlist_id, opened, editing } = props

    const dispatch = useAppDispatch()
    return (
        <Dialog
            open={opened === newLinkPermissionId}
            onClose={() => {
                dispatch(setLinkPermissionOpened(null))
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
                {editing.link_permission_id && (
                    <>
                        <Grid item xs={2} />
                        <Grid item xs={8}>
                            <Typography>
                                {editing.link_permission_id}
                            </Typography>
                        </Grid>
                        <Grid item xs={1}>
                            <IconButton
                                onClick={() =>
                                    navigator.clipboard.writeText(
                                        `${client_base_url}/wishlist/${wishlist_id}?link_permission_id=${editing.link_permission_id}`
                                    )
                                }
                            >
                                {/* copies the **wishlist** link the user should use to access the wishlist with a permission link. */}
                                <ContentCopy />
                            </IconButton>
                        </Grid>
                        <Grid item xs={1}>
                            <IconButton
                                onClick={() => {
                                    dispatch(
                                        revokeLinkPermission({
                                            wishlist_id: wishlist_id,
                                            link_permission_id:
                                                editing.link_permission_id,
                                        })
                                    )
                                    dispatch(setLinkPermissionOpened(null))
                                }}
                            >
                                {/* deletes the current link permission */}
                                <Delete />
                            </IconButton>
                        </Grid>
                    </>
                )}
                <Grid item xs={12}>
                    {editing.view ? (
                        <Button
                            variant='text'
                            color='primary'
                            onClick={() => {
                                dispatch(setLinkPermissionView(false))
                            }}
                        >
                            Can View
                        </Button>
                    ) : (
                        <Button
                            variant='text'
                            color='error'
                            onClick={() => {
                                dispatch(setLinkPermissionView(true))
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
                                dispatch(setLinkPermissionEdit(false))
                            }}
                        >
                            Can Edit
                        </Button>
                    ) : (
                        <Button
                            variant='text'
                            color='error'
                            onClick={() => {
                                dispatch(setLinkPermissionEdit(true))
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
                                dispatch(setLinkPermissionEditItems(false))
                            }}
                        >
                            Can Edit Items
                        </Button>
                    ) : (
                        <Button
                            variant='text'
                            color='error'
                            onClick={() => {
                                dispatch(setLinkPermissionEditItems(true))
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
                                dispatch(setLinkPermissionEditTags(false))
                            }}
                        >
                            Can Edit Tags
                        </Button>
                    ) : (
                        <Button
                            variant='text'
                            color='error'
                            onClick={() => {
                                dispatch(setLinkPermissionEditTags(true))
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
                                dispatch(setLinkPermissionEditItemTags(false))
                            }}
                        >
                            Can Edit Item Tags
                        </Button>
                    ) : (
                        <Button
                            variant='text'
                            color='error'
                            onClick={() => {
                                dispatch(setLinkPermissionEditItemTags(true))
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
                                dispatch(setLinkPermissionComment(false))
                            }}
                        >
                            Can Comment
                        </Button>
                    ) : (
                        <Button
                            variant='text'
                            color='error'
                            onClick={() => {
                                dispatch(setLinkPermissionComment(true))
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
                                createLinkPermission({
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
                            dispatch(setLinkPermissionOpened(null))
                        }}
                    >
                        Close
                    </Button>
                </Grid>
            </Grid>
        </Dialog>
    )
}

export default AddLinkPermissionDialog
