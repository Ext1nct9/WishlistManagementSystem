// store all permissions for the wishlist.
// ATTENTION: permissions can be empty if they are not fetched
// and you usually don't need to fetch them if you're not directly editing permissions.
// You can only expect this field to be filled only if you have the "edit permissions" component open.
export type PermissionState = {
  user: {
    user_account_id: string
    permissions: number
  }[]
  link: {
    link_permission_id: string
    permissions: number
  }[]
}
