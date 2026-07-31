import React from 'https://esm.sh/react@18?dev';
import htm from 'https://esm.sh/htm?dev';
import AuthForm from './components/AuthForm.js';
import TodoCreateForm from './components/TodoCreateForm.js';
import TodoList from './components/TodoList.js';
import { getStoredToken, saveToken, login, registerUser, fetchTodos, createTodo, updateTodo, deleteTodo } from './api.js';

const html = htm.bind(React.createElement);

function App() {
  const [authToken, setAuthToken] = React.useState(getStoredToken());
  const [mode, setMode] = React.useState('login');
  const [todos, setTodos] = React.useState([]);
  const [message, setMessage] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [loginValues, setLoginValues] = React.useState({ email: '', password: '' });
  const [registerValues, setRegisterValues] = React.useState({ name: '', email: '', password: '' });
  const [todoValues, setTodoValues] = React.useState({ title: '', description: '' });

  React.useEffect(() => {
    if (authToken) {
      saveToken(authToken);
      loadTodos();
    } else {
      saveToken('');
      setTodos([]);
    }
  }, [authToken]);

  const notify = (text, type = 'success') => {
    setMessage({ text, type });
    window.clearTimeout(window.todoMessageTimeout);
    window.todoMessageTimeout = window.setTimeout(() => setMessage(null), 4000);
  };

  const handleUnauthorized = () => {
    setAuthToken('');
    notify('Session expired. Please log in again.', 'error');
  };

  const loadTodos = async () => {
    if (!authToken) return;

    setLoading(true);
    try {
      const data = await fetchTodos(authToken);
      setTodos(data || []);
    } catch (error) {
      if (error.status === 401) {
        handleUnauthorized();
      } else {
        notify(error.message || 'Unable to load todos.', 'error');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      const data = await login(loginValues);
      setAuthToken(data.access_token);
      notify('Logged in successfully.');
    } catch (error) {
      notify(error.message || 'Login failed.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      await registerUser(registerValues);
      notify('Registration successful. Please log in.');
      setMode('login');
    } catch (error) {
      notify(error.message || 'Registration failed.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTodo = async (event) => {
    event.preventDefault();
    if (!authToken) {
      notify('Please log in to create a todo.', 'error');
      return;
    }

    setLoading(true);
    try {
      await createTodo(authToken, todoValues);
      setTodoValues({ title: '', description: '' });
      notify('Todo created successfully.');
      await loadTodos();
    } catch (error) {
      if (error.status === 401) {
        handleUnauthorized();
      } else {
        notify(error.message || 'Unable to create todo.', 'error');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleToggleTodo = async (todo) => {
    if (!authToken) {
      notify('Please log in to update todos.', 'error');
      return;
    }

    setLoading(true);
    try {
      await updateTodo(authToken, todo.id, { completed: !todo.completed });
      notify('Todo updated successfully.');
      await loadTodos();
    } catch (error) {
      if (error.status === 401) {
        handleUnauthorized();
      } else {
        notify(error.message || 'Unable to update todo.', 'error');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTodo = async (todoId) => {
    if (!authToken) {
      notify('Please log in to delete todos.', 'error');
      return;
    }

    setLoading(true);
    try {
      await deleteTodo(authToken, todoId);
      notify('Todo deleted successfully.');
      await loadTodos();
    } catch (error) {
      notify(error.message || 'Unable to delete todo.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setAuthToken('');
    setTodos([]);
    notify('Logged out.');
  };

  const messageClass = message ? `message ${message.type}` : 'message';
  const loginTabClass = mode === 'login' ? 'tab active' : 'tab';
  const registerTabClass = mode === 'register' ? 'tab active' : 'tab';

  return html`
    <div className="app-shell">
      <header className="card">
        <div>
          <h1>Todo List</h1>
          <p>${authToken ? 'Authenticated' : 'Please log in or register'}</p>
        </div>
        ${authToken
          ? html`<button type="button" className="secondary" onClick=${handleLogout}>Logout</button>`
          : null}
      </header>

      ${message ? html`<div className=${messageClass}>${message.text}</div>` : null}

      <section className="card">
        <div className="form-tabs">
          <button type="button" className=${loginTabClass} onClick=${() => setMode('login')}>
            Login
          </button>
          <button type="button" className=${registerTabClass} onClick=${() => setMode('register')}>
            Register
          </button>
        </div>

        <${AuthForm}
          mode=${mode}
          values=${mode === 'login' ? loginValues : registerValues}
          onChange=${mode === 'login' ? setLoginValues : setRegisterValues}
          onSubmit=${mode === 'login' ? handleLogin : handleRegister}
          loading=${loading}
        />
      </section>

      ${authToken
        ? html`
            <section className="card">
              <h2>My Todos</h2>
              <${TodoCreateForm} values=${todoValues} onChange=${setTodoValues} onSubmit=${handleCreateTodo} loading=${loading} />
              <${TodoList} todos=${todos} loading=${loading} onToggle=${handleToggleTodo} onDelete=${handleDeleteTodo} />
            </section>
          `
        : null}
    </div>
  `;
}

export default App;
