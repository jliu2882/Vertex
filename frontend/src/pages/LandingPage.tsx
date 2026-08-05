import React from 'react';
import { useNavigate } from 'react-router-dom';

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="page-shell">
      <div className="auth-card">
        <span className="page-badge">Task flow</span>
        <h1 className="page-title">Stay on top of your day!</h1>
        <p className="page-subtitle">
          Organize your ideas, set priorities, and keep your plans moving forward.
        </p>

        <div className="auth-form">
          <button
            onClick={() => navigate('/login')}
            className="auth-button"
          >
            Login
          </button>
          <button
            onClick={() => navigate('/register')}
            className="auth-button"
            style={{ background: 'linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)' }}
          >
            Create an account
          </button>
        </div>
      </div>
    </div>
  );
};
