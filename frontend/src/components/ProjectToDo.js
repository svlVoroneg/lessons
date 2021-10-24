import React from 'react';
import {useParams} from 'react-router-dom';
import ToDoForm from "./ToDoForm";

const ToDoItem = ({todo, deleteToDo}) => {
    return (
        <tr>
            <td>{todo.id}</td>
            <td>{todo.text_todo}</td>
            <td>{todo.created}</td>
            <td><button type='button' onClick={()=>deleteToDo(todo.id)}>Удалить</button></td>
        </tr>
    )
}

const ProjectToDoList = ({todos, users, deleteToDo, createToDo}) => {
    let { id } = useParams()
    let filtered_todos = todos.filter((todo) => todo.project === +id)

    return (
        <div>
            <h1>Список заметок проекта:</h1>
        <table>
            <th>Id</th>
            <th>текст ссылки</th>
            <th>создана</th>
            <th>Действия</th>
            {filtered_todos.map((b) => <ToDoItem todo={b} deleteToDo={deleteToDo}/>)}
        </table>
        <ToDoForm createToDo={createToDo} project={id} users={users}/>
        </div>
    )
}

export default ProjectToDoList
