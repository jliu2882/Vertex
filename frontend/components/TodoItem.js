import React from 'https://esm.sh/react@18?dev';
import htm from 'https://esm.sh/htm?dev';

const html = htm.bind(React.createElement);

export default function TodoItem({ todo, onToggle, onDelete }) {
  return html`
    <li className="todo-item">
      <header>
        <strong>${todo.title}</strong>
        <span style=${{ color: todo.completed ? '#166534' : '#334155' }}>
          ${todo.completed ? 'Completed' : 'Pending'}
        </span>
      </header>
      <p>${todo.description || 'No description provided.'}</p>
      <footer>
        <button type="button" onClick=${() => onToggle(todo)}>
          ${todo.completed ? 'Mark Incomplete' : 'Mark Complete'}
        </button>
        <button type="button" className="secondary" onClick=${() => onDelete(todo.id)}>
          Delete
        </button>
      </footer>
    </li>
  `;
}
