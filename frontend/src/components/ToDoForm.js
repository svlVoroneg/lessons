import React from 'react'

class ToDoForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            'text_todo': '',
            'user': props.users[0].pk
        }
    }

    handleChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        })
    }

    handleSubmit(event) {
        console.log(this.props.project, this.state.text_todo, this.state.user)
        this.props.createToDo(this.props.project, this.state.text_todo, this.state.user)
        event.preventDefault()
    }

    render() {
        return (
            <form onSubmit={(event) => this.handleSubmit(event)}>
                <input type="text" name="text_todo" placeholder="Текст заметки" value={this.state.repo} onChange = {(event) => this.handleChange(event)} />
                <select name="user" className='form-control' onChange = {(event) => this.handleChange(event)}>
                    {this.props.users.map((item) => <option value={item.pk}>{item.first_name} {item.last_name} </option>)}
                </select>
                <input type="submit" value="Создать заметку" />
            </form>
        )
    }
}

export default ToDoForm
