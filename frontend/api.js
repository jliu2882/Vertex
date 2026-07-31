const backendOrigin = '';
const tokenStorageKey = 'todo_api_token';

export function getStoredToken() {
  return localStorage.getItem(tokenStorageKey) || '';
}

export function saveToken(token) {
  if (token) {
    localStorage.setItem(tokenStorageKey, token);
  } else {
    localStorage.removeItem(tokenStorageKey);
  }
}

async function request(path, { token = '', method = 'GET', body = null } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${backendOrigin}${path}`, {
    method,
    headers,
    body,
  });

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    const message = payload?.detail || response.statusText || 'API request failed';
    const error = new Error(message);
    error.status = response.status;
    throw error;
  }

  return payload;
}

export async function login(credentials) {
  return request('/accounts/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  });
}

export async function registerUser(payload) {
  return request('/accounts/register', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function fetchTodos(token) {
  return request('/todos', { token, method: 'GET' });
}

export async function createTodo(token, payload) {
  return request('/todos', {
    token,
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function updateTodo(token, todoId, payload) {
  return request(`/todos/${todoId}`, {
    token,
    method: 'PUT',
    body: JSON.stringify(payload),
  });
}

export async function deleteTodo(token, todoId) {
  return request(`/todos/${todoId}`, {
    token,
    method: 'DELETE',
  });
}
