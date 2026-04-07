import axios from "axios";

export const api = axios.create({
    baseURL: 'http://3.138.247.77/api/v1/'
})

export const deleteATask = async( id ) => {
    let response = await api.delete(`tasks/${id}/`)
    if(response.status === 200){
        return response.data // str success
    }
    return null
}

export const putTask = async( id, title, dueDate ) => {
    let response = await api.put(`tasks/${id}/`,
        {'title':title, 'due_date': dueDate || null}
    )
    if (response.status === 200){
        return response.data // {task}
    }
    console.error(response.data)
    return null
}

export const getAllTasks = async() => {
    let response = await api.get("tasks/")
    if (response.status === 200){
        return response.data // [{task},{task},{task}]
    }
    console.error(response.data)
    return []
}

export const createTask = async( title, dueDate ) => {
    let response =  await api.post('tasks/',
        {'title':title, 'due_date': dueDate || null}
    )
    if (response.status === 201){
        return response.data
    }
    else{
        console.error(response.data)
        return null
    }
}

export const logoutUser = async() => {
    let response = await api.post('users/logout/')
    if (response.status === 200){
        localStorage.removeItem('token')
        delete api.defaults.headers.common['Authorization']
        return null
    }
    alert("Something went wrong")
    return null
}

export const userConfirmation = async() => {
    let token = localStorage.getItem("token") // 'str' | null
    if (token){
        api.defaults.headers.common['Authorization'] = `Token ${token}`
        let response = await api.get('users/')
        if (response.status === 200){
            let user = response.data.email
            console.log("SUCCESS")
            return user
        }
        console.error(response.data)
        return null
    }
    return null
}

export const handleUserAuth = async( data, create ) => {
    // url pattern users/create|login/
    // body of request must hold {email,password}
    let response = await api.post(`users/${create ? 'create' : 'login'}/`,
        data
    )
    // response status of 201 | 200| 400 |404
    if (response.status === 201 || response.status === 200){
        let token = response.data.token
        api.defaults.headers.common['Authorization'] = `Token ${token}`
        localStorage.setItem("token", token)
        return response.data.email
    }
    // response data = {token, email} | {errors}
    else{
        console.error(response.data)
        return null
    }
}