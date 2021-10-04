import React from 'react'
import {Route, Link, Switch, Redirect, BrowserRouter} from 'react-router-dom'
import axios from 'axios'
import UserList from './components/Users.js';
import ProjectList from './components/Projects.js';
import ProjectToDoList from './components/ProjectToDo.js';
import UserToDoList from './components/UserToDo.js';
import ToDoList from "./components/ToDo.js";

const NotFound = ({location}) => {
    return (<div>Страница не найдена: {location.pathname}</div>)
}

class App extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            'users': [],
            'projects': [],
            'todos': []
        }
    }

    componentDidMount() {
        axios.get('http://127.0.0.1:8000/api/users/')
        .then(response => {
            const users = response.data
            this.setState( {
                'users': users
            })
        })
        axios.get('http://127.0.0.1:8000/api/projects/')
        .then(response => {
            const projects = response.data
            this.setState( {
                'projects': projects
            })
        })
        axios.get('http://127.0.0.1:8000/api/todos/')
        .then(response => {
            const todos = response.data
            this.setState( {
                'todos': todos
            })
        })
        .catch(error => console.log(error))
    }

    render() {
        return (
            <div>
                <BrowserRouter>
                    <nav>
                       <ul> Меню
                            <li><Link to='/users'>Список пользователей</Link></li>
                            <li><Link to='/projects'>Список проектов</Link></li>
                            <li><Link to='/todos'>Список заметок</Link></li>
                        </ul>
                    </nav>
                    <Switch>
                        <Route path='/' exact component={() => <UserList users = {this.state.users}/>} />
                        <Route path='/user/:id' component={() => <UserToDoList todos = {this.state.todos}/>} />
                        <Route path='/project/:id' component={() => <ProjectToDoList todos = {this.state.todos}/>} />
                        <Route path='/projects' exact component={() => <ProjectList projects = {this.state.projects}/>} />
                        <Route path='/todos' exact component={() => <ToDoList todos = {this.state.todos}/>} />
                        <Redirect from='/users' to='/' />
                        <Route component={NotFound} />
                    </Switch>
                </BrowserRouter>
                <footer><p>Copyright Вячеслав Семенов</p></footer>
            </div>
        )
    }
}

export default App;
