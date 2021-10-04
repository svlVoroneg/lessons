import React from 'react'
import {Link} from 'react-router-dom'

const ProjectItem = ({project}) => {
    return (
        <tr>
            <td><Link to={`project/${project.id}`} >{project.name}</Link></td>
            <td>{project.repo}</td>
            <td>{project.id}</td>
        </tr>
    )
}


const ProjectList = ({projects}) => {
    return (
        <table>
            <th>Имя проекта</th>
            <th>Ссылка на репозиторий</th>
            <th>id</th>
            {projects.map((c) => <ProjectItem project={c} />)}
        </table>
    )
}

export default ProjectList
