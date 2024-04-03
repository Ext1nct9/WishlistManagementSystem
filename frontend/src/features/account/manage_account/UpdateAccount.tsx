import { useAppDispatch, useAppSelector } from '../../../app/hooks'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import Box from '@mui/material/Box'
import Dialog from '@mui/material/Dialog'
import {
    selectUserAccountId,
    selectEmailError,
    selectEmail,
    selectEmailHasError,
    selectUsername,
    selectUsernameHasError,
    selectUsernameError,
    selectPasswordHasError,
    selectPasswordError,
    setHandleUpdateOpen,
    setHandleUpdateEmail,
    setHandleUpdateUsername,
    setHandleUpdatePassword,
    selectUpdateOpen,
    setHandleEditEmailOpen,
    setHandleEditUsernameOpen,
    setHandleEditPasswordOpen,
    selectUpdateEmail,
    selectUpdatePassword,
    selectUpdateUsername,
    updateAccountEmail,
    updateAccountPassword,
    updateAccountUsername,
    setHandleEditEmailHasError,
    setHandleEditEmailError,
    setHandleEditEmailReset,
    selectPassword,
    setHandleEditUsernameError,
    setHandleEditUsernameHasError,
    setHandleEditUsernameReset,
    setHandleEditPasswordError,
    setHandleEditPasswordHasError,
    setHandleEditPasswordReset,
    fetchAccountInfo,
} from '../accountSlice'

export const UpdateAccount = ({
    editEmailOpen,
    editUsernameOpen,
    editPasswordOpen,
}) => {
    const dispatch = useAppDispatch()
    const updateOpen = useAppSelector(selectUpdateOpen)
    const userAccountId = useAppSelector(selectUserAccountId)
    const currentEmail = useAppSelector(selectEmail)
    const updateEmail = useAppSelector(selectUpdateEmail)
    const emailHasError = useAppSelector(selectEmailHasError)
    const emailError = useAppSelector(selectEmailError)
    const currentUsername = useAppSelector(selectUsername)
    const updateUsername = useAppSelector(selectUpdateUsername)
    const usernameHasError = useAppSelector(selectUsernameHasError)
    const usernameError = useAppSelector(selectUsernameError)
    const currentPassword = useAppSelector(selectPassword)
    const updatePassword = useAppSelector(selectUpdatePassword)
    const passwordHasError = useAppSelector(selectPasswordHasError)
    const passwordError = useAppSelector(selectPasswordError)

    const handleClose = () => {
        dispatch(setHandleUpdateOpen(false))
        dispatch(setHandleEditEmailOpen(false))
        dispatch(setHandleEditUsernameOpen(false))
        dispatch(setHandleEditPasswordOpen(false))
        dispatch(setHandleEditEmailHasError(false))
        dispatch(setHandleEditEmailError(''))
        dispatch(setHandleEditUsernameHasError(false))
        dispatch(setHandleEditUsernameError(''))
        dispatch(setHandleEditPasswordHasError(false))
        dispatch(setHandleEditPasswordError(''))
    }

    const handleUpdateEmail = event => {
        dispatch(setHandleEditEmailHasError(false))
        dispatch(setHandleEditEmailError(''))
        dispatch(setHandleUpdateEmail(event.target.value))
    }

    async function handleUpdateAccountEmail() {
        try {
            const account_info = {
                userAccountId: userAccountId,
                email: updateEmail,
            }
            let action = await dispatch(updateAccountEmail(account_info))

            // There was an error
            if (action.error) {
                throw action.error
            }

            // There was no error
            dispatch(setHandleEditEmailOpen(false))
            dispatch(setHandleUpdateOpen(false))
        } catch (error) {
            // Handle the error
            dispatch(setHandleEditEmailHasError(true))
            dispatch(setHandleEditEmailError(error.message))
            dispatch(setHandleEditEmailReset(currentEmail))
        }
    }

    const handleUpdateUsername = event => {
        dispatch(setHandleUpdateUsername(event.target.value))
    }

    async function handleUpdateAccountUsername() {
        try {
            const account_info = {
                userAccountId: userAccountId,
                username: updateUsername,
            }
            let action = await dispatch(updateAccountUsername(account_info))

            if (action.error) {
                throw action.error
            }

            dispatch(setHandleEditUsernameOpen(false))
            dispatch(setHandleUpdateOpen(false))
        } catch (error) {
            dispatch(setHandleEditUsernameHasError(true))
            dispatch(setHandleEditUsernameError(error.message))
            dispatch(setHandleEditUsernameReset(currentUsername))
        }
    }
    const handleUpdatePassword = event => {
        dispatch(setHandleUpdatePassword(event.target.value))
    }

    async function handleUpdateAccountPassword() {
        try {
            const account_info = {
                userAccountId: userAccountId,
                password: updatePassword,
            }
            let action = await dispatch(updateAccountPassword(account_info))

            if (action.error) {
                throw action.error
            }

            dispatch(setHandleEditPasswordOpen(false))
            dispatch(setHandleUpdateOpen(false))
            dispatch(fetchAccountInfo())
        } catch (error) {
            dispatch(setHandleEditPasswordHasError(true))
            dispatch(setHandleEditPasswordError(error.message))
            dispatch(setHandleEditPasswordReset(currentPassword))
        }
    }
    return (
        <Dialog onClose={handleClose} open={updateOpen}>
            <Box
                width={600}
                display='flex'
                alignItems='center'
                flexDirection='column'
                sx={{
                    borderRadius: 2,
                    bgcolor: 'grey.300',
                }}
            >
                {editEmailOpen && (
                    <Box mb={4} mt={4} width={500}>
                        <TextField
                            label='New Email'
                            defaultValue={currentEmail}
                            fullWidth
                            error={emailHasError}
                            helperText={emailError}
                            onChange={handleUpdateEmail}
                        />
                    </Box>
                )}

                {editUsernameOpen && (
                    <Box mb={4} mt={4} width={500}>
                        <TextField
                            label='New Username'
                            defaultValue={currentUsername}
                            fullWidth
                            error={usernameHasError}
                            helperText={usernameError}
                            onChange={handleUpdateUsername}
                        />
                    </Box>
                )}

                {editPasswordOpen && (
                    <Box mb={4} mt={4} width={500}>
                        <TextField
                            label='New Password'
                            type='password'
                            defaultValue={'**********'}
                            fullWidth
                            error={passwordHasError}
                            helperText={passwordError}
                            onChange={handleUpdatePassword}
                        />
                    </Box>
                )}

                <Box mb={4} sx={{ display: 'flex', gap: '30px' }}>
                    <Button
                        variant='contained'
                        color='error'
                        onClick={handleClose}
                    >
                        Cancel
                    </Button>
                    {editEmailOpen && (
                        <Button
                            variant='contained'
                            onClick={handleUpdateAccountEmail}
                        >
                            Update Account
                        </Button>
                    )}
                    {editUsernameOpen && (
                        <Button
                            variant='contained'
                            onClick={handleUpdateAccountUsername}
                        >
                            Update Account
                        </Button>
                    )}
                    {editPasswordOpen && (
                        <Button
                            variant='contained'
                            onClick={handleUpdateAccountPassword}
                        >
                            Update Account
                        </Button>
                    )}
                </Box>
            </Box>
        </Dialog>
    )
}
