import React from 'https://esm.sh/react@18?dev';
import htm from 'https://esm.sh/htm?dev';

const html = htm.bind(React.createElement);

export default function AuthForm({ mode, values, onChange, onSubmit, loading }) {
  return html`
    <form className="form" onSubmit=${onSubmit}>
      ${mode === 'register'
        ? html`
            <label>
              Name
              <input
                type="text"
                value=${values.name}
                onChange=${(event) => onChange({ ...values, name: event.target.value })}
                required
              />
            </label>
          `
        : null}

      <label>
        Email
        <input
          type="email"
          value=${values.email}
          onChange=${(event) => onChange({ ...values, email: event.target.value })}
          required
        />
      </label>
      <label>
        Password
        <input
          type="password"
          value=${values.password}
          onChange=${(event) => onChange({ ...values, password: event.target.value })}
          required
        />
      </label>
      <button type="submit" disabled=${loading}>
        ${loading ? (mode === 'login' ? 'Logging in…' : 'Registering…') : mode === 'login' ? 'Login' : 'Register'}
      </button>
    </form>
  `;
}
