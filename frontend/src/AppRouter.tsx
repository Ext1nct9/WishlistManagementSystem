import {
    BrowserRouter as Router,
    Routes,
    Route,
    Navigate,
} from 'react-router-dom'
import DefaultPage from './pages/DefaultPage'
import DevPage from './pages/DevPage'
import CreateAccount from './features/account/CreateAccount'

const AppRouter = () => {
    return (
        <Router>
            <Routes>
                <Route path='/' element={<DefaultPage />} />
                <Route path='/dev' element={<DevPage />} />
                <Route path ='/create_account' element={<CreateAccount />} />
                <Route path='*' element={<Navigate to='/' />} />
            </Routes>
        </Router>
    )
}

export default AppRouter
