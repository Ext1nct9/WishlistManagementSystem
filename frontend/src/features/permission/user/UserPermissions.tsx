import { Grid } from '@mui/material'
import UserPermissionRow from './UserPermissionRow'

import type { GridProps } from '@mui/material'
import type { UserPermissionState } from '../permissionState'
import AddUserPermissionDialog from './AddUserPermissionDialog'

declare type LinkPermissionsProps = GridProps & {
    wishlist_id: string
    user: UserPermissionState
}

const UserPermissions = (props: LinkPermissionsProps) => {
    const { wishlist_id, user, ...rest } = props
    const { opened, editing, user_permissions } = user

    return (
        <Grid container {...rest}>
            <Grid item xs={12}>
                {/* A list of all link permissions. Each link permission will be mapped to a LinkPermissionRow. */}
                {user_permissions.map(user => (
                    <UserPermissionRow
                        wishlist_id={wishlist_id}
                        opened={opened}
                        editing={editing}
                        user={user}
                    />
                ))}
            </Grid>
            <AddUserPermissionDialog
                wishlist_id={wishlist_id}
                opened={opened}
                editing={editing}
            />
        </Grid>
    )
}

export default UserPermissions
