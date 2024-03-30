import React, {useState} from "react"
import { useNavigate } from "react-router-dom"
import {useForm, Controller} from "react-hook-form"
import * as yup from "yup"
import {yupResolver} from "@hookform/resolvers/yup"
import { useAppDispatch, useAppSelector } from '../../app/hooks'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import { createAccount } from './accountSlice'
import ButtonAppBar from '../misc/topBar'
import Grid from '@mui/material/Grid'
import Link from '@mui/material/Link'
import Container from '@mui/material/Container'
import { CssBaseline} from "@mui/material"
import Typography from '@mui/material/Typography'
import styles from './CreateAccount.module.css'
import FormControl from "@mui/material"



export default function CreateAccount(){
    const dispatch = useAppDispatch();
    const navigate = useNavigate();
    const validationSchema = yup.object().shape({
        email: yup.string().required('Email is required').email('Email is invalid'),
        username: yup.string().required('Username is required'),
        password: yup.string().trim().required('Password is required').min(10, 'Password must be at least 10 characters').matches(/\d/, 'Password must contain at least one digit'),
        cpassword: yup.string().trim().required('Confirmation Password is required').oneOf([yup.ref('password'), null], 'Passwords must match')
    });
    const { register, handleSubmit, formState: { errors }, control } = useForm({
        mode: "onBlur",
        resolver: yupResolver(validationSchema)
    });

    async function onSubmit(data) {
        console.log(data);
        try{
            await dispatch(createAccount(data));
            navigate('/login');
        }
        catch(error){
            console.error('Failed to create account', error);
        }
    }

    const [showPassword, setShowPassword] = useState(false);

    const handle = () => {
        setShowPassword(!showPassword);
    }

    return (
        <Box>
            <ButtonAppBar />
            <CssBaseline />
            <Container maxWidth="xs" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '90vh', padding: 0 }}>
            <Typography component="h1" variant="h5" style = {{marginBottom: 30, fontSize: 32}}>
                Create an Account
            </Typography>
            <form className ={styles.form} onSubmit={handleSubmit(onSubmit)}>
                <Grid container spacing={2}>
                <Grid item xs={12}>
                    <Controller
                        control={control}
                        name = "email"
                        defaultValue = ""
                        render={({ field }) => (
                            <TextField
                            {...field}
                            label="Email Address"
                            name="email"
                            variant="outlined"
                            fullWidth
                            autoComplete="email"
                            error={!!errors.email}
                            helperText={errors.email?.message}
                            />
                        )}
                    />
                </Grid>
                <Grid item xs={12}>
                    <Controller
                        control={control}
                        render={({ field }) => (
                            <TextField
                            {...field}
                            label="Username"
                            name="username"
                            variant="outlined"
                            fullWidth
                            autoComplete="username"
                            error={!!errors.username}
                            helperText={errors.username?.message}
                            />
                        )}
                        name="username"
                        defaultValue = ""
                    />
                </Grid>
                <Grid item xs={12}>
                    <Controller
                        control={control}
                        name = "password"
                        defaultValue = ""
                        render={({ field }) => (
                            <TextField
                            {...field}
                            type = {showPassword ? 'text' : 'password'}
                            label="Password"
                            name="password"
                            variant="outlined"
                            fullWidth
                            autoComplete="password"
                            error={!!errors.password}
                            helperText={errors.password?.message}
                            />
                        )}
                    />
                </Grid>
                <Grid item xs={12}>
                    <Controller
                        control={control}
                        defaultValue = ""
                        render={({ field }) => (
                            <TextField
                            {...field}
                            type = {showPassword ? 'text' : 'password'}
                            label="Confirmation password"
                            name="cpassword"
                            variant="outlined"
                            fullWidth
                            autoComplete="cpassword"
                            error={!!errors.cpassword}
                            helperText={errors.cpassword?.message}
                            />
                        )}
                        name="cpassword"
                    />
                </Grid>
                <Grid item xs={12}>
                    <Button 
                    type="submit"
                    fullWidth
                    variant="contained"
                    color="primary"
                    className = {styles.submit}
                    >
                    Create Account
                    </Button>
                </Grid>
                </Grid>
                <Grid container justifyContent="center">
                <Grid item >
                    <Link href="/login" variant="body2">
                    Already have an account? Sign in
                    </Link>
                </Grid>
                </Grid>
            </form>
            </Container>
        </Box>
    )
}

export { CreateAccount as AccountCreation };