
import { useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { Heart, Mail, Lock, ArrowRight, UserRound, Users } from 'lucide-react';

import { useAuth } from '../context/AuthContext';
import './Auth.css';

function Login() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { login } = useAuth();

  const selectedRole = searchParams.get('role') || 'patient';

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setSubmitting(true);

    try {
      const user = await login(email.trim(), password);

      navigate(
        user.role === 'patient' ? '/patient' : '/caregiver',
        { replace: true }
      );
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Unable to sign in. Please check your details.'
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="auth-page">
      <nav className="auth-nav">
        <Link to="/" className="auth-brand">
          <span className="auth-brand-icon">
            <Heart size={21} />
          </span>
          <span>DementiaCare</span>
        </Link>

        <Link to="/" className="auth-back-link">
          Back to home
        </Link>
      </nav>

      <section className="auth-content">
        <div className="auth-heading">
          <span className="auth-eyebrow">
            CARE · CONNECTION · COMFORT
          </span>

          <h1>Welcome back.</h1>

          <p>
            A familiar space, whenever you need it.
          </p>
        </div>

        <div className="auth-card">
          <div className="auth-role-indicator">
            <span className="auth-role-icon">
              {selectedRole === 'caregiver'
                ? <Users size={21} />
                : <UserRound size={21} />
              }
            </span>

            <div>
              <strong>
                {selectedRole === 'caregiver'
                  ? 'Caregiver sign in'
                  : 'Patient sign in'
                }
              </strong>
              <span>Sign in to continue to your account</span>
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="auth-field">
              <label htmlFor="email">Email address</label>

              <div className="auth-input-wrap">
                <Mail size={18} />
                <input
                  id="email"
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  autoComplete="email"
                  required
                />
              </div>
            </div>

            <div className="auth-field">
              <label htmlFor="password">Password</label>

              <div className="auth-input-wrap">
                <Lock size={18} />
                <input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete="current-password"
                  required
                />
              </div>
            </div>

            {error && (
              <div className="auth-error" role="alert">
                {error}
              </div>
            )}

            <button
              type="submit"
              className="auth-submit"
              disabled={submitting}
            >
              {submitting ? 'Signing in...' : 'Sign in'}
              {!submitting && <ArrowRight size={19} />}
            </button>
          </form>

          <div className="auth-switch">
            Don't have an account?{' '}
            <Link to={`/register?role=${selectedRole}`}>
              Create one
            </Link>
          </div>
        </div>

        <p className="auth-footer-note">
          Built around care, patience and connection.
        </p>
      </section>
    </main>
  );
}

export default Login;
