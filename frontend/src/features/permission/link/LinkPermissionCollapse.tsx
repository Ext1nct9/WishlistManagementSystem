import { Collapse, Grid, Button } from '@mui/material'
import {
    buildPermissions,
    canComment,
    canEditItems,
    canEditTags,
    canEditWishlist,
    canSetTags,
    canView,
} from '../permissionsValidation'
import { useAppDispatch } from '../../../app/hooks'
import {
    setLinkPermissionComment,
    setLinkPermissionEdit,
    setLinkPermissionEditItems,
    setLinkPermissionEditItemTags,
    setLinkPermissionEditTags,
    setLinkPermissionView,
    updateLinkPermission,
} from '../../wishlist/wishlistSlice'
import type { LinkPermissionRowState } from '../permissionState'

export const LinkPermissionCollapse = (props: LinkPermissionRowState) => {
    const { wishlist_id, opened, editing, link } = props

    const dispatch = useAppDispatch()

    return (
        <Collapse
            in={opened === link.link_permission_id}
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
                    {(opened ? editing.view : canView(link.permissions)) ? (
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
                    {(
                        opened
                            ? editing.edit
                            : canEditWishlist(link.permissions)
                    ) ? (
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
                    {(
                        opened
                            ? editing.edit_items
                            : canEditItems(link.permissions)
                    ) ? (
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
                    {(
                        opened
                            ? editing.edit_tags
                            : canEditTags(link.permissions)
                    ) ? (
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
                    {(
                        opened
                            ? editing.edit_item_tags
                            : canSetTags(link.permissions)
                    ) ? (
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
                    {(
                        opened ? editing.comment : canComment(link.permissions)
                    ) ? (
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
                {/* Placeholder buttons, later will map to the component that allows updating and deleting the current link permission. */}
                <Grid item xs={2}>
                    <Button
                        variant='contained'
                        size='small'
                        onClick={() => {
                            dispatch(
                                updateLinkPermission({
                                    wishlist_id: wishlist_id,
                                    link_permission_id: link.link_permission_id,
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
                                setLinkPermissionView(canView(link.permissions))
                            )
                            dispatch(
                                setLinkPermissionEdit(
                                    canEditWishlist(link.permissions)
                                )
                            )
                            dispatch(
                                setLinkPermissionEditItems(
                                    canEditItems(link.permissions)
                                )
                            )
                            dispatch(
                                setLinkPermissionEditTags(
                                    canEditTags(link.permissions)
                                )
                            )
                            dispatch(
                                setLinkPermissionEditItemTags(
                                    canSetTags(link.permissions)
                                )
                            )
                            dispatch(
                                setLinkPermissionComment(
                                    canComment(link.permissions)
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
