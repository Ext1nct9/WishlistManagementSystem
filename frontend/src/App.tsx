import { CssBaseline } from '@mui/material'
import AppRouter from './AppRouter'
import TopBar from './features/misc/TopBar'

import './App.css'

const App = () => {
    return (
        <>
            <TopBar />
            <CssBaseline />
            <AppRouter />
        </>
    )
}

export default App
