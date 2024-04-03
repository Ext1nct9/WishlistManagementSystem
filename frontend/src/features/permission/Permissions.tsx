import {
    Button,
    Dialog,
    DialogContent,
    DialogTitle,
    Grid,
    Typography,
} from '@mui/material'
import type { DialogProps, GridProps } from '@mui/material'
import type { PermissionState } from './permissionState'
import LinkPermissions from './link/LinkPermissions'
import UserPermissions from './user/UserPermissions'
import { useAppDispatch } from '../../app/hooks'
import {
    setLinkPermissionCreateNew,
    setPermissionOpened,
    setUserPermissionCreateNew,
} from '../wishlist/wishlistSlice'

declare type UserPermissionsProps = DialogProps &
    PermissionState & {
        wishlist_id: string
        userProps?: GridProps // TODO: placeholder, can be any MUI props depending on the component used.
        linkProps?: GridProps // TODO: placeholder, can be any MUI props depending on the component used.
    }

const Permissions = (props: UserPermissionsProps) => {
    const { wishlist_id, user, link, userProps, linkProps, ...rest } = props

    const dispatch = useAppDispatch()
    return (
        <Dialog
            {...rest}
            scroll='paper'
            sx={{ '& .MuiDialog-paper': { width: '600px' } }}
            onClose={() => {
                dispatch(setPermissionOpened(false))
            }}
        >
            <DialogTitle>Manage Wishlist Permissions</DialogTitle>
            <Grid container p={2}>
                <Grid item xs={9}>
                    <Typography variant='subtitle1'>
                        User Permissions
                    </Typography>
                </Grid>
                <Grid item xs={3}>
                    <Button
                        variant='contained'
                        size='small'
                        onClick={() => {
                            dispatch(
                                setUserPermissionCreateNew({})
                            )
                        }}
                    >
                        Create New
                    </Button>
                </Grid>
            </Grid>
            <DialogContent
                dividers={true}
                sx={{
                    height: '50vh' /* not actual height, used to control the relative dimension between the two content. */,
                }}
            >
                <UserPermissions
                    wishlist_id={wishlist_id}
                    user={user}
                    {...props.userProps}
                />
            </DialogContent>
            <Grid container p={2}>
                <Grid item xs={9}>
                    <Typography variant='subtitle1'>
                        Link Permissions
                    </Typography>
                </Grid>
                <Grid item xs={3}>
                    <Button
                        variant='contained'
                        size='small'
                        onClick={() => {
                            dispatch(
                                setLinkPermissionCreateNew({})
                            )
                        }}
                    >
                        Create New
                    </Button>
                </Grid>
            </Grid>
            <DialogContent
                dividers={true}
                sx={{
                    height: '50vh' /* not actual height, used to control the relative dimension between the two content. */,
                }}
            >
                <LinkPermissions
                    wishlist_id={wishlist_id}
                    link={link}
                    {...props.linkProps}
                />
            </DialogContent>
        </Dialog>
    )
}

export default Permissions
