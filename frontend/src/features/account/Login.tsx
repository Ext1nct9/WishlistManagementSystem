import { useAppDispatch, useAppSelector } from '../../app/hooks'
import { useNavigate } from 'react-router-dom'
import * as yup from 'yup'
import { yupResolver } from '@hookform/resolvers/yup'
import { Controller, useForm } from 'react-hook-form'
import { useState } from 'react'
import { Box, Button, Grid, Link, TextField } from '@mui/material'
import Container from '@mui/material/Container'
import Typography from '@mui/material/Typography'
import styles from './CreateAccount.module.css'
import {
    login,
    logout,
    fetchAccountInfo,
    type AccountSliceState,
} from './accountSlice'

export default function Login() {
    const dispatch = useAppDispatch()
    const navigate = useNavigate()
    const validationSchema = yup.object().shape({
        email: yup
            .string()
            .required('Email is required')
            .email('Email is invalid'),
        password: yup.string().trim().required('Password is required'),
    })
    const {
        handleSubmit,
        formState: { errors },
        control,
    } = useForm({
        mode: 'onBlur',
        resolver: yupResolver(validationSchema),
    })
    async function onSubmit(data) {
        console.log(data)
        try {
            let action = await dispatch(login(data))
            if (action.error) {
                throw action.error
            }
            window.alert('Login successful')
            let action2 = await dispatch(fetchAccountInfo({}))
            console.log(action2)
            if (action2.error) {
                throw action2.error
            }
            navigate('/')
        } catch (error) {
            window.alert(`${error.message}`)
            console.error(error)
        }
    }

    async function handleLogout() {
        try {
            let action = await dispatch(logout())
            if (action.error) {
                throw action.error
            }
            // Clear account information from local storage
            window.alert('Logout successful')
            navigate('/')
        } catch (error) {
            window.alert(`${error.message}`)
            console.error(error)
        }
    }
    const [showPassword, setShowPassword] = useState(false)

    if (
        useAppSelector(
            (state: { account: AccountSliceState }) =>
                state.account.userAccountId
        )
    ) {
        return (
            <Container
                maxWidth='xs'
                style={{
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    alignItems: 'center',
                    height: '90vh',
                    padding: 0,
                }}
            >
                <Typography
                    component='h1'
                    variant='h5'
                    style={{ marginBottom: 30, fontSize: 32 }}
                >
                    You are already logged in.
                </Typography>
                <Button
                    fullWidth
                    variant='contained'
                    color='primary'
                    onClick={handleLogout}
                >
                    Logout
                </Button>
            </Container>
        )
    } else {
        return (
            <Container
                maxWidth='xs'
                style={{
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    alignItems: 'center',
                    height: '90vh',
                    padding: 0,
                }}
            >
                <Typography
                    component='h1'
                    variant='h5'
                    style={{ marginBottom: 30, fontSize: 32 }}
                >
                    Login
                </Typography>
                <Box
                    component='form'
                    className={styles.form}
                    onSubmit={handleSubmit(onSubmit)}
                >
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <Controller
                                control={control}
                                name='email'
                                defaultValue=''
                                render={({ field }) => (
                                    <TextField
                                        {...field}
                                        label='Email'
                                        variant='outlined'
                                        fullWidth
                                        error={!!errors.email}
                                        helperText={errors.email?.message}
                                        autoComplete='email'
                                    />
                                )}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <Controller
                                control={control}
                                name='password'
                                defaultValue=''
                                render={({ field }) => (
                                    <TextField
                                        {...field}
                                        type={
                                            showPassword ? 'text' : 'password'
                                        }
                                        label='Password'
                                        variant='outlined'
                                        fullWidth
                                        autoComplete='password'
                                        error={!!errors.password}
                                        helperText={errors.password?.message}
                                    />
                                )}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <Button
                                type='submit'
                                fullWidth
                                variant='contained'
                                color='primary'
                                className={styles.submit}
                            >
                                Login
                            </Button>
                        </Grid>
                    </Grid>
                    <Grid container justifyContent='center'>
                        <Grid item>
                            <Link href='/create_account' variant='body2'>
                                Don't have an account? Sign up
                            </Link>
                        </Grid>
                    </Grid>
                </Box>
            </Container>
        )
    }
}

export { Login }
