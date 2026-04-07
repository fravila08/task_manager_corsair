import Stack from 'react-bootstrap/Stack';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { useState } from 'react';
import { deleteATask, putTask } from '../utilities';

const TaskDisplay = ({task, rmTask, updateTask}) => {

    const [edit, setEdit] = useState(false)
    const [editTitle, setEditTitle] = useState(task.title)
    const [editDueDate, setEditDueDate] = useState(task.due_date)

    const editTaskHandle = async () => {
        let editedTask = await putTask(task.id, editTitle, editDueDate)
        if (editedTask){
            updateTask(editedTask)
        }
        setEdit(!edit)
    }

    const handleRemove = async() => {
        let taskDelete = await deleteATask(task.id) // str | null
        if (taskDelete){
            rmTask(task)
        }
    }

    return (
        <>
            <Stack direction="horizontal" gap={3} style={{border:"solid black 1vmin"}}>
            {edit ?
            <>
                <Form.Control 
                    className="p-2" 
                    placeholder={task.title}
                    value={editTitle}
                    onChange={(e)=>setEditTitle(e.target.value)}
                />
                <Form.Control 
                    className="p-2" 
                    type="date"
                    placeholder={task.due_date}
                    value={editDueDate}
                    onChange={(e)=>setEditDueDate(e.target.value)}
                />
                <Button variant="outline-primary" onClick={editTaskHandle}>Submit</Button>
                <div className="vr" />
                <Button variant="outline-secondary" onClick={()=>[setEdit(!edit), setEditTitle(task.title)]}>Cancel</Button>
            </>
            :
            <>
                <div className="p-2">{task.title}</div>
                <div className="p-2">{task.due_date}</div>
                <div className="p-2 ms-auto">
                    <Button variant='warning' onClick={()=>setEdit(!edit)}>
                        Edit
                    </Button>
                </div>
                <div className="vr" />
                <div className="p-2">
                    <Button variant='danger' onClick={handleRemove}>
                        Delete
                    </Button>
                </div>
            </>
        }
        </Stack>
        </>
    )
}

export default TaskDisplay