import type { PayloadAction, Slice } from "@reduxjs/toolkit/react"
import type { PermissionState } from "../permission/permissionState"
import { createAppSlice } from "../../app/createAppSlice"
import { server_base_url as BASE_URL } from "../../appsettings.json"

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
      user: [],
      link: [],
    },
    // TODO: other states if necessary
  }
}

export type WishlistSliceState = {
  current: null | undefined | WishlistState // The current wishlist opened in a wishlist view by the user
  // TODO: other states if necessary
}

const initialState: WishlistSliceState = {
  current: undefined,
}

export const wishlistSlice: Slice = createAppSlice({
  name: "wishlist",
  initialState,
  reducers: create => ({
    setCurrentWishlist: create.reducer(
      (state, action: PayloadAction<WishlistResponse>) => {
        state.current = initializeWishlistState(
          action.payload.wishlist_id,
          action.payload.name,
          action.payload.description,
          action.payload.user_account_id,
        )
      },
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
                    state.current.permissions.link.push({
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
                        state.current.permissions.link.find(
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
                    state.current.permissions.link =
                        state.current.permissions.link.filter(
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
                    body: JSON.stringify({ name: name, description: description }),
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
  }),
})