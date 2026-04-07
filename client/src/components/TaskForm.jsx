import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/esm/Button';
import { createTask } from '../utilities';

function TaskForm({addTask}) {
    const [taskTitle, setTaskTitle] = useState('')
    // TODO(human): add dueDate state here
    const [dueDate, setDueDate] = useState('')

    const handleSubmit = async(e) => {
        e.preventDefault()
        // TODO(human): pass dueDate to createTask and reset it after submission
        let newTask = await createTask( taskTitle, dueDate ) // {id, title, due_date, user} | null
        if (newTask){
            addTask(newTask)
        }
        setTaskTitle('')
        setDueDate('')
    }

    return (
        <>
            <Form onSubmit={handleSubmit} style={{width:"100%", display:"flex", justifyContent:"space-around"}}>
                <Form.Control
                    type="text"
                    placeholder='input a new task title here'
                    value={taskTitle}
                    onChange={(e)=>setTaskTitle(e.target.value)}
                />
                <Form.Control
                    type="date"
                    placeholder='input a due date here'
                    value={dueDate}
                    onChange={(e)=>setDueDate(e.target.value)}
                />
                <Button type='submit'>
                    Create
                </Button>
            </Form>
        </>
    );
}

export default TaskForm;