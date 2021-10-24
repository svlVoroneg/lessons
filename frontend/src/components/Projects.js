import React from 'react'
import {Link} from 'react-router-dom'

const ProjectItem = ({project, deleteProject}) => {
    return (
        <tr>
            <td><Link to={`project/${project.id}`} >{project.name}</Link></td>
            <td>{project.repo}</td>
            <td>{project.id}</td>
            <td>
                <button type='button' onClick={()=>deleteProject(project.id)}>Удалить</button>
            </td>
        </tr>
    )
}


const ProjectList = ({projects, deleteProject}) => {
    return (
        <table>
            <th>Имя проекта</th>
            <th>Ссылка на репозиторий</th>
            <th>id</th>
            <th>Действия</th>
            {projects.map((c) => <ProjectItem project={c} deleteProject={deleteProject}/>)}
        </table>
    )
}

export default ProjectList
