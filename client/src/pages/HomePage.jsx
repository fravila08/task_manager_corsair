import { useState } from "react";
import { useLoaderData, useOutletContext } from "react-router-dom";
import Stack from 'react-bootstrap/Stack';
import TaskDisplay from "../components/TaskDisplay";
import TaskForm from "../components/TaskForm";
import { logoutUser } from "../utilities";

const HomePage = () => {
    const {user, setUser} = useOutletContext()
    const [tasks, setTasks] = useState(useLoaderData())

    const addTask = (task) => {
        setTasks([...tasks, task])
    }

    const rmTask = (rmTask) => {
        setTasks(tasks.filter((task)=>(
            task.id !== rmTask.id
        )))
    }

    const updateTask = (editTask) => {
        setTasks(tasks.map((task)=>(
            task.id === editTask.id ? editTask : task
        )))
    }

    return (
        <>
            <h1>Welcome {user && user}: Here are your Tasks <button onClick={async()=>setUser(await logoutUser())}>Log Out</button></h1>

            <Stack gap={3}>
                <TaskForm addTask={addTask}/>

                {tasks.map((task)=>(
                    <TaskDisplay 
                        key={task.id} 
                        task={task}
                        rmTask={rmTask}
                        updateTask={updateTask}
                    />
                ))}

            </Stack>
        </>
    )
}

export default HomePage;