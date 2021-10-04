import React from 'react'
import {useParams} from 'react-router-dom'

const ToDoItem = ({todo}) => {
    return (
        <tr>
            <td>{todo.id}</td>
            <td>{todo.text_todo}</td>
            <td>{todo.created}</td>
            <td>{todo.project}</td>
        </tr>
    )
}


const ProjectToDoList = ({todos}) => {
    let { id } = useParams()
    let filtered_todos = todos.filter((todo) => todo.project === +id)

    return (
        <table>
            <th>Имя проекта</th>
            <th>Ссылка на репозиторий</th>
            {filtered_todos.map((b) => <ToDoItem todo={b} />)}
        </table>
    )
}

export default ProjectToDoList
