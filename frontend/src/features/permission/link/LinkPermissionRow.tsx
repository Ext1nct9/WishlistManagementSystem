import {
    KeyboardArrowUp,
    KeyboardArrowDown,
    ContentCopy,
    Delete,
} from '@mui/icons-material'
import { Grid, IconButton, Typography } from '@mui/material'
import { LinkPermissionCollapse } from './LinkPermissionCollapse'

import {
    setLinkPermissionOpened,
    revokeLinkPermission,
} from '../../wishlist/wishlistSlice'
import { useAppDispatch } from '../../../app/hooks'

import { client_base_url } from '../../../appsettings.json'
import type { LinkPermissionRowState } from '../permissionState'

const LinkPermissionRow = (props: LinkPermissionRowState) => {
    const { wishlist_id, opened, editing, link } = props

    // used to dispatch reducer actions, namely to update and delete the current link permission
    const dispatch = useAppDispatch()

    return (
        <Grid
            container
            key={link.link_permission_id}
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
                            setLinkPermissionOpened(link.link_permission_id)
                        )
                    }}
                >
                    {/* the button that opens/closes the dropdown menu (which is called a Collapse in MUI) */}
                    {opened === link.link_permission_id ? (
                        <KeyboardArrowUp />
                    ) : (
                        <KeyboardArrowDown />
                    )}
                </IconButton>
            </Grid>
            <Grid item xs={8}>
                <Typography key={link.link_permission_id}>
                    {link.link_permission_id}
                </Typography>
            </Grid>
            <Grid item xs={1}>
                <IconButton
                    onClick={() =>
                        navigator.clipboard.writeText(
                            `${client_base_url}/wishlist/${wishlist_id}?link_permission_id=${link.link_permission_id}`
                        )
                    }
                >
                    {/* copies the **wishlist** link the user should use to access the wishlist with a permission link. */}
                    <ContentCopy />
                </IconButton>
            </Grid>
            <Grid item xs={1}>
                <IconButton
                    onClick={() =>
                        dispatch(
                            revokeLinkPermission({
                                wishlist_id: wishlist_id,
                                link_permission_id: link.link_permission_id,
                            })
                        )
                    }
                >
                    {/* deletes the current link permission */}
                    <Delete />
                </IconButton>
            </Grid>
            {/* The dropdown menu. It is hidden if opened does not correspond to the current link. */}
            <LinkPermissionCollapse
                opened={opened}
                editing={editing}
                wishlist_id={wishlist_id}
                link={link}
            />
        </Grid>
    )
}

export default LinkPermissionRow
