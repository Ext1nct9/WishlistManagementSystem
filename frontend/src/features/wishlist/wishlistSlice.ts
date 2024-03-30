import type { PayloadAction, Slice } from "@reduxjs/toolkit/react"
import type { PermissionState } from "../permission/permissionState"
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
  // TODO: other states if necessary
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
        user_permissions: []
      },
      link: {
        opened: null,
        editing: {
            view: false,
            edit: false,
            edit_items: false,
            edit_tags: false,
            edit_item_tags: false,
            comment: false,
        },
        link_permissions: []
      },
    },
    // TODO: other states if necessary
  }
}

export type WishlistSliceState = {
  current: null | undefined | WishlistState // The current wishlist opened in a wishlist view by the user
  // TODO: other states if necessary
  allWishlists: null | undefined | CompactWishlistState[] // All wishlists of the user

}

const initialState: WishlistSliceState = {
  current: undefined,
  allWishlists: [],
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
                ) {
                    state.current.permissions.link.opened = null
                    state.current.permissions.link.editing = {
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
    fetchLinkPermissions: create.asyncThunk(
      async (wishlist_id: string): Promise<any> => {
        fetch(`${BASE_URL}/wishlist/${wishlist_id}/permission_link`, {
          credentials: "same-origin", // to enable cookies so that user account id can get through
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
            state.current.permissions.link = permission_links
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
            fetch(`${BASE_URL}/wishlist/${wishlist_id}/permission_link`, {
            method: "POST",
            credentials: "same-origin", // to enable cookies so that user account id can get through
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
            fetch(
                `${BASE_URL}/wishlist/${wishlist_id}/permission_link/${link_permission_id}`,
                {
                    method: 'PUT',
                    credentials: 'same-origin', // to enable cookies so that user account id can get through
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
            fetch(
                `${BASE_URL}/wishlist/${wishlist_id}/permission_link/${link_permission_id}`,
                {
                    method: 'DELETE',
                    credentials: 'same-origin', // to enable cookies so that user account id can get through
                }
            ).then(response => {
                if (response.ok) {
                    return response.json()
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
                ) {
                    state.current.permissions.user.opened = null
                } else {
                    state.current.permissions.user.opened = action.payload
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
    fetchUserPermissions: create.asyncThunk(
        async (wishlist_id: string): Promise<any> => {
            fetch(`${BASE_URL}/get_user_permissions/${wishlist_id}`, {
                credentials: 'same-origin', // to enable cookies so that user account id can get through
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
                const { wishlist_id, permission_users } = action.payload
                if (state.current && state.current.wishlist_id === wishlist_id) {
                    // response is valid
                    state.current.permissions.user = permission_users
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
            user_account_id: string,
            wishlist_id: string,
            permissions: number,
        }): Promise<any> => {
            const { user_account_id, wishlist_id, permissions } = args
            fetch(
                `${BASE_URL}/user_permission/${user_account_id}/${wishlist_id}`,
                {
                    method: 'POST',
                    credentials: 'same-origin', // to enable cookies so that user account id can get through
                    body: JSON.stringify({ permissions: permissions }),
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
            fetch(
                `${BASE_URL}/user_permission/${user_account_id}/${wishlist_id}`,
                {
                    method: 'PUT',
                    credentials: 'same-origin', // to enable cookies so that user account id can get through
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
            fetch(
                `${BASE_URL}/user_permission/${user_account_id}/${wishlist_id}`,
                {
                    method: 'DELETE',
                    credentials: 'same-origin', // to enable cookies so that user account id can get through
                }
            ).then(response => {
                if (response.ok) {
                    return response.json()
                }
                console.error('Failed to revoke user permissions')
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
            fetch(
                `${BASE_URL}/wishlist/view/${wishlist_id}?link_permission_id=${link_permission_id}`, {
                credentials: "same-origin", 
            }).then(response => {
                if (response.ok) {
                    return response.json()
                }
              
                console.error("Failed to get the wishlist")
            })
        },
        {
            pending: state => {

            },
            fulfilled: (state, action) => {
                const { wishlist_id, name, description } = action.payload
                if (
                    state.current &&
                    state.current.wishlist_id === wishlist_id
                ) {
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
            rejected: state => {
                console.error("Failed to get the wishlist")
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
            fetch(
                `${BASE_URL}/wishlist/view/${wishlist_id}?link_permission_id=${link_permission_id}`, 
                {
                    method: 'PUT',
                    credentials: "same-origin", 
                }
            ).then(response => {
                if (response.ok) {
                    return response.json()
                }
              
                console.error("Failed to update the wishlist")
            })
        },
        {
            pending: state => {

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
            rejected: state => {
                console.error("Failed to update the wishlist")
            },
        },
    ),
    deleteWishlist: create.asyncThunk(
        async (args: {
            wishlist_id: string
           }): Promise<any> => {
            const { wishlist_id } = args
            fetch(
                `${BASE_URL}/wishlist/delete/${wishlist_id}`, 
                {
                    method: 'DELETE',
                    credentials: "same-origin", 
                }
            ).then(response => {
                if (response.ok) {
                    return response.json()
                }
              
                console.error("Failed to delete the wishlist")
            })
        },
        {
            pending: state => {

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
            rejected: state => {
                console.error("Failed to delete the wishlist")
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
            fetch(
                `${BASE_URL}/wishlist/create/${user_account_id}`, 
                {
                    method: 'POST',
                    credentials: "same-origin",     //check if user is logged in
                    body: JSON.stringify({ name: name, description: description }),
                }
            ).then(response => {
                if (response.ok) {
                    return response.json();
                }
              
                console.error("Failed to create the wishlist");
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
            const { user_account_id, link_permission_id } = args;
            fetch(
                `${BASE_URL}/wishlist/view_by_user/${user_account_id}}`, 
                {
                    method: 'GET',
                    credentials: "same-origin",
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
  }),
})

export const {
    setCurrentWishlist,
    setMockCurrentWishlist,
    setPermissionOpened,
    setLinkPermissionOpened,
    setLinkPermissionView,
    setLinkPermissionEdit,
    setLinkPermissionEditItems,
    setLinkPermissionEditTags,
    setLinkPermissionEditItemTags,
    setLinkPermissionComment,
    fetchLinkPermissions,
    createLinkPermission,
    updateLinkPermission,
    revokeLinkPermission,
    setUserPermissionOpened,
    setUserPermissionEditing,
    fetchUserPermissions,
    createUserPermission,
    updateUserPermission,
    revokeUserPermission,
    fetchWishlist,
    updateWishlist,
    deleteWishlist,
} = wishlistSlice.actions