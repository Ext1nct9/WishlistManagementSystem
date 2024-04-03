import { useAppDispatch, useAppSelector } from '../../../app/hooks'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import Dialog from '@mui/material/Dialog'
import DialogActions from '@mui/material/DialogActions'
import DialogContent from '@mui/material/DialogContent'
import DialogContentText from '@mui/material/DialogContentText'
import DialogTitle from '@mui/material/DialogTitle'
import Box from '@mui/material/Box'
import { client_base_url } from '../../../appsettings.json'
import {
    selectUserAccountId,
    deleteAccount,
    setHandleDeleteAccount,
    selectConfirmationOpen,
    selectDeleteAccountError,
    selectDeleteAccountHasError,
    selectConfirmationPassword,
    setHandleConfirmationPassword,
    confirmDeleteAccount,
    setHandleDeleteAccountError,
    setHandleDeleteAccountHasError,
    logout,
} from '../accountSlice'

export const DeleteAccount = () => {
    const dispatch = useAppDispatch()
    const userAccountId = useAppSelector(selectUserAccountId)
    const confirmationOpen = useAppSelector(selectConfirmationOpen)
    const confirmationPassword = useAppSelector(selectConfirmationPassword)
    const deleteAccountHasError = useAppSelector(selectDeleteAccountHasError)
    const deleteAccountError = useAppSelector(selectDeleteAccountError)

    const handleDeleteAccount = () => {
        dispatch(setHandleDeleteAccount(true))
    }

    const handleConfirmationPassword = event => {
        dispatch(setHandleDeleteAccountHasError(false))
        dispatch(setHandleDeleteAccountError(''))
        dispatch(setHandleConfirmationPassword(event.target.value))
    }

    const handleClose = () => {
        dispatch(setHandleDeleteAccount(false))
        dispatch(setHandleConfirmationPassword(''))
        dispatch(setHandleDeleteAccountHasError(false))
        dispatch(setHandleDeleteAccountError(''))
    }

    async function handleConfirmDeleteAccount() {
        try {
            const account_info = {
                userAccountId: userAccountId,
                password: confirmationPassword,
            }

            let action = await dispatch(confirmDeleteAccount(account_info))

            // There was an error
            if (action && action.error) {
                throw action.error
            }

            // If there was no error
            await dispatch(deleteAccount())
            await dispatch(logout())
            window.location.href = `${client_base_url}/`
        } catch (error) {
            // Handle the error
            dispatch(setHandleDeleteAccountHasError(true))
            dispatch(setHandleDeleteAccountError(error.message))
        }
    }

    return (
        <Box>
            <Box
                mb={4}
                mt={4}
                width={200}
                flexDirection='column'
                display='flex'
                alignItems='center'
            >
                <Button
                    variant='contained'
                    color='warning'
                    onClick={handleDeleteAccount}
                >
                    Delete Account
                </Button>
            </Box>

            <Dialog open={confirmationOpen} onClose={handleClose}>
                <DialogTitle>Delete account</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        To delete your account permanently from Listful, please
                        enter your password below.
                    </DialogContentText>
                    <TextField
                        autoFocus
                        label='Password'
                        type='password'
                        variant='standard'
                        fullWidth
                        onChange={handleConfirmationPassword}
                        error={deleteAccountHasError}
                        helperText={deleteAccountError}
                    />
                </DialogContent>
                <DialogActions>
                    <Button
                        variant='contained'
                        color='success'
                        onClick={handleClose}
                    >
                        Cancel
                    </Button>
                    <Button
                        type='submit'
                        variant='contained'
                        color='error'
                        onClick={handleConfirmDeleteAccount}
                    >
                        Delete Account
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    )
}
