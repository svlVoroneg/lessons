import React from 'react'
import {useParams, withRouter} from 'react-router-dom'

class ProjectForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            'id':  1,
            'project': this.props.projects.filter((project) => project.id === this.state.id),
            'users': this.state.project.users
        }
    }

    handleChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        })
    }

    handleUserChange(event) {
        if (!event.target.selectedOptions) {
            return;
        }
        let users = []
        for(let i = 0; i < event.target.selectedOptions.length; i++) {
            users.push(parseInt(event.target.selectedOptions.item(i).value))
        }
        this.setState({
            ['users']: users
        })
    }

    handleSubmit(event) {
        console.log(this.state.name, this.state.repo, this.state.users)
        this.props.updateProject(this.state.id, this.state.project.name, this.project.state.repo, this.state.users)
        event.preventDefault()
        this.props.history.push('/projects')
    }

    render() {
        return (
            <form onSubmit={(event) => this.handleSubmit(event)}>
                <input type="text" name="name" value={this.state.project.name} onChange = {(event) => this.handleChange(event)} />
                <input type="text" name="repo" value={this.state.project.repo} onChange = {(event) => this.handleChange(event)} />
                <select multiple name="users" onChange = {(event) => this.handleUserChange(event)}>
                    {this.props.users.map((user) => <option value={user.id}>{user.first_name} {user.last_name} </option>)}
                </select>
                <input type="submit" value="Обновить проект" />
            </form>
        )
    }
}

export default withRouter(ProjectForm)
