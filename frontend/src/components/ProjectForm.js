import React from 'react'
import {withRouter} from 'react-router-dom'

class ProjectForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            'name': '',
            'repo': '',
            'users': []
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
        this.props.createProject(this.state.name, this.state.repo, this.state.users)
        event.preventDefault()
        this.props.history.push('/projects')
    }

    render() {
        return (
            <form onSubmit={(event) => this.handleSubmit(event)}>
                <input type="text" name="name" placeholder="Наименование проекта" value={this.state.name} onChange = {(event) => this.handleChange(event)} />
                <input type="text" name="repo" placeholder="Ссылка на репозиторий" value={this.state.repo} onChange = {(event) => this.handleChange(event)} />
                <select multiple name="users" onChange = {(event) => this.handleUserChange(event)}>
                    {this.props.users.map((user) => <option value={user.id}>{user.first_name} {user.last_name} </option>)}
                </select>
                <input type="submit" value="Создать проект" />
            </form>
        )
    }
}

export default withRouter(ProjectForm)
