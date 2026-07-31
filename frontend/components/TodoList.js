import React from 'https://esm.sh/react@18?dev';
import htm from 'https://esm.sh/htm?dev';
import TodoItem from './TodoItem.js';

const html = htm.bind(React.createElement);

export default function TodoList({ todos, loading, onToggle, onDelete }) {
  return html`
    <ul className="todo-list">
      ${todos.length
        ? todos.map((todo) => html`<${TodoItem} key=${todo.id} todo=${todo} onToggle=${onToggle} onDelete=${onDelete} />`)
        : html`
            <li className="todo-item">
              <p>${loading ? 'Loading todos…' : 'No todos yet. Add one above.'}</p>
            </li>
          `}
    </ul>
  `;
}
