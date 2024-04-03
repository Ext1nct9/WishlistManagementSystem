import { PayloadAction, Slice } from '@reduxjs/toolkit'
import { createAppSlice } from '../../app/createAppSlice'
import { server_base_url } from '../../appsettings.json'
import { DeleteAccountState } from './manage_account/manageAccountState'
import { GetAccountInformation } from './manage_account/manageAccountState'
import { UpdateAccountState } from './manage_account/manageAccountState'

// Define initial state
export interface AccountSliceState {
    userAccountId: string
    email: string
    username: string
    password: string
    getAccountInfoVars: GetAccountInformation
    isLoggedIn: boolean
    updateAccountVars: UpdateAccountState
    deleteAccountVars: DeleteAccountState
}

// Define initial state
const initialState: AccountSliceState = {
    userAccountId: '',
    email: '',
    username: '',
    password: '',
    getAccountInfoVars: {
        getAccountHasError: false,
        getAccountError: '',
    },
    isLoggedIn: false,
    updateAccountVars: {
        updateOpen: false,
        editEmailOpen: false,
        updateEmail: '',
        emailHasError: false,
        emailError: '',
        editUsernameOpen: false,
        updateUsername: '',
        usernameHasError: false,
        usernameError: '',
        editPasswordOpen: false,
        updatePassword: '',
        passwordHasError: false,
        passwordError: '',
    },
    deleteAccountVars: {
        confirmationOpen: false,
        confirmationPassword: '',
        deleteAccountHasError: false,
        deleteAccountError: '',
    },
}

export const accountSlice: Slice = createAppSlice({
    // Define account slice
    name: 'account',
    initialState,
    reducers: create => ({
        // Define async thunk for creating account information
        createAccount: create.asyncThunk(
            async (args: {
                email: string
                username: string
                password: string
            }): Promise<any> => {
                const { email, username, password } = args
                return fetch(`${server_base_url}/create_account`, {
                    // Return payload
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email,
                        username: username,
                        password: password,
                    }),
                }).then(async response => {
                    if (response.ok) {
                        console.log('Account created successfully')
                        return response.json()
                    } else {
                        const errorData = await response.json()
                        const error = new Error('Failed to create account')
                        error.message = `${errorData.error_msg}, Status code: ${response.status}`
                        throw error
                    }
                })
            },
            {
                pending: state => {
                    // do nothing
                },
                fulfilled: (state, action) => {
                    if (!state) {
                        // the user closed account creation view or response expired, do nothing
                        console.warn(
                            `Incoming account creation, but the session expired.`
                        )
                        console.log('Response is ignored.')
                    }
                },
                rejected: state => {
                    console.error('Failed to create account')
                },
            }
        ),
        login: create.asyncThunk(
            async (args: { email: string; password: string }): Promise<any> => {
                const { email, password } = args
                return fetch(`${server_base_url}/login`, {
                    method: 'POST',
                    credentials: 'include', // to enable cookies so that user account id can get through
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password,
                    }),
                }).then(async response => {
                    if (response.ok) {
                        console.log('Successful Login')
                        // return response.json() Throws 'Unexpected end of JSON input' error because no response body
                    } else {
                        const errorData = await response.json()
                        const error = new Error('Failed to login')
                        error.message = `${errorData.error_msg}, Status code: ${response.status}`
                        throw error
                    }
                })
            },
            {
                pending: state => {
                    // do nothing
                },
                fulfilled: (state, action) => {
                    state.isLoggedIn = true
                    if (!state) {
                        // the user closed login view or response expired, do nothing
                        console.warn(`Incoming login, but the session expired.`)
                        console.log('Response is ignored.')
                    }
                },
                rejected: state => {
                    console.error('Failed to login')
                },
            }
        ),

        // Define async thunk for fetching account information
        fetchAccountInfo: create.asyncThunk(
            async (): Promise<any> => {
                return fetch(`${server_base_url}/get_account`, {
                    method: 'GET',
                    credentials: 'include', // to enable cookies so that user account id can get through
                    headers: {
                        'Content-Type': 'application/json', // or whatever your server expects
                        Accept: 'application/json', // or whatever your server sends
                    },
                }).then(async response => {
                    if (response.ok) {
                        return response.json()
                    } else {
                        const errorData = await response.json()
                        const error = new Error('Failed to login')
                        error.message = `${errorData.error_msg}, Status code: ${response.status}`
                        throw error
                    }
                })
            },
            {
                pending: (state, action) => {
                    // do nothing
                },
                fulfilled: (state, action) => {
                    const { user_account_id, email, username, password } =
                        action.payload
                    // response is valid
                    state.userAccountId = user_account_id
                    state.email = email
                    state.username = username
                    state.password = password
                    state.updateAccountVars.updateEmail = email
                    state.updateAccountVars.updateUsername = username
                    state.updateAccountVars.updatePassword = password
                },
                rejected: (state, action) => {
                    // necessary state changes handled from the .tsx file
                },
            }
        ),
        setHandleGetAccountHasError: create.reducer(
            (state, action: PayloadAction<boolean>) => {
                state.getAccountInfoVars.getAccountHasError = action.payload
            }
        ),
        setHandleGetAccountError: create.reducer(
            (state, action: PayloadAction<string>) => {
                state.getAccountInfoVars.getAccountError = action.payload
            }
        ),

        logout: create.asyncThunk(
            async (): Promise<any> => {
                return fetch(`${server_base_url}/logout`, {
                    method: 'POST',
                    credentials: 'include', // to enable cookies so that user account id can get through
                }).then(async response => {
                    if (response.ok) {
                        console.log('Logged out successfully')
                    } else {
                        const errorData = await response.json()
                        const error = new Error('Failed to logout')
                        error.message = `${errorData.error_msg}, Status code: ${response.status}`
                        throw error
                    }
                })
            },
            {
                pending: state => {
                    // do nothing
                },
                fulfilled: state => {
                    state.userAccountId = ''
                    state.email = ''
                    state.username = ''
                    state.password = ''
                    state.getAccountInfoVars = {
                        getAccountHasError: false,
                        getAccountError: '',
                    }
                    state.isLoggedIn = false
                    state.updateAccountVars = {
                        updateOpen: false,
                        editEmailOpen: false,
                        updateEmail: '',
                        emailHasError: false,
                        emailError: '',
                        editUsernameOpen: false,
                        updateUsername: '',
                        usernameHasError: false,
                        usernameError: '',
                        editPasswordOpen: false,
                        updatePassword: '',
                        passwordHasError: false,
                        passwordError: '',
                    }
                    state.deleteAccountVars = {
                        confirmationOpen: false,
                        confirmationPassword: '',
                        deleteAccountHasError: false,
                        deleteAccountError: '',
                    }
                },
                rejected: state => {
                    console.error('Failed to logout')
                },
            }
        ),

        setHandleUpdateOpen: create.reducer(
            (state, action: PayloadAction<boolean>) => {
                state.updateAccountVars.updateOpen = action.payload
            }
        ),
        // Define async thunk for updating account email
        updateAccountEmail: create.asyncThunk(
            async (account_info: {
                userAccountId: string
                email: string
            }): Promise<any> => {
                const { userAccountId, email } = account_info
                return fetch(`${server_base_url}/update_account_email`, {
                    method: 'PUT',
                    credentials: 'include', // to enable cookies so that user account id can get through
                    headers: {
                        'Content-Type': 'application/json',
                        Accept: 'application/json',
                    },
                    body: JSON.stringify({
                        user_account_id: userAccountId,
                        email: email,
                    }),
                }).then(async response => {
                    if (response.ok) {
                        return response.json()
                    } else {
                        const errorData = await response.json()
                        const error = new Error('Failed to update account')
                        error.message = `${errorData.error_msg} \n Status code: ${response.status}`
                        throw error
                    }
                })
            },
            {
                pending: (state, action) => {
                    // do nothing
                },
                fulfilled: (state, action) => {
                    const { user_account_id, email } = action.payload
                    // response is valid
                    state.email = email
                    state.updateAccountVars.updateEmail = email
                },
                rejected: (state, action) => {
                    // necessary state changes handled from the .tsx file
                },
            }
        ),
        setHandleEditEmailHasError: create.reducer(
            (state, action: PayloadAction<boolean>) => {
                state.updateAccountVars.emailHasError = action.payload
            }
        ),
        setHandleEditEmailError: create.reducer(
            (state, action: PayloadAction<string>) => {
                state.updateAccountVars.emailError = action.payload
            }
        ),
        setHandleEditEmailReset: create.reducer(
            (state, action: PayloadAction<string>) => {
                state.updateAccountVars.updateEmail = action.payload
            }
        ),
        setHandleEditEmailOpen: create.reducer(
            (state, action: PayloadAction<boolean>) => {
                state.updateAccountVars.editEmailOpen = action.payload
            }
        ),
        setHandleUpdateEmail: create.reducer(
            (state, action: PayloadAction<string>) => {
                state.updateAccountVars.updateEmail = action.payload
            }
        ),
        // Define async thunk for updating account username
        updateAccountUsername: create.asyncThunk(
            async (account_info: {
                userAccountId: string
                username: string
            }): Promise<any> => {
                const { userAccountId, username } = account_info
                return fetch(`${server_base_url}/update_account_username`, {
                    method: 'PUT',
                    credentials: 'include', // to enable cookies so that user account id can get through
                    headers: {
                        'Content-Type': 'application/json',
                        Accept: 'application/json',
                    },
                    body: JSON.stringify({
                        user_account_id: userAccountId,
                        username: username,
                    }),
                }).then(async response => {
                    if (response.ok) {
                        return response.json()
                    } else {
                        const errorData = await response.json()
                        const error = new Error('Failed to update account')
                        error.message = `${errorData.error_msg} \n Status code: ${response.status}`
                        throw error
                    }
                })
            },
            {
                pending: (state, action) => {
                    // do nothing
                },
                fulfilled: (state, action) => {
                    const { user_account_id, username } = action.payload
                    // response is valid
                    state.username = username
                    state.updateAccountVars.updateUsername = username
                },
                rejected: (state, action) => {
                    // necessary state changes handled from the .tsx file
                },
            }
        ),
        setHandleEditUsernameHasError: create.reducer(
            (state, action: PayloadAction<boolean>) => {
                state.updateAccountVars.usernameHasError = action.payload
            }
        ),
        setHandleEditUsernameError: create.reducer(
            (state, action: PayloadAction<string>) => {
                state.updateAccountVars.usernameError = action.payload
            }
        ),
        setHandleEditUsernameReset: create.reducer(
            (state, action: PayloadAction<string>) => {
                state.updateAccountVars.updateUsername = action.payload
            }
        ),
        setHandleEditUsernameOpen: create.reducer(
            (state, action: PayloadAction<boolean>) => {
                state.updateAccountVars.editUsernameOpen = action.payload
            }
        ),
        setHandleUpdateUsername: create.reducer(
            (state, action: PayloadAction<string>) => {
                state.updateAccountVars.updateUsername = action.payload
            }
        ),
        // Define async thunk for updating account username
        updateAccountPassword: create.asyncThunk(
            async (account_info: {
                userAccountId: string
                password: string
            }): Promise<any> => {
                const { userAccountId, password } = account_info
                return fetch(`${server_base_url}/update_account_password`, {
                    method: 'PUT',
                    credentials: 'include', // to enable cookies so that user account id can get through
                    headers: {
                        'Content-Type': 'application/json',
                        Accept: 'application/json',
                    },
                    body: JSON.stringify({
                        user_account_id: userAccountId,
                        password: password,
                    }),
                }).then(async response => {
                    if (response.ok) {
                        return response.json()
                    } else {
                        const errorData = await response.json()
                        const error = new Error('Failed to update account')
                        error.message = `${errorData.error_msg} \n Status code: ${response.status}`
                        throw error
                    }
                })
            },
            {
                pending: (state, action) => {
                    // do nothing
                },
                fulfilled: (state, action) => {
                    // necessary state changes handled from the .tsx file
                },
                rejected: (state, action) => {
                    // necessary state changes handled from the .tsx file
                },
            }
        ),
        setHandleEditPasswordHasError: create.reducer(
            (state, action: PayloadAction<boolean>) => {
                state.updateAccountVars.passwordHasError = action.payload
            }
        ),
        setHandleEditPasswordError: create.reducer(
            (state, action: PayloadAction<string>) => {
                state.updateAccountVars.passwordError = action.payload
            }
        ),
        setHandleEditPasswordReset: create.reducer(
            (state, action: PayloadAction<string>) => {
                state.updateAccountVars.updatePassword = action.payload
            }
        ),
        setHandleEditPasswordOpen: create.reducer(
            (state, action: PayloadAction<boolean>) => {
                state.updateAccountVars.editPasswordOpen = action.payload
            }
        ),
        setHandleUpdatePassword: create.reducer(
            (state, action: PayloadAction<string>) => {
                state.updateAccountVars.updatePassword = action.payload
            }
        ),

        // Define async thunk for deleting account
        deleteAccount: create.asyncThunk(
            async (): Promise<any> => {
                return fetch(`${server_base_url}/delete_account`, {
                    method: 'DELETE',
                    credentials: 'include', // to enable cookies so that user account id can get through
                    headers: {
                        'Content-Type': 'application/json',
                        Accept: 'application/json',
                    },
                }).then(async response => {
                    if (response.status === 204) {
                        return null
                    } else {
                        const errorData = await response.json()
                        const error = new Error('Failed to delete account')
                        error.message = `${errorData.error_msg} \n Status code: ${response.status}`
                        throw error
                    }
                })
            },
            {
                pending: (state, action) => {
                    // do nothing
                },
                fulfilled: (state, action) => {
                    state = initialState
                },
                rejected: (state, action) => {
                    // handled from the .tsx file
                },
            }
        ),
        setHandleDeleteAccount: create.reducer(
            (state, action: PayloadAction<boolean>) => {
                state.deleteAccountVars.confirmationOpen = action.payload
            }
        ),
        setHandleConfirmationPassword: create.reducer(
            (state, action: PayloadAction<string>) => {
                state.deleteAccountVars.confirmationPassword = action.payload
            }
        ),
        // Define async thunk for verifying if the provided password is the proper one
        confirmDeleteAccount: create.asyncThunk(
            async (account_info: {
                userAccountId: string
                password: string
            }): Promise<any> => {
                const { userAccountId, password } = account_info
                return fetch(`${server_base_url}/delete_account_confirmation`, {
                    method: 'POST',
                    credentials: 'include', // to enable cookies so that user account id can get through
                    headers: {
                        'Content-Type': 'application/json',
                        Accept: 'application/json',
                    },
                    body: JSON.stringify({
                        user_account_id: userAccountId,
                        password: password,
                    }),
                }).then(async response => {
                    if (response.status === 204) {
                        return null
                    } else {
                        const errorData = await response.json()
                        const error = new Error('Failed to delete account')
                        error.message = `${errorData.error_msg} \n Status code: ${response.status}`
                        throw error
                    }
                })
            },
            {
                pending: (state, action) => {
                    // do nothing
                },
                fulfilled: (state, action) => {
                    // handled from the .tsx file
                },
                rejected: (state, action) => {
                    // handled from the .tsx file
                },
            }
        ),
        setHandleDeleteAccountHasError: create.reducer(
            (state, action: PayloadAction<boolean>) => {
                state.deleteAccountVars.deleteAccountHasError = action.payload
            }
        ),
        setHandleDeleteAccountError: create.reducer(
            (state, action: PayloadAction<string>) => {
                state.deleteAccountVars.deleteAccountError = action.payload
            }
        ),
    }),
    selectors: {
        selectIsLoggedIn: account => account.isLoggedIn,
        selectUserAccountId: account => account.userAccountId,
        selectEmail: account => account.email,
        selectUsername: account => account.username,
        selectPassword: account => account.password,
        selectGetAccountHasError: account =>
            account.getAccountInfoVars.getAccountHasError,
        selectGetAccountError: account =>
            account.getAccountInfoVars.getAccountError,
        selectUpdateOpen: account => account.updateAccountVars.updateOpen,
        selectEditEmailOpen: account => account.updateAccountVars.editEmailOpen,
        selectUpdateEmail: account => account.updateAccountVars.updateEmail,
        selectEmailHasError: account => account.updateAccountVars.emailHasError,
        selectEmailError: account => account.updateAccountVars.emailError,
        selectEditUsernameOpen: account =>
            account.updateAccountVars.editUsernameOpen,
        selectUpdateUsername: account =>
            account.updateAccountVars.updateUsername,
        selectUsernameHasError: account =>
            account.updateAccountVars.usernameHasError,
        selectUsernameError: account => account.updateAccountVars.usernameError,
        selectEditPasswordOpen: account =>
            account.updateAccountVars.editPasswordOpen,
        selectUpdatePassword: account =>
            account.updateAccountVars.updatePassword,
        selectPasswordHasError: account =>
            account.updateAccountVars.passwordHasError,
        selectPasswordError: account => account.updateAccountVars.passwordError,
        selectConfirmationOpen: account =>
            account.deleteAccountVars.confirmationOpen,
        selectConfirmationPassword: account =>
            account.deleteAccountVars.confirmationPassword,
        selectDeleteAccountHasError: account =>
            account.deleteAccountVars.deleteAccountHasError,
        selectDeleteAccountError: account =>
            account.deleteAccountVars.deleteAccountError,
    },
})
export const {
    selectIsLoggedIn,
    selectUserAccountId,
    selectEmail,
    selectUsername,
    selectPassword,
    selectGetAccountHasError,
    selectGetAccountError,
    selectUpdateOpen,
    selectEditEmailOpen,
    selectUpdateEmail,
    selectEmailHasError,
    selectEmailError,
    selectEditUsernameOpen,
    selectUpdateUsername,
    selectUsernameHasError,
    selectUsernameError,
    selectEditPasswordOpen,
    selectUpdatePassword,
    selectPasswordHasError,
    selectPasswordError,
    selectConfirmationOpen,
    selectConfirmationPassword,
    selectDeleteAccountHasError,
    selectDeleteAccountError,
} = accountSlice.selectors

export const {
    createAccount,
    login,
    logout,
    fetchAccountInfo,
    setHandleUpdateOpen,
    updateAccountEmail,
    setHandleEditEmailHasError,
    setHandleEditEmailError,
    setHandleEditEmailReset,
    setHandleEditEmailOpen,
    setHandleUpdateEmail,
    updateAccountUsername,
    setHandleEditUsernameOpen,
    setHandleEditUsernameHasError,
    setHandleEditUsernameError,
    setHandleEditUsernameReset,
    setHandleUpdateUsername,
    updateAccountPassword,
    setHandleEditPasswordOpen,
    setHandleEditPasswordHasError,
    setHandleEditPasswordError,
    setHandleEditPasswordReset,
    setHandleUpdatePassword,
    deleteAccount,
    confirmDeleteAccount,
    setHandleDeleteAccount,
    setHandleConfirmDeleteAccount,
    setHandleConfirmationPassword,
    setHandleDeleteAccountHasError,
    setHandleDeleteAccountError,
    setHandleGetAccountHasError,
    setHandleGetAccountError,
} = accountSlice.actions
