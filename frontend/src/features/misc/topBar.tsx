import AppBar from '@mui/material/AppBar'
import Box from '@mui/material/Box'
import Toolbar from '@mui/material/Toolbar'
import Button from '@mui/material/Button'
import { useAppSelector, useAppDispatch } from '../../app/hooks'
import {
    AccountSliceState,
    logout,
    selectIsLoggedIn,
} from '../account/accountSlice'
import { AccountMenu } from '../account/manage_account/AccountMenu'

export default function TopBar() {
    const dispatch = useAppDispatch()
    const isLoggedIn = useAppSelector(selectIsLoggedIn)

    async function handleLogout() {
        try {
            let action = await dispatch(logout({}))
            if (action.error) {
                throw action.error
            }
            window.alert('Logout successful')
            window.location.href = '/'
        } catch (error) {
            window.alert(`${error.message}`)
            console.error(error)
        }
    }

    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position='static'>
                <Toolbar sx={{ justifyContent: 'space-between' }}>
                    <Button color='inherit' href='/'>
                        Listful
                    </Button>

                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        {isLoggedIn && <AccountMenu />}
                        {useAppSelector(
                            (state: AccountSliceState) =>
                                state.account.userAccountId
                        ) ? (
                            <Button
                                color='inherit'
                                sx={{ marginLeft: 5 }}
                                onClick={handleLogout}
                            >
                                Logout
                            </Button>
                        ) : (
                            <Button
                                color='inherit'
                                sx={{ marginLeft: 5 }}
                                href='/login'
                            >
                                Login
                            </Button>
                        )}
                    </Box>
                </Toolbar>
            </AppBar>
        </Box>
    )
}
