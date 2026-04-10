import axios from "axios";

export const api = axios.create({
    baseURL: 'https://deployment-demo.com/api/v1/',
    withCredentials: true,
})

const refreshAccessToken = async() => {
    return axios.post(
        'https://deployment-demo.com/api/v1/users/refresh/',
        {},
        { withCredentials:true }
    )
}
// use(func1:true, func2:false)
api.interceptors.response.use( // creation of interceptor
    // success
    (response) => response,

    // failure
    async (error) => {
        const originalRequest = error.config
        console.log(originalRequest)
        if (error.response?.status === 401 && !originalRequest._retry){
            originalRequest._retry = true

            try{
                await refreshAccessToken()
                return api(originalRequest)
            } catch (refreshError) {
                return Promise.reject(refreshError)
            }
        }
        return Promise.reject(error)
    }
)

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
    try{
        let response = await api.get("tasks/")
        if (response.status === 200){
            return response.data // [{task},{task},{task}]
        }
    }    catch(error){
        console.error(error)
        return []
    }
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
        return null
    }
    alert("Something went wrong")
    return null
}

export const userConfirmation = async() => {
    try{
        let response = await api.get('users/')
        if (response.status === 200){
            let user = response.data.email
            console.log("SUCCESS")
            return user
        } 
        console.error(response.data)
        return null
    } catch(error){
        console.error(error)
        return null
    }
}

export const handleUserAuth = async( data, create ) => {
    try{
        let response = await api.post(`users/${create ? 'create' : 'login'}/`,
            data
        )
        // response status of 201 | 200| 400 |404
        if (response.status === 201 || response.status === 200){
            return response.data.email
        }
        else{
            console.error(response.data)
            return null
        }
    }
    catch(error){
        console.error(error)
        return null
    }
}