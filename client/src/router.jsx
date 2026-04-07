import { createBrowserRouter } from 'react-router-dom'
import AuthPage from "./pages/AuthPage"
import HomePage from "./pages/HomePage"
import App from "./App"
import { getAllTasks, userConfirmation } from './utilities'

const router = createBrowserRouter([
    {
        path:"/",
        element: <App/>,
        loader: userConfirmation,
        children:[
            {
                index:true,
                element:<AuthPage/>
            },
            {
                path:"home",
                element: <HomePage />,
                loader: getAllTasks
            }
        ]
    }
])

export default router