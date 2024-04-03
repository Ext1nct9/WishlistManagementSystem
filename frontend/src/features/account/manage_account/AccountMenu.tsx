import Button from '@mui/material/Button' // Assuming you're using Material-UI
import { useAppDispatch, useAppSelector } from '../../../app/hooks'
import { client_base_url } from '../../../appsettings.json'
import {
    fetchAccountInfo,
    setHandleGetAccountError,
    setHandleGetAccountHasError,
} from '../accountSlice'

export const AccountMenu = () => {
    const MANAGE_ACCOUNT_URL = 'manage_account'

    const dispatch = useAppDispatch()

    const goToManageAccount = async () => {
        try {
            let action = await dispatch(fetchAccountInfo())

            if (action.error) {
                throw action.error
            }

            window.location.href = `${client_base_url}/${MANAGE_ACCOUNT_URL}`
        } catch (error) {
            window.alert(error.message)
            //dispatch(setHandleGetAccountHasError(true))
            //dispatch(setHandleGetAccountError(error.message))
        }
    }

    return (
        <Button color='inherit' onClick={goToManageAccount}>
            Manage my account
        </Button>
    )
}
