import { Grid } from '@mui/material'
import UserPermissionRow from './UserPermissionRow'

import type { GridProps } from '@mui/material'
import type { UserPermissionState } from '../permissionState'

declare type LinkPermissionsProps = GridProps & {
    wishlist_id: string
    user: UserPermissionState
}

const UserPermissions = (props: LinkPermissionsProps) => {
    const { wishlist_id, user, ...rest } = props
    const { opened, user_permissions } = user

    return (
        <Grid container {...rest}>
            <Grid item xs={12}>
                {/* A list of all link permissions. Each link permission will be mapped to a LinkPermissionRow. */}
                {user_permissions.map(user => (
                    <UserPermissionRow
                        wishlist_id={wishlist_id}
                        opened={opened}
                        user={user}
                    />
                ))}
            </Grid>
        </Grid>
    )
}

export default UserPermissions
