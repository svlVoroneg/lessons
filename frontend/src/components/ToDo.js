import React from 'react'


const ToDoItem = ({todo}) => {
    return (
        <tr>
            <td>{todo.id}</td>
            <td>{todo.text_todo}</td>
            <td>{todo.created}</td>
            <td>{todo.user}</td>
            <td>{todo.project}</td>
        </tr>
    )
}


const ToDoList = ({todos}) => {
    return (
        <table>
            <tr>
                <th>id</th>
                <th>Заметка</th>
                <th>Создана</th>
                <th>Пользователь</th>
                <th>Проект</th>
            </tr>
            <tbody>
            {todos.map((c) => <ToDoItem todo={c} />)}
            </tbody>
        </table>
    )
}

export default ToDoList
