import React from 'react'
import {Link} from 'react-router-dom'

const UserItem = ({user}) => {
    return (
        <tr>
            <td><Link to={`user/${user.id}`} >{user.first_name}</Link></td>
            <td>{user.last_name}</td>
            <td>{user.email}</td>
        </tr>
    )
} 


const UserList = ({users}) => {
    return (
        <table>
            <th>Имя</th>
            <th>Фамилия</th>
            <th>E-mail</th>
            {users.map((a) => <UserItem user={a} />)}
        </table>
    )
}

export default UserList
