import { Grid } from '@mui/material'
import LinkPermissionRow from './LinkPermissionRow'

import type { GridProps } from '@mui/material'
import type { LinkPermissionState } from '../permissionState'

declare type LinkPermissionsProps = GridProps & {
    wishlist_id: string
    link: LinkPermissionState
}

const LinkPermissions = (props: LinkPermissionsProps) => {
    const { wishlist_id, link, ...rest } = props
    const { opened, editing, link_permissions } = link

    return (
        <Grid container {...rest}>
            <Grid item xs={12}>
                {/* A list of all link permissions. Each link permission will be mapped to a LinkPermissionRow. */}
                {link_permissions.map(link => (
                    <LinkPermissionRow
                        key={link.link_permission_id}
                        wishlist_id={wishlist_id}
                        opened={opened}
                        editing={editing}
                        link={link}
                    />
                ))}
            </Grid>
        </Grid>
    )
}

export default LinkPermissions
