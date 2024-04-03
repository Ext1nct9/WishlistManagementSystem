import Box from '@mui/material/Box'
import Grid from '@mui/material/Grid'
import Typography from '@mui/material/Typography'
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem'
import Divider from '@mui/material/Divider'
import EditIcon from '@mui/icons-material/Edit'
import { grey } from '@mui/material/colors'
import { UpdateAccount } from './UpdateAccount'
import { DeleteAccount } from './DeleteAccount'
import {
    selectEmail,
    selectUsername,
    setHandleUpdateOpen,
    selectEditEmailOpen,
    selectEditUsernameOpen,
    selectEditPasswordOpen,
    setHandleEditEmailOpen,
    setHandleEditUsernameOpen,
    setHandleEditPasswordOpen,
} from '../accountSlice'
import { useAppDispatch, useAppSelector } from '../../../app/hooks'

export const ManageAccount = () => {
    const dispatch = useAppDispatch()
    const email = useAppSelector(selectEmail)
    const editEmailOpen = useAppSelector(selectEditEmailOpen)
    const username = useAppSelector(selectUsername)
    const editUsernameOpen = useAppSelector(selectEditUsernameOpen)
    const editPasswordOpen = useAppSelector(selectEditPasswordOpen)

    const handleEmailEdit = () => {
        dispatch(setHandleEditEmailOpen(true))
        dispatch(setHandleEditUsernameOpen(false))
        dispatch(setHandleEditPasswordOpen(false))
        dispatch(setHandleUpdateOpen(true))
    }

    const handleUsernameEdit = () => {
        dispatch(setHandleEditEmailOpen(false))
        dispatch(setHandleEditUsernameOpen(true))
        dispatch(setHandleEditPasswordOpen(false))
        dispatch(setHandleUpdateOpen(true))
    }

    const handlePasswordEdit = () => {
        dispatch(setHandleEditEmailOpen(false))
        dispatch(setHandleEditUsernameOpen(false))
        dispatch(setHandleEditPasswordOpen(true))
        dispatch(setHandleUpdateOpen(true))
    }

    // display any error not related to fields
    return (
        <Box align='center'>
            <Typography
                variant='h3'
                align='center'
                style={{ margin: '30px 0' }}
            >
                My account
            </Typography>
            <List
                sx={{
                    p: 0,
                    width: '100%',
                    maxWidth: 750,
                    borderRadius: 2,
                    border: '1px solid',
                    borderColor: 'divider',
                    backgroundColor: grey[300],
                }}
                aria-label='mailbox folders'
            >
                <ListItem>
                    <Box sx={{ flexGrow: 1 }}>
                        <Grid
                            container
                            spacing={5}
                            padding={2}
                            sx={{
                                rowGap: 1,
                            }}
                        >
                            <Grid item xs>
                                Email
                            </Grid>
                            <Grid item xs={8}>
                                {email}
                            </Grid>
                            <Grid item xs={1}>
                                <EditIcon
                                    sx={{ cursor: 'pointer' }}
                                    onClick={handleEmailEdit}
                                ></EditIcon>
                            </Grid>
                        </Grid>
                    </Box>
                </ListItem>
                <Divider component='li' />
                <ListItem>
                    <Box sx={{ flexGrow: 1 }}>
                        <Grid
                            container
                            spacing={5}
                            padding={2}
                            sx={{
                                rowGap: 1,
                            }}
                        >
                            <Grid item xs>
                                Username
                            </Grid>
                            <Grid item xs={8}>
                                {username}
                            </Grid>
                            <Grid item xs={1}>
                                <EditIcon
                                    sx={{ cursor: 'pointer' }}
                                    onClick={handleUsernameEdit}
                                ></EditIcon>
                            </Grid>
                        </Grid>
                    </Box>
                </ListItem>
                <Divider component='li' />
                <ListItem>
                    <Box sx={{ flexGrow: 1 }}>
                        <Grid
                            container
                            spacing={5}
                            padding={2}
                            sx={{
                                rowGap: 1,
                            }}
                        >
                            <Grid item xs>
                                Password
                            </Grid>
                            <Grid item xs={8}>
                                **********
                            </Grid>
                            <Grid item xs={1}>
                                <EditIcon
                                    sx={{ cursor: 'pointer' }}
                                    onClick={handlePasswordEdit}
                                ></EditIcon>
                            </Grid>
                        </Grid>
                    </Box>
                </ListItem>
            </List>
            <UpdateAccount
                editEmailOpen={editEmailOpen}
                editUsernameOpen={editUsernameOpen}
                editPasswordOpen={editPasswordOpen}
            ></UpdateAccount>
            <DeleteAccount></DeleteAccount>
        </Box>
    )
}
