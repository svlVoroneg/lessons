import React from 'react'
import {useParams} from 'react-router-dom'

const ToDoItem1 = ({todo}) => {
    return (
        <tr>
            <td>{todo.id}</td>
            <td>{todo.text_todo}</td>
            <td>{todo.created}</td>
            <td>{todo.user}</td>
        </tr>
    )
}


const UserToDoList = ({todos}) => {
    let { id } = useParams()
    let filtered_todos = todos.filter((todo) => todo.user === parseInt(id))

    return (
        <table>
            <th>Имя</th>
            <th>Фамилия</th>
            <th>E-mail</th>
            {filtered_todos.map((td) => <ToDoItem1 todo={td} />)}
        </table>
    )
}

export default UserToDoList
