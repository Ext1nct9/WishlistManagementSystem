export const canView = (permissions: number): boolean =>
    Boolean(permissions & 0b00000001)

export const canEditWishlist = (permissions: number): boolean =>
    Boolean(permissions & 0b00000010)

export const canEditItems = (permissions: number): boolean =>
    Boolean(permissions & 0b00000100)

export const canEditTags = (permissions: number): boolean =>
    Boolean(permissions & 0b00001000)

export const canSetTags = (permissions: number): boolean =>
    Boolean(permissions & 0b00010000)

export const canComment = (permissions: number): boolean =>
    Boolean(permissions & 0b00100000)

export const buildPermissions = (editing: {
    view: boolean
    edit: boolean
    edit_items: boolean
    edit_tags: boolean
    edit_item_tags: boolean
    comment: boolean
}): number => {
    let permissions = 0b00000000
    if (editing.view) permissions |= 0b00000001
    if (editing.edit) permissions |= 0b00000010
    if (editing.edit_items) permissions |= 0b00000100
    if (editing.edit_tags) permissions |= 0b00001000
    if (editing.edit_item_tags) permissions |= 0b00010000
    if (editing.comment) permissions |= 0b00100000
    return permissions
}
