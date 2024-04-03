import type { PayloadAction, Slice } from "@reduxjs/toolkit/react"
import { newLinkPermissionId, newUserPermissionId, type PermissionState } from "../permission/permissionState"
import type { tagState } from "../tag/tagState"
import type { CommentState } from "../comment/commentState"
import type { ItemState } from "../item/itemState"
import { createAppSlice } from "../../app/createAppSlice"
import { server_base_url as BASE_URL } from "../../appsettings.json"
import { canComment, canEditItems, canEditTags, canEditWishlist, canSetTags, canView } from "../permission/permissionsValidation"

export type WishlistResponse = {
  wishlist_id: string
  name: string
  description: string
  user_account_id: string
}

export type WishlistState = {
  wishlist_id: string
  name: string
  description: string
  user_account_id: string
  permissions: PermissionState // stores all permissions for the wishlist. ATTENTION: permissions can be empty if they are not fetched, which can be the case if you're not directly editing permissions
  tags: tagState[] // stores all tags for the wishlist
  // TODO: other states if necessary
  openDialog: boolean
  items: ItemState[]
}

export type CompactWishlistState = {
    wishlist_id: string
    name: string
    description: string
}

const initializeWishlistState = (
  wishlist_id: string,
  name: string,
  description: string,
  user_account_id: string,
): WishlistState => {
  return {
    wishlist_id: wishlist_id,
    name: name,
    description: description,
    user_account_id: user_account_id,
    tags: [],
    permissions: {
      open: false,
      user: {
        opened: null,
        editing: {
            view: false,
            edit: false,
            edit_items: false,
            edit_tags: false,
            edit_item_tags: false,
            comment: false,
        },
        user_permissions: [],
        waiting: false,
      },
      link: {
        opened: null,
        editing: {
            link_permission_id: null,
            view: false,
            edit: false,
            edit_items: false,
            edit_tags: false,
            edit_item_tags: false,
            comment: false,
        },
        link_permissions: [],
        waiting: false,
      },
    },
    // TODO: other states if necessary
    openDialog: false,
    items: [],
  }
}

export type WishlistSliceState = {
  current: null | undefined | WishlistState // The current wishlist opened in a wishlist view by the user
  // TODO: other states if necessary
  allWishlists: null | undefined | CompactWishlistState[] // All wishlists of the user
  loading: boolean
  errorCode : string | null
}

const initialState: WishlistSliceState = {
  current: undefined,
  allWishlists: [],
  loading : false,
  errorCode : null,
}

export const wishlistSlice: Slice = createAppSlice({
  name: "wishlist",
  initialState,
  reducers: create => ({
    setCurrentWishlist: create.reducer(
      (state, action: PayloadAction<WishlistResponse>) => {
        if (action.payload === null || action.payload === undefined) {
          state.current = null
          return
        }

        state.current = initializeWishlistState(
          action.payload.wishlist_id,
          action.payload.name,
          action.payload.description,
          action.payload.user_account_id,
        )
      },
    ),
    setMockCurrentWishlist: create.reducer( // **DO NOT USE THIS IN PRODUCTION**
      (state, action: PayloadAction<any>) => {
        state.current = action.payload
      }
    ),
    setPermissionOpened: create.reducer(
      (state, action: PayloadAction<boolean>) => {
        if (state.current) {
          state.current.permissions.open = action.payload
        }
      },
    ),
    setLinkPermissionOpened: create.reducer(
        (state, action: PayloadAction<string>) => {
            if (state.current) {
                if (
                    state.current.permissions.link.opened === action.payload
                    || action.payload === null
                ) {
                    state.current.permissions.link.opened = null
                    state.current.permissions.link.editing = {
                        link_permission_id: null,
                        view: false,
                        edit: false,
                        edit_items: false,
                        edit_tags: false,
                        edit_item_tags: false,
                        comment: false,
                    }
                } else {
                    const current_link = state.current.permissions.link.link_permissions.find(
                        link_permission =>
                            link_permission.link_permission_id === action.payload
                    )

                    if (current_link) {
                        state.current.permissions.link.opened = action.payload
                        state.current.permissions.link.editing = {
                            link_permission_id: action.payload,
                            view: canView(current_link.permissions),
                            edit: canEditWishlist(current_link.permissions),
                            edit_items: canEditItems(current_link.permissions),
                            edit_tags: canEditTags(current_link.permissions),
                            edit_item_tags: canSetTags(current_link.permissions),
                            comment: canComment(current_link.permissions),
                        }
                    }
                }
            }
        }
    ),
    setLinkPermissionCreateNew: create.reducer(
        (state) => {
            if (state.current) {
                state.current.permissions.link.opened = newLinkPermissionId
                state.current.permissions.link.editing = {
                    link_permission_id: null,
                    view: false,
                    edit: false,
                    edit_items: false,
                    edit_tags: false,
                    edit_item_tags: false,
                    comment: false,
                }
            }
        }
    ),
    setLinkPermissionView: create.reducer(
        (state, action: PayloadAction<boolean>) => {
            if (state.current) {
                if (state.current.permissions.link.opened) {
                    state.current.permissions.link.editing.view = action.payload
                }
            }
        }
    ),
    setLinkPermissionEdit: create.reducer(
        (state, action: PayloadAction<boolean>) => {
            if (state.current) {
                if (state.current.permissions.link.opened) {
                    state.current.permissions.link.editing.edit = action.payload
                }
            }
        }
    ),
    setLinkPermissionEditItems: create.reducer(
        (state, action: PayloadAction<boolean>) => {
            if (state.current) {
                if (state.current.permissions.link.opened) {
                    state.current.permissions.link.editing.edit_items = action.payload
                }
            }
        }
    ),
    setLinkPermissionEditTags: create.reducer(
        (state, action: PayloadAction<boolean>) => {
            if (state.current) {
                if (state.current.permissions.link.opened) {
                    state.current.permissions.link.editing.edit_tags = action.payload
                }
            }
        }
    ),
    setLinkPermissionEditItemTags: create.reducer(
        (state, action: PayloadAction<boolean>) => {
            if (state.current) {
                if (state.current.permissions.link.opened) {
                    state.current.permissions.link.editing.edit_item_tags = action.payload
                }
            }
        }
    ),
    setLinkPermissionComment: create.reducer(
        (state, action: PayloadAction<boolean>) => {
            if (state.current) {
                if (state.current.permissions.link.opened) {
                    state.current.permissions.link.editing.comment = action.payload
                }
            }
        }
    ),
    setDialogOpen: create.reducer(
        (state, action: PayloadAction<boolean>) => {
            if (state.current) {
                state.current.openDialog = action.payload
            }
        }
    ),
    updateName: create.reducer((state, action: PayloadAction<string>) => {
        if (state.current) {
            state.current.name = action.payload
        }
    }),
    updateDescription: create.reducer(
        (state, action: PayloadAction<string>) => {
            if (state.current) {
                state.current.description = action.payload
            }
        }
    ),
    fetchLinkPermissions: create.asyncThunk(
      async (wishlist_id: string): Promise<any> => {
        return fetch(`${BASE_URL}/wishlist/${wishlist_id}/permission_link`, {
          credentials: "include", // to enable cookies so that user account id can get through
        }).then(response => {
          if (response.ok) {
            return response.json()
          }

          console.error("Failed to fetch link permissions")
        })
      },
      {
        pending: state => {
          // do nothing
          // TODO: do something?
        },
        fulfilled: (state, action) => {
          const { wishlist_id, permission_links } = action.payload
          if (state.current && state.current.wishlist_id === wishlist_id) {
            // response is valid
            state.current.permissions.link.link_permissions = permission_links
            state.current.permissions.link.waiting = false
          } else {
            // the user closed or switched wishlist view
            // response expired, do nothing
            console.warn(
              `Incoming link permissions response for wishlist ${wishlist_id},
              but the wishlist view expired.`,
            )
            console.log("Response is ignored.")
          }
        },
        rejected: state => {
          console.error("Failed to fetch link permissions")
        },
      },
    ),
    createLinkPermission: create.asyncThunk(
        async (args: {
            wishlist_id: string
            permissions: number
        }): Promise<any> => {
            const { wishlist_id, permissions } = args
            return fetch(`${BASE_URL}/wishlist/${wishlist_id}/permission_link`, {
            method: "POST",
            credentials: 'include', // to enable cookies so that user account id can get through
            body: JSON.stringify({ permissions: permissions }),
            }).then(response => {
            if (response.ok) {
                return response.json()
            }

            console.error("Failed to create link permissions")
            })
        },
        {
            pending: state => {
            // do nothing
            // TODO: do something?
            },
            fulfilled: (state, action) => {
                const { link_permission_id, permissions, wishlist_id } =
                    action.payload
                if (state.current && state.current.wishlist_id === wishlist_id) {
                    // response is valid
                    state.current.permissions.link.link_permissions.push({
                        link_permission_id: link_permission_id,
                        permissions: permissions,
                    })

                    state.current.permissions.link.editing.link_permission_id = link_permission_id

                    console.log(state)
                } else {
                    // the user closed or switched wishlist view
                    // response expired, do nothing
                    console.warn(
                        `Incoming link permissions response for wishlist ${wishlist_id},
                        but the wishlist view expired.`,
                    )
                    console.log("Response is ignored.")
                }
            },
            rejected: state => {
                console.error("Failed to create link permissions")
            },
        }
    ),
    updateLinkPermission: create.asyncThunk(
        async (args: {
            wishlist_id: string
            link_permission_id: string
            permissions: number
        }): Promise<any> => {
            const { wishlist_id, link_permission_id, permissions } = args
            return fetch(
                `${BASE_URL}/wishlist/${wishlist_id}/permission_link/${link_permission_id}`,
                {
                    method: 'PUT',
                    credentials: 'include', // to enable cookies so that user account id can get through
                    body: JSON.stringify({ permissions: permissions }),
                }
            ).then(response => {
                if (response.ok) {
                    return response.json()
                }

                console.error('Failed to update link permissions')
            })
        },
        {
            pending: state => {
                // do nothing
                // TODO: do something?
            },
            fulfilled: (state, action) => {
                const { link_permission_id, permissions, wishlist_id } =
                    action.payload
                if (
                    state.current &&
                    state.current.wishlist_id === wishlist_id
                ) {
                    // response is valid
                    const link_permission =
                        state.current.permissions.link.link_permissions.find(
                            link_permission =>
                                link_permission.link_permission_id ===
                                link_permission_id
                        )
                    if (link_permission) {
                        link_permission.permissions = permissions
                        alert('LinkPermissions updated successfully')
                    } else {
                        // technically shouldn't happen, but as a failsafe
                        console.warn(
                            `Incoming link permissions response for wishlist ${wishlist_id},
            but the link permission ${link_permission_id} is not found.`
                        )
                        console.log('Response is ignored.')
                    }
                } else {
                    // the user closed or switched wishlist view
                    // response expired, do nothing
                    console.warn(
                        `Incoming link permissions response for wishlist ${wishlist_id},
            but the wishlist view expired.`
                    )
                    console.log('Response is ignored.')
                }
            },
            rejected: state => {
                console.error('Failed to update link permissions')
            },
        }
    ),
    revokeLinkPermission: create.asyncThunk(
        async (args: {
            wishlist_id: string
            link_permission_id: string
        }): Promise<any> => {
            const { wishlist_id, link_permission_id } = args
            return fetch(
                `${BASE_URL}/wishlist/${wishlist_id}/permission_link/${link_permission_id}`,
                {
                    method: 'DELETE',
                    credentials: 'include', // to enable cookies so that user account id can get through
                }
            ).then(response => {
                if (response.ok) {
                    return { wishlist_id, link_permission_id }
                }

                console.error('Failed to revoke link permissions')
            })
        },
        {
            pending: state => {
                // do nothing
                // TODO: do something?
            },
            fulfilled: (state, action) => {
                const { link_permission_id, wishlist_id } = action.payload
                if (
                    state.current &&
                    state.current.wishlist_id === wishlist_id
                ) {
                    // response is valid
                    state.current.permissions.link.link_permissions =
                        state.current.permissions.link.link_permissions.filter(
                            link_permission =>
                                link_permission.link_permission_id !==
                                link_permission_id
                        )
                } else {
                    // the user closed or switched wishlist view
                    // response expired, do nothing
                    console.warn(
                        `Incoming link permissions response for wishlist ${wishlist_id},
            but the wishlist view expired.`
                    )
                    console.log('Response is ignored.')
                }
            },
            rejected: state => {
                console.error('Failed to revoke link permissions')
            },
        }
    ),
    setUserPermissionOpened: create.reducer(
        (state, action: PayloadAction<string>) => {
            if (state.current) {
                if (
                    state.current.permissions.user.opened === action.payload
                    || action.payload === null
                ) {
                    state.current.permissions.user.opened = null
                    state.current.permissions.user.editing = {
                        view: false,
                        edit: false,
                        edit_items: false,
                        edit_tags: false,
                        edit_item_tags: false,
                        comment: false,
                    }
                } else {
                    const current_user = state.current.permissions.user.user_permissions.find(
                        user_permission =>
                            user_permission.user_account.user_account_id === action.payload
                    )

                    if (current_user) {
                        state.current.permissions.user.opened = action.payload
                        state.current.permissions.user.editing = {
                            view: canView(current_user.permissions),
                            edit: canEditWishlist(current_user.permissions),
                            edit_items: canEditItems(current_user.permissions),
                            edit_tags: canEditTags(current_user.permissions),
                            edit_item_tags: canSetTags(current_user.permissions),
                            comment: canComment(current_user.permissions),
                        }
                    }
                }
            }
        }
    ),
    setUserPermissionEditing: create.reducer(
        (state, action: PayloadAction<number>) => {
            if (state.current) {
                state.current.permissions.user.editing = {
                    view: canView(action.payload),
                    edit: canEditWishlist(action.payload),
                    edit_items: canEditItems(action.payload),
                    edit_tags: canEditTags(action.payload),
                    edit_item_tags: canSetTags(action.payload),
                    comment: canComment(action.payload),
                }
            }
        }
    ),
    setUserPermissionCreateNew: create.reducer(
        (state) => {
            if (state.current) {
                state.current.permissions.user.opened = newUserPermissionId
                state.current.permissions.user.editing = {
                    view: false,
                    edit: false,
                    edit_items: false,
                    edit_tags: false,
                    edit_item_tags: false,
                    comment: false,
                }
            }
        }
    ),
    setUserPermissionView: create.reducer(
        (state, action: PayloadAction<boolean>) => {
            if (state.current) {
                if (state.current.permissions.user.opened) {
                    state.current.permissions.user.editing.view = action.payload
                }
            }
        }
    ),
    setUserPermissionEdit: create.reducer(
        (state, action: PayloadAction<boolean>) => {
            if (state.current) {
                if (state.current.permissions.user.opened) {
                    state.current.permissions.user.editing.edit = action.payload
                }
            }
        }
    ),
    setUserPermissionEditItems: create.reducer(
        (state, action: PayloadAction<boolean>) => {
            if (state.current) {
                if (state.current.permissions.user.opened) {
                    state.current.permissions.user.editing.edit_items = action.payload
                }
            }
        }
    ),
    setUserPermissionEditTags: create.reducer(
        (state, action: PayloadAction<boolean>) => {
            if (state.current) {
                if (state.current.permissions.user.opened) {
                    state.current.permissions.user.editing.edit_tags = action.payload
                }
            }
        }
    ),
    setUserPermissionEditItemTags: create.reducer(
        (state, action: PayloadAction<boolean>) => {
            if (state.current) {
                if (state.current.permissions.user.opened) {
                    state.current.permissions.user.editing.edit_item_tags = action.payload
                }
            }
        }
    ),
    setUserPermissionComment: create.reducer(
        (state, action: PayloadAction<boolean>) => {
            if (state.current) {
                if (state.current.permissions.user.opened) {
                    state.current.permissions.user.editing.comment = action.payload
                }
            }
        }
    ),
    fetchUserPermissions: create.asyncThunk(
        async (wishlist_id: string): Promise<any> => {
            return fetch(`${BASE_URL}/get_user_permissions/${wishlist_id}`, {
                credentials: 'include', // to enable cookies so that user account id can get through
            }).then(response => {
                if (response.ok) {
                    return response.json()
                }
                console.error('Failed to fetch user permissions')
            })
        },
        {
            pending: state => {},
            fulfilled: (state, action) => {
                const { wishlist_id, user_permissions } = action.payload
                if (state.current && state.current.wishlist_id === wishlist_id) {
                    // response is valid
                    state.current.permissions.user.user_permissions = user_permissions
                    state.current.permissions.user.waiting = false
                } else {
                    // the user closed or switched wishlist view
                    // response expired, do nothing
                    console.warn(
                        `Incoming user permissions response for wishlist ${wishlist_id},
                        but the wishlist view expired.`
                    );
                    console.log('Response is ignored.')
                }
            },
            rejected: state => {
                console.error('Failed to fetch user permissions')
            },
        }
    ),
    createUserPermission: create.asyncThunk(
        async (args: {
            user_account_email: string,
            wishlist_id: string,
            permissions: number,
        }): Promise<any> => {
            const { user_account_email, wishlist_id, permissions } = args
            console.log(user_account_email)
            return fetch(
                `${BASE_URL}/create_user_permission/${wishlist_id}`,
                {
                    method: 'POST',
                    credentials: 'include', // to enable cookies so that user account id can get through
                    body: JSON.stringify({ user_account_email: user_account_email, permissions: permissions }),
                }
            ).then(response => {
                if (response.ok) {
                    return response.json()
                }
                console.error('Failed to fetch user permissions')
            })
        },
        {
            pending: state => {},
            fulfilled: (state, action) => {
                const { user_account, wishlist_id, permissions } = action.payload
                if (state.current && state.current.wishlist_id === wishlist_id) {
                    // response is valid
                    state.current.permissions.user.user_permissions.push({
                        user_account: user_account,
                        wishlist_id: wishlist_id,
                        permissions: permissions,
                    })
                    // close the dialog
                    state.current.permissions.user.opened = null
                } else {
                    // the user closed or switched wishlist view
                    // response expired, do nothing
                    console.warn(
                        `Incoming user permissions response for wishlist ${wishlist_id},
                        but the wishlist view expired.`
                    );
                    console.log('Response is ignored.')
                }
            },
            rejected: state => {
                console.error('Failed to fetch user permissions')
            },
        }
    ),
    updateUserPermission: create.asyncThunk(
        async (args: {
            user_account_id: string
            wishlist_id: string
            permissions: number
        }): Promise<any> => {
            const { user_account_id, wishlist_id, permissions } = args
            return fetch(
                `${BASE_URL}/user_permission/${user_account_id}/${wishlist_id}`,
                {
                    method: 'PUT',
                    credentials: 'include', // to enable cookies so that user account id can get through
                    body: JSON.stringify({ permissions: permissions }),
                }
            ).then(response => {
                if (response.ok) {
                    return response.json()
                }
                console.error('Failed to update link permissions')
            })
        },
        {
            pending: state => {},
            fulfilled: (state, action) => {
                const { user_account_id, wishlist_id, permissions } = action.payload
                if (
                    state.current &&
                    state.current.wishlist_id === wishlist_id
                ) {
                    // response is valid
                    const user_permission = state.current.permissions.user.user_permissions.find(
                        user_permission =>
                            user_permission.user_account.user_account_id === user_account_id
                    )
                    if (user_permission) {
                        user_permission.permissions = permissions
                        alert('UserPermissions updated successfully')
                    } else {
                        // technically shouldn't happen, but as a failsafe
                        console.warn(
                            `Incoming user permissions response for wishlist ${wishlist_id},
                            but the user permission ${user_account_id} is not found.`
                        );
                        console.log('Response is ignored.')
                    }
                } else {
                    // the user closed or switched wishlist view
                    // response expired, do nothing
                    console.warn(
                        `Incoming user permissions response for wishlist ${wishlist_id},
                        but the wishlist view expired.`
                    );
                    console.log('Response is ignored.')
                }
            },
            rejected: state => {
                console.error('Failed to update link permissions')
            },
        },
    ),
    revokeUserPermission: create.asyncThunk(
        async (args: {
            user_account_id: string
            wishlist_id: string
        }): Promise<any> => {
            const { user_account_id, wishlist_id } = args
            return fetch(
                `${BASE_URL}/user_permission/${user_account_id}/${wishlist_id}`,
                {
                    method: 'DELETE',
                    credentials: 'include', // to enable cookies so that user account id can get through
                }
            ).then(response => {
                if (response.ok) {
                    return { user_account_id, wishlist_id }
                }
                console.error('Failed to revoke user permissions - response not ok')
            })
        },
        {
            pending: state => {},
            fulfilled: (state, action) => {
                const { user_account_id, wishlist_id } = action.payload
                if (
                    state.current &&
                    state.current.wishlist_id === wishlist_id
                ) {
                    // response is valid
                    state.current.permissions.user.user_permissions = state.current.permissions.user.user_permissions.filter(
                        user_permission =>
                            user_permission.user_account.user_account_id !== user_account_id
                    )
                    
                } else {
                    // the user closed or switched wishlist view
                    // response expired, do nothing
                    console.warn(
                        `Incoming user permissions response for wishlist ${wishlist_id},
                        but the wishlist view expired.`
                    );
                    console.log('Response is ignored.')
                }
            },
            rejected: state => {
                console.error('Failed to revoke user permissions')
            },
        },
    ),
    fetchWishlist: create.asyncThunk(
        async (args: {
            wishlist_id: string
            link_permission_id?: string //optional
        }): Promise<any> => {
            const { wishlist_id, link_permission_id } = args
            return fetch(
                `${BASE_URL}/wishlist/view/${wishlist_id}?link_permission_id=${link_permission_id}`, {
                credentials: "include",

            }).then(response => {
                if (response.ok) {
                    return response.json()
                }
                throw new Error (response.status.toString())
            })
        },
        {
            pending: state => {
                state.loading = true
                state.errorCode = null
            },
            fulfilled: (state, action) => {
                // state.current = action.payload
                const {wishlist_id, name, description, user_account_id } = action.payload
                
                state.current = initializeWishlistState(wishlist_id, name, description, user_account_id);
                state.loading = false
                state.current.permissions.link.waiting = true
                state.current.permissions.user.waiting = true
            },
            rejected: (state, action) => {
                state.loading = false
                state.errorCode = action.error.message
                state.current = null
            },
        },
    ),
    updateWishlist: create.asyncThunk(
        async (args: {
            wishlist_id: string
            name: string
            description: string
            link_permission_id?: string //optional
        }): Promise<any> => {
            const { wishlist_id, name, description, link_permission_id } = args
            return fetch(
                `${BASE_URL}/wishlist/update/${wishlist_id}?link_permission_id=${link_permission_id}`, 
                {
                    method: 'PUT',
                    credentials: "include",
                    body: JSON.stringify({ name: name , description: description }),
                }
            ).then(response => {
                if (response.ok) {
                    return response.json()
                }
                throw new Error (response.status.toString())
            })
        },
        {
            pending: state => {
                state.errorCode = null

            },
            fulfilled: (state, action) => {
                const { wishlist_id, name, description } = action.payload
                
                if (
                    state.current &&
                    state.current.wishlist_id === wishlist_id
                ) {
                    // response is valid
                    state.current.name = name
                    state.current.description = description

                } else {
                    console.warn(
                      `Incoming wishlist data response for wishlist ${wishlist_id},
                      but the wishlist view expired.`,
                    )
                    console.log("Response is ignored.")
                }
            },
            rejected: (state , action) => {
                console.error("Failed to update the wishlist")
                state.errorCode = action.error.message
            },
        },
    ),
    deleteWishlist: create.asyncThunk(
        async (args: {
            wishlist_id: string
           }): Promise<any> => {
            const { wishlist_id } = args
            return fetch(
                `${BASE_URL}/wishlist/delete/${wishlist_id}`, 
                {
                    method: 'DELETE',
                    credentials: "include", 
                }
            ).then(response => {
                if (response.ok) {
                    return response.json()
                }

                throw new Error (response.status.toString())
            })
        },
        {
            pending: state => {
                state.errorCode = null
            },
            fulfilled: (state, action) => {
                const { wishlist_id } = action.payload
                
                if (
                    state.current &&
                    state.current.wishlist_id === wishlist_id
                ) {
                    // response is valid
                    state.current = undefined

                } else {
                    console.warn(
                      `Incoming wishlist data response for wishlist ${wishlist_id},
                      but the wishlist view expired.`,
                    )
                    console.log("Response is ignored.")
                }
            },
            rejected: (state, action) => {
                console.error("Failed to delete the wishlist")
                state.errorCode = action.error.message

            },
        },
    ),

    createTag  : create.asyncThunk(
        async (args: {
            wishlist_id: string
            label: string
            color: string
            link_permission_id?: string //optional
        }): Promise<any> => {
            const { wishlist_id, label, color, link_permission_id } = args
            return fetch(
                `${BASE_URL}/wishlist/${wishlist_id}/create_tag/link_permission_id=${link_permission_id}`, 
                {
                    method: 'PUT',
                    credentials: "include", 
                    body: JSON.stringify({ label: label, color: color }),
                }
            ).then(response => {
                if (response.ok) {
                    return response.json()
                }
              
                console.error("Failed to create the tag")

            })
        },
        {
            pending: state => {

            },

            fulfilled: (state, action) => {
                const { wishlist_id, tag_id, label, color} = action.payload
                if (state.current && state.current.wishlist_id === wishlist_id) {
                    // response is valid
                    state.current.tags.push({ 
                        wishlist_id: wishlist_id,
                        tag_id: tag_id,
                        label: label,
                        color: color,
                    })
                } else {
                    console.warn(
                      `Incoming tag data response for wishlist ${wishlist_id},
                      but the wishlist view expired.`,
                    )
                    console.log("Response is ignored.")
                }
            },
            rejected: state => {
                console.error("Failed to create the tag")
            },
        },
    ),
    updateTag: create.asyncThunk(
        async (args: {
            wishlist_id: string
            tag_id: string
            label: string
            color: string
            link_permission_id?: string //optional
        }): Promise<any> => {
            const { wishlist_id, tag_id, label, color, link_permission_id } = args
            return fetch(
                `${BASE_URL}/wishlist/${wishlist_id}/tag/${tag_id}?link_permission_id=${link_permission_id}`, 
                {
                    method: 'POST',
                    credentials: "include", 
                    body: JSON.stringify({ label: label, color: color }),
                }
            ).then(response => {
                if (response.ok) {
                    return response.json()
                }
              
                console.error("Failed to update the tag")

            })
        },
        {
            pending: state => {

            },

            fulfilled: (state, action) => {
                const { wishlist_id, tag_id, label , color} = action.payload
                if (
                    state.current && 
                    state.current.wishlist_id === wishlist_id
                ) {
                    const tag = state.current.tags.find(
                        tag => 
                            tag.tag_id === tag_id
                    )
                    if(tag) {
                        tag.label = label
                        tag.color = color
                    } else {
                        console.warn(
                          `Incoming tag data response for wishlist ${wishlist_id},
                          but the tag ${tag_id} is not found.`,
                        )
                        console.log("Response is ignored.")
                    }

                } else {
                    console.warn(
                      `Incoming tag data response for wishlist ${wishlist_id},
                      but the wishlist view expired.`,
                    )
                    console.log("Response is ignored.")
                }
            },
            rejected: state => {
                console.error("Failed to update the tag")
            },
        },
    ),
    deleteTag: create.asyncThunk(
        async (args: {
            wishlist_id: string
            tag_id: string
        }): Promise<any> => {
            const { wishlist_id, tag_id} = args
            return fetch(
                `${BASE_URL}/wishlist/${wishlist_id}/tag/${tag_id}`, 
                {
                    method: 'DELETE',
                    credentials: "include", 
                }
            ).then(response => {
                if (response.ok) {
                    return response.json()
                }
              
                console.error("Failed to delete the tag")
            })
        },
        {
            pending: state => {

            },
            fulfilled: (state, action) => {
                const { wishlist_id, tag_id } = action.payload
                if (
                    state.current && 
                    state.current.wishlist_id === wishlist_id
                ) {
                    state.current.tags = state.current.tags.filter(
                        tag => 
                            tag.tag_id !== tag_id
                    )
                } else {
                    console.warn(
                      `Incoming tag data response for wishlist ${wishlist_id},
                      but the wishlist view expired.`,
                    )
                    console.log("Response is ignored.")
                }
            },
            rejected: state => {
                console.error("Failed to delete the tag")
            },
        },
    ),
    createWishlist: create.asyncThunk(
        async (args: {
            name: string
            description: string
            user_account_id: string
        }): Promise<any> => {
            const { name, description, user_account_id } = args
            return fetch(
                `${BASE_URL}/wishlist/create/${user_account_id}`, 
                {
                    method: 'POST',
                    credentials: "include",     //check if user is logged in
                    body: JSON.stringify({ name: name, description: description }),
                }
            ).then(response => {
                if (response.ok) {
                    return response.json()
                }

                console.error("Failed to create the wishlist")
            })
        },
        {
            pending: state => {

            },
            fulfilled: (state, action) => {
                state.allWishlists.push(action.payload)
            },

            rejected: state => {
                console.error("Failed to create the wishlist")
            },
        },
    ),
    fetchAllWishlists: create.asyncThunk(
        async (args: {
            user_account_id: string
            link_permission_id?: string //optional
        }): Promise<any> => {
            const { user_account_id, link_permission_id } = args
            return fetch(
                `${BASE_URL}/wishlist/view_by_user/${user_account_id}}`, 
                {
                    method: 'GET',
                    credentials: "include",
            }
            ).then(response => {
                if (response.ok) {
                    return response.json()
                }
                console.error("Failed to get the wishlists")
            })
        },
        {
            pending: state => {

            },

            fulfilled: (state, action) => {
                state.allWishlists = action.payload
            },

            rejected: state => {
                console.error("Failed to get the wishlists")
            },
        },
    ),
      fetchItems: create.asyncThunk(
            async (args: {
                wishlist_id: string
                link_permission_id?: string //optional
            }): Promise<any> => {
                const { wishlist_id, link_permission_id } = args
                return fetch(
                    `${BASE_URL}/view_wishlist_items/${wishlist_id}?link_permission_id=${link_permission_id}`,
                    {
                        credentials: 'include',
                    }
                ).then(response => {
                    if (response.ok) {
                        return response.json()
                    }

                    console.error('Failed to fetch items')
                })
            },
            {
                pending: state => {
                    // do nothing
                },
                fulfilled: (state, action) => {
                    const { wishlist_id, items } = action.payload
                    if (
                        state.current &&
                        state.current.wishlist_id === wishlist_id
                    ) {
                        // response is valid
                        state.current.items = items
                    } else {
                        // the user closed or switched wishlist view
                        // response expired, do nothing
                        console.warn(
                            `Incoming items response for wishlist ${wishlist_id},
                    but the wishlist view expired.`
                        )
                        console.log('Response is ignored.')
                    }
                },
                rejected: state => {
                    console.error('Failed to fetch items')
                },
            }
        ),
        createItem: create.asyncThunk(
            async (args: {
                wishlist_id: string
                name: string
                description: string
                link: string
                status: string
                link_permission_id?: string //optional
            }): Promise<any> => {
                const { wishlist_id, name, description, link, status, link_permission_id} = args
                return fetch(`${BASE_URL}/create_item/${wishlist_id}??link_permission_id=${link_permission_id}`, {
                    method: 'POST',
                    credentials: 'include', // to enable cookies so that user account id can get through
                    body: JSON.stringify({
                        name: name,
                        description: description,
                        link: link,
                        status: status,
                    }),
                }).then(response => {
                    if (response.ok) {
                        return response.json()
                    }

                    console.error('Failed to create item')
                })
            },
            {
                pending: state => {
                    // do nothing
                },
                fulfilled: (state, action) => {
                    const {
                        wishlist_id,
                        item_id,
                        name,
                        description,
                        link,
                        status,
                    } = action.payload
                    if (
                        state.current &&
                        state.current.wishlist_id === wishlist_id
                    ) {
                        // response is valid
                        state.current.items.push({
                            item_id: item_id,
                            name: name,
                            description: description,
                            link: link,
                            status: status,
                            comments: []
                        })
                    } else {
                        // the user closed or switched wishlist view
                        // response expired, do nothing
                        console.warn(
                            `Incoming item response for wishlist ${wishlist_id},
                    but the wishlist view expired.`
                        )
                        console.log('Response is ignored.')
                    }
                },
                rejected: state => {
                    console.error('Failed to create item')
                },
            }
        ),
    fetchComment: create.asyncThunk(
      async (args: { item_id: string }): Promise<any> => {
        const { item_id } = args;
        return fetch(`${BASE_URL}/comment/${item_id}`, {
          method: "GET",
          credentials: "include", // to enable cookies so that user account id can get through
        })
          .then(response => {
            if (response.ok) {
              return response.json();
            }
            console.error('Failed to fetch comments');
            throw new Error('Failed to fetch comments');
          });
      },
      {
        pending: (state) => {
          // Update the state to indicate that the fetch operation is in progress
        },
        fulfilled: (state, action) => {
          const {item_id} = action.payload
          // Update the state with the fetched comments
          const item = state.current.items.find(item => item.item_id == item_id)
          if (item) {
            item.comments = action.payload.comments
          }
        },
        rejected: (state, action) => {
          // Update the state to indicate that the fetch operation failed
          console.error('Failed to fetch comments');
        },
      }
    ),
    createComment: create.asyncThunk(
      async (args: { comment: CommentState }): Promise<any> => {
        const { comment } = args;
        return fetch(`${BASE_URL}/comment/${comment.item_id}`, {
          method: 'POST',
          credentials: "include",
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(comment),
        })
          .then(response => {
            if (response.ok) {
              return response.json();
            }
            console.error('Failed to create comment');
          });
      },
      {
        pending: state => {
          // Handle the pending state if necessary
        },
        fulfilled: (state, action) => {
          const {comment} = action.payload
          // Add the new comment to the state
          const item = state.current.items.find(item => item.item_id == comment.item_id)

          if (item) {
            item.comments.push(comment)
          }
        },
        rejected: state => {
          console.error('Failed to create comment');
        },
      }
    ),
    updateComment: create.asyncThunk(
      async (args: { comment: CommentState }): Promise<any> => {
        const { comment } = args;
        return fetch(`${BASE_URL}/comment/${comment.comment_id}`, {
          method: 'PUT',
          credentials: "include",
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(comment),
        })
          .then(response => {
            if (response.ok) {
              return response.json();
            }
            console.error('Failed to update comment');
          });
      },
      {
        pending: state => {
          // Handle the pending state if necessary
        },
        fulfilled: (state, action) => {
          const {comment} = action.payload
          // Find the comment in the state and update it
          const itemIndex = state.current.items.findIndex(item => item.item_id == comment.item_id)
          if (itemIndex !== -1) {
            let commentIndex = state.current.items[itemIndex].comments.findIndex(c => c.comment_id == comment.comment_id);
            state.current.items[itemIndex].comments[commentIndex] = comment;
          }
        },
        rejected: state => {
          console.error('Failed to update comment');
        },
      }
    ),
    deleteComment: create.asyncThunk(
      async (args: { comment_id: string }): Promise<any> => {
        const { comment_id } = args;
        return fetch(`${BASE_URL}/comment/${comment_id}`, {
          method: 'DELETE',
          credentials: "include"
        })
          .then(response => {
            if (response.ok) {
              return response.json();
            }
            console.error('Failed to delete comment');
          });
      },
      {
        pending: state => {
          // Handle the pending state if necessary
        },
        fulfilled: (state, action) => {
          // Remove the comment from the state
          const {comment_id} = action.payload
          const itemIndex = state.current.items.findIndex(item => item.item_id == action.payload.item_id)
          if (itemIndex !== -1) {
            state.current.items[itemIndex].comments = state.current.items[itemIndex].comments.filter(c => c.comment_id !== comment_id);
          }
        },
        rejected: state => {
          console.error('Failed to delete comment');
        },
      }
    ),
  }),
})         

export const {
    setCurrentWishlist,
    setMockCurrentWishlist,
    setPermissionOpened,
    setLinkPermissionOpened,
    setLinkPermissionCreateNew,
    setLinkPermissionView,
    setLinkPermissionEdit,
    setLinkPermissionEditItems,
    setLinkPermissionEditTags,
    setLinkPermissionEditItemTags,
    setLinkPermissionComment,
    setDialogOpen,
    updateName,
    updateDescription,
    fetchLinkPermissions,
    createLinkPermission,
    updateLinkPermission,
    revokeLinkPermission,
    setUserPermissionOpened,
    setUserPermissionEditing,
    setUserPermissionCreateNew,
    setUserPermissionView,
    setUserPermissionEdit,
    setUserPermissionEditItems,
    setUserPermissionEditTags,
    setUserPermissionEditItemTags,
    setUserPermissionComment,
    fetchUserPermissions,
    createUserPermission,
    updateUserPermission,
    revokeUserPermission,
    fetchWishlist,
    updateWishlist,
    deleteWishlist,
    createTag,
    updateTag,
    deleteTag,
    createWishlist, 
    fetchAllWishlists,
    fetchItems,
    createItem,
    fetchComment,
    createComment,
    deleteComment,
} = wishlistSlice.actions
