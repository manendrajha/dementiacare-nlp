
import { useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import {
  Heart,
  Mail,
  Lock,
  UserRound,
  Users,
  ArrowRight
} from 'lucide-react';

import { useAuth } from '../context/AuthContext';
import './Auth.css';

function Register() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { register } = useAuth();

  const initialRole = searchParams.get('role') === 'caregiver'
    ? 'caregiver'
    : 'patient';

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState(initialRole);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');

    if (password.length < 8) {
      setError('Password must contain at least 8 characters.');
      return;
    }

    setSubmitting(true);

    try {
      const user = await register(
        name.trim(),
        email.trim(),
        password,
        role
      );

      navigate(
        user.role === 'patient' ? '/patient' : '/caregiver',
        { replace: true }
      );
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Unable to create your account. Please try again.'
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

      <section className="auth-content register-content">
        <div className="auth-heading">
          <span className="auth-eyebrow">
            CARE · CONNECTION · COMFORT
          </span>

          <h1>Let's get started.</h1>

          <p>
            Create an account to begin your DementiaCare journey.
          </p>
        </div>

        <div className="auth-card">
          <form onSubmit={handleSubmit}>
            <div className="auth-field">
              <label htmlFor="name">Full name</label>

              <div className="auth-input-wrap">
                <UserRound size={18} />
                <input
                  id="name"
                  type="text"
                  placeholder="Enter your name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  autoComplete="name"
                  minLength={2}
                  maxLength={100}
                  required
                />
              </div>
            </div>

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
                  placeholder="Create a password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete="new-password"
                  minLength={8}
                  maxLength={128}
                  required
                />
              </div>

              <span className="auth-field-hint">
                Use at least 8 characters.
              </span>
            </div>

            <div className="auth-field">
              <label>I am registering as</label>

              <div className="auth-role-options">
                <button
                  type="button"
                  className={`auth-role-option ${
                    role === 'patient' ? 'selected' : ''
                  }`}
                  onClick={() => setRole('patient')}
                  aria-pressed={role === 'patient'}
                >
                  <UserRound size={21} />
                  <span>Patient</span>
                </button>

                <button
                  type="button"
                  className={`auth-role-option ${
                    role === 'caregiver' ? 'selected' : ''
                  }`}
                  onClick={() => setRole('caregiver')}
                  aria-pressed={role === 'caregiver'}
                >
                  <Users size={21} />
                  <span>Caregiver</span>
                </button>
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
              {submitting ? 'Creating account...' : 'Create account'}
              {!submitting && <ArrowRight size={19} />}
            </button>
          </form>

          <div className="auth-switch">
            Already have an account?{' '}
            <Link to={`/login?role=${role}`}>
              Sign in
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

export default Register;
