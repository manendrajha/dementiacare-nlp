
import { useNavigate } from 'react-router-dom';
import { Heart, ArrowRight, Users, UserRound } from 'lucide-react';
import '../App.css';

function Home() {
  const navigate = useNavigate();

  return (
    <main className="home-page">
      <nav className="home-nav">
        <div className="brand">
          <div className="brand-icon">
            <Heart size={21} />
          </div>
          <span>DementiaCare</span>
        </div>

        <span className="nav-caption">
          A little support, every day.
        </span>
      </nav>

      <section className="hero-section">
        <div className="hero-content">
          <span className="eyebrow">CARE · CONNECTION · COMFORT</span>

          <h1>
            Making every day
            <br />
            a little <span>easier.</span>
          </h1>

          <p>
            A supportive space for everyday conversations,
            familiar memories and meaningful connections.
          </p>
        </div>

        <div className="role-section">
          <h2>Welcome! How would you like to continue?</h2>

          <div className="role-grid">
            <button
              className="role-card patient-card"
              onClick={() => navigate('/login?role=patient')}
            >
              <div className="role-icon">
                <UserRound size={28} />
              </div>

              <div>
                <h3>I'm a patient</h3>
                <p>
                  Chat, explore activities and revisit
                  familiar memories.
                </p>
              </div>

              <ArrowRight className="role-arrow" size={21} />
            </button>

            <button
              className="role-card caregiver-card"
              onClick={() => navigate('/login?role=caregiver')}
            >
              <div className="role-icon">
                <Users size={28} />
              </div>

              <div>
                <h3>I'm a caregiver</h3>
                <p>
                  Manage reminders, memories and
                  patient interactions.
                </p>
              </div>

              <ArrowRight className="role-arrow" size={21} />
            </button>
          </div>
        </div>
      </section>

      <footer className="home-footer">
        Built around care, patience and connection.
      </footer>
    </main>
  );
}

export default Home;
