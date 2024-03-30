// store all permissions for the wishlist.
// ATTENTION: permissions can be empty if they are not fetched
// and you usually don't need to fetch them if you're not directly editing permissions.
// You can only expect this field to be filled only if you have the "edit permissions" component open.
export type UserPermission = {
    wishlist_id: string
    user_account: {
        user_account_id: string
        email: string
        username: string
    }
    permissions: number
}

export type UserPermissionState = {
    opened: null | undefined | string // currently opened user permission row in table
    editing:
        | null
        | undefined
        | {
              view: boolean
              edit: boolean
              edit_items: boolean
              edit_tags: boolean
              edit_item_tags: boolean
              comment: boolean
          } // current unsaved editing of the currently opened user permission row
    user_permissions: UserPermission[]
}

export type LinkPermission = {
    link_permission_id: string
    permissions: number
}

export type LinkPermissionState = {
    opened: null | undefined | string // currently opened link permission row in table
    editing:
        | null
        | undefined
        | {
              view: boolean
              edit: boolean
              edit_items: boolean
              edit_tags: boolean
              edit_item_tags: boolean
              comment: boolean
          } // current unsaved editing of the currently opened link permission row
    link_permissions: LinkPermission[]
}

export type LinkPermissionRowState = {
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
    link: {
        link_permission_id: string
        permissions: number
    }
}

export type PermissionState = {
    open: boolean
    user: UserPermissionState
    link: LinkPermissionState
}
