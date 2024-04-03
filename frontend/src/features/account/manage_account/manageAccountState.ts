export type GetAccountInformation = {
    getAccountHasError: boolean
    getAccountError: string
}

export type UpdateAccountState = {
    updateOpen: boolean
    editEmailOpen: boolean
    updateEmail: string
    emailHasError: boolean
    emailError: string
    editUsernameOpen: boolean
    updateUsername: string
    usernameHasError: boolean
    usernameError: string
    editPasswordOpen: boolean
    updatePassword: string
    passwordHasError: boolean
    passwordError: string
}

export type DeleteAccountState = {
    confirmationOpen: boolean
    confirmationPassword: string
    deleteAccountHasError: boolean
    deleteAccountError: string
}
