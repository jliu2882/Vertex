import React from 'https://esm.sh/react@18?dev';
import htm from 'https://esm.sh/htm?dev';

const html = htm.bind(React.createElement);

export default function TodoCreateForm({ values, onChange, onSubmit, loading }) {
  return html`
    <form className="form" onSubmit=${onSubmit}>
      <label>
        Title
        <input
          type="text"
          value=${values.title}
          onChange=${(event) => onChange({ ...values, title: event.target.value })}
          required
        />
      </label>
      <label>
        Description
        <input
          type="text"
          value=${values.description}
          onChange=${(event) => onChange({ ...values, description: event.target.value })}
        />
      </label>
      <button type="submit" disabled=${loading}>
        ${loading ? 'Saving…' : 'Create Todo'}
      </button>
    </form>
  `;
}
