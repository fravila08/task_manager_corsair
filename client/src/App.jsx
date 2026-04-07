import { useEffect, useState } from 'react'
import { Outlet, useLoaderData, useNavigate, useLocation } from 'react-router-dom'
import './App.css'

function App() {
  const [user, setUser] = useState(useLoaderData())
  const navigate = useNavigate()
  const location = useLocation()

  useEffect(()=>{
    console.log(user)
  }, [user])

  useEffect(()=>{
    if (user && location.pathname === '/'){
      navigate('/home')
    } else if ( !user && location.pathname !== '/'){
      navigate('/')
    }
  }, [user, location.pathname])


  return (
    <>
     <Outlet context={{ user, setUser }}/>
    </>
  )
}

export default App