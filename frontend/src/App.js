import React from 'react'
import {Route, Link, Switch, Redirect, BrowserRouter} from 'react-router-dom'
import axios from 'axios'
import UserList from './components/Users.js';
import ProjectList from './components/Projects.js';
import ProjectToDoList from './components/ProjectToDo.js';
import UserToDoList from './components/UserToDo.js';
import ToDoList from "./components/ToDo.js";
import LoginForm from "./components/LoginForm.js";
import ProjectForm from "./components/ProjectForm.js"

const NotFound = ({location}) => {
    return (<div>Страница не найдена: {location.pathname}</div>)
}

class App extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            'users': [],
            'projects': [],
            'todos': [],
            'token': '',
            'userlogin': '',
            'user': []
        }
    }

    getToken(login, password) {
        this.setState({'userlogin': login })
        axios.post('http://127.0.0.1:8000/api-token-auth/', {"username": login, "password": password})
        .then(response => {
            localStorage.setItem('token', response.data.token)
            localStorage.setItem('userlogin', login)
            this.setState({'token': response.data.token}, this.loadData)
        })
        .catch(error => {
            console.log(error)
            alert("Wrong password")
        })
    }

    logout() {
        localStorage.setItem('token', '')
        localStorage.setItem('userlogin', '')
        this.setState({'userlogin': ''})
        this.setState({'token': ''}, this.loadData)
    }

    isAuthenticated() {
        return !!this.state.token
    }

    getHeaders() {
        if (this.isAuthenticated()) { return {'Authorization': 'Token ' + this.state.token} }
        return {}
    }

    createProject(name, repo, users) {
        const headers = this.getHeaders()
        axios.post('http://127.0.0.1:8000/api/projects/',
            {'name': name, 'repo': repo, 'users': users} ,
            {headers})
        .then(response => {
            this.loadData();
        }).catch(error => {console.log(error)})
    }

    updateProject(id, name, repo, users) {
        const headers = this.getHeaders()
        axios.put(`http://127.0.0.1:8000/api/projects/${id}/`,
            {'name': name, 'repo': repo, 'users': users} ,
            {headers})
        .then(response => {
            this.loadData();
        }).catch(error => {console.log(error)})
    }

    deleteProject(id) {
        const headers = this.getHeaders()
        axios.delete(`http://127.0.0.1:8000/api/projects/${id}/`, {headers})
        .then(response => {
            this.loadData();
        }).catch(error => {console.log(error)})
    }

    createToDo(project, text_todo, user) {
        const headers = this.getHeaders()
        console.log(text_todo)
        console.log(user)
        axios.post('http://127.0.0.1:8000/api/todos/',
            {'project': project, 'text_todo': text_todo, 'user': user} ,
            {headers})
        .then(response => {
            this.loadData();
        }).catch(error => {console.log(error)})
    }

    deleteToDo(id) {
        const headers = this.getHeaders()
        axios.delete(`http://127.0.0.1:8000/api/todos/${id}/`, {headers})
        .then(response => {
            this.setState( {
                'todos': this.state.todos.filter((todo) => todo.id !== id)
            })
        }).catch(error => {console.log(error)})
    }

    loadData() {
        const headers = this.getHeaders()
        axios.get('http://127.0.0.1:8000/api/users/', {headers})
        .then(response => {
            const users = response.data
            const user = users.filter((st) => st.email === this.state.userlogin)
            this.setState( {'users': users })
            this.setState({'user': user[0] })
        })
        .catch(error => {
            console.log(error)
            this.setState({
                'users': []
            })
        })
        axios.get('http://127.0.0.1:8000/graphql/?query={allProjects{id name repo}}')
        .then(response => {
            const projects = response.data.data.allProjects
            this.setState( {
                'projects': projects
            })
        })
        .catch(error => {
            console.log(error)
            this.setState({
                'projects': []
            })
        })
        axios.get('http://127.0.0.1:8000/api/todos/', {headers})
        .then(response => {
            const todos = response.data
            this.setState( {
                'todos': todos
            })
        })
        .catch(error => {
            console.log(error)
            this.setState({
                'todos': []
            })
        })
    }

    componentDidMount() {
        const token = localStorage.getItem('token')
        const userlogin = localStorage.getItem('userlogin')
        console.log(token)
        console.log(userlogin)
        this.setState({'userlogin': userlogin})
        this.setState({'token': token}, this.loadData)
    }

    render() {
        return (
            <div>
                <div>
                   { this.isAuthenticated() ?
                       <div>
                           <button onClick={()=>this.logout()}>Выйти</button>
                           <div>Пользователь: {this.state.user['first_name']}</div>
                       </div> :
                        <LoginForm getToken={(login, password) => this.getToken(login, password)} />
                   }
                </div>
                <BrowserRouter>
                    <nav>
                       <ul> Меню
                           <li><Link to='/users'>Список пользователей</Link></li>
                           <li><Link to='/projects'>Список проектов</Link></li>
                           <li><Link to='/projects/create'>Создать проект</Link></li>
                           <li><Link to='/todos'>Список заметок</Link></li>
                         </ul>
                    </nav>
                    <Switch>
                        <Route path='/' exact component={() => <UserList users = {this.state.users}/>} />
                        <Route path='/projects' exact component={
                            () => <ProjectList projects = {this.state.projects}
                                               deleteProject={(id) => this.deleteProject(id)}/>} />
                        <Route path='/projects/create' exact component={
                            () => <ProjectForm users = {this.state.users} createProject={
                                (name, repo, users) => this.createProject(name, repo, users)}/>} />
                        <Route path='/todos' exact component={() => <ToDoList todos = {this.state.todos}/>} />
                        <Route path='/user/:id' component={() => <UserToDoList todos = {this.state.todos}/>} />
                        <Route path='/project/:id' component={
                            () => <ProjectToDoList todos = {this.state.todos}
                                                   users = {this.state.users}
                                                   deleteToDo={(id) => this.deleteToDo(id)}
                                                   createToDo={(project, text_todo, user) => this.createToDo(project, text_todo, user)}
                            />} />
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
