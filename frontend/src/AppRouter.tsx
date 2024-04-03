import {
    BrowserRouter as Router,
    Routes,
    Route,
    Navigate,
} from 'react-router-dom'
import HomePage from './pages/HomePage'
import DevPage from './pages/DevPage'
import Wishlist from './pages/WishlistPage'
import { AccountCreation } from './features/account/CreateAccount'
import { ManageAccount } from './features/account/manage_account/ManageAccount'
import { Login } from './features/account/Login'
import ForbiddenErrorPage from './pages/ForbiddenPage'
import NotFoundErrorPage from './pages/NotFoundPage'
import DefaultErrorPage from './pages/DefaultErrorPage'
import { AccountMenu } from './features/account/manage_account/AccountMenu'

const AppRouter = () => {
    return (
        <Router>
            <Routes>
                <Route path='/' element={<HomePage />} />
                <Route path='/dev' element={<DevPage />} />
                <Route path='/create_account' element={<AccountCreation />} />
                <Route path='/login' element={<Login />} />
                <Route path='/manage_account' element={<ManageAccount />} />
                <Route path='*' element={<Navigate to='/' />} />
                <Route path='/wishlist/:wishlist_id' element={<Wishlist />} />
                <Route path='/account_menu' element={<AccountMenu />} />
                <Route path='/error/403' element={<ForbiddenErrorPage />} />
                <Route path='/error/404' element={<NotFoundErrorPage />} />
                <Route path='/error/default' element={<DefaultErrorPage />} />
            </Routes>
        </Router>
    )
}

export default AppRouter
