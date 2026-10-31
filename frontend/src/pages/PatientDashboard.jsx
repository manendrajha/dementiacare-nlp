import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Heart, Home, MessageCircle, Clock, BookHeart, Puzzle, Send,
  ArrowLeft, Sun, CheckCircle2, Sparkles, Plus, Copy, Check
} from 'lucide-react';

import '../App.css';
import {
  sendChatMessage,
  getMemories,
  getReminders,
  generateLinkingCode
} from '../services/api';

const initialMessages = [
  { role: 'assistant', text: "Hello! It's lovely to see you today. How are you feeling?" }
];

const dailyWords = [
  { word: 'Garden', meaning: 'A place where flowers, plants and trees grow.', example: 'We enjoy walking through the garden.' },
  { word: 'Gentle', meaning: 'Kind, soft and calm.', example: 'A gentle breeze came through the window.' },
  { word: 'Journey', meaning: 'A trip from one place to another.', example: 'Our journey to the hills was wonderful.' },
  { word: 'Harvest', meaning: 'The time when crops are gathered.', example: 'Farmers gather the harvest in autumn.' },
  { word: 'Lantern', meaning: 'A light inside a protective case.', example: 'A lantern lit the path.' },
  { word: 'Melody', meaning: 'A pleasant sequence of musical notes.', example: 'She hummed a familiar melody.' },
  { word: 'Meadow', meaning: 'A field of grass and wild flowers.', example: 'The children played in the meadow.' }
];

const quizQuestions = [
  { question: 'Which of these is a fruit?', options: ['Carrot', 'Apple', 'Potato'], answer: 'Apple', explanation: 'An apple is a fruit.' },
  { question: 'How many days are there in a week?', options: ['Five', 'Seven', 'Ten'], answer: 'Seven', explanation: 'There are seven days in a week.' },
  { question: 'Which season is usually the coldest?', options: ['Winter', 'Summer', 'Spring'], answer: 'Winter', explanation: 'Winter is generally the coldest season.' },
  { question: 'What do bees make?', options: ['Milk', 'Honey', 'Bread'], answer: 'Honey', explanation: 'Bees make honey.' },
  { question: 'Which one tells time?', options: ['Clock', 'Plate', 'Pillow'], answer: 'Clock', explanation: 'A clock tells us the time.' }
];

function formatTime(value) {
  if (!value) return '';
  const [hours, minutes] = value.split(':').map(Number);
  if (Number.isNaN(hours) || Number.isNaN(minutes)) return value;
  const period = hours >= 12 ? 'PM' : 'AM';
  return `${hours % 12 || 12}:${String(minutes).padStart(2, '0')} ${period}`;
}

function PatientDashboard() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('home');
  const [messages, setMessages] = useState(initialMessages);
  const [message, setMessage] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [memories, setMemories] = useState([]);
  const [reminders, setReminders] = useState([]);
  const [completed, setCompleted] = useState([]);
  const [dataLoading, setDataLoading] = useState(true);
  const [dataError, setDataError] = useState('');
  const [linkCode, setLinkCode] = useState('');
  const [linkCodeLoading, setLinkCodeLoading] = useState(false);
  const [linkCodeError, setLinkCodeError] = useState('');
  const [copied, setCopied] = useState(false);
  const [quizIndex, setQuizIndex] = useState(0);
  const [quizScore, setQuizScore] = useState(0);
  const [quizAnswer, setQuizAnswer] = useState('');
  const [quizFinished, setQuizFinished] = useState(false);

  useEffect(() => {
    let active = true;
    const loadPatientData = async () => {
      setDataLoading(true);
      setDataError('');
      const [memoryResult, reminderResult] = await Promise.allSettled([
        getMemories(), getReminders()
      ]);
      if (!active) return;
      if (memoryResult.status === 'fulfilled') setMemories(memoryResult.value);
      else setDataError('We could not load your memories. Please try refreshing the page.');
      if (reminderResult.status === 'fulfilled') {
        setReminders(reminderResult.value);
      } else {
        setDataError(previous => previous ? `${previous} Reminders could not be loaded.` : 'We could not load your reminders. Please try refreshing the page.');
      }
      setDataLoading(false);
    };
    loadPatientData();
    return () => { active = false; };
  }, []);

  const today = new Date().toLocaleDateString('en-IN', {
    weekday: 'long', day: 'numeric', month: 'long'
  });
  const wordOfDay = dailyWords[Math.floor(Date.now() / 86400000) % dailyWords.length];

  const sendMessage = async (text = message) => {
    const trimmed = text.trim();
    if (!trimmed || isSending) return;
    setMessages(previous => [...previous, { role: 'user', text: trimmed }]);
    setMessage('');
    setIsSending(true);
    try {
      const result = await sendChatMessage(trimmed);
      setMessages(previous => [...previous, {
        role: 'assistant',
        text: result.response || "I'm here with you. Would you like to tell me a little more?"
      }]);
    } catch (error) {
      console.error('Chat request failed:', error);
      setMessages(previous => [...previous, {
        role: 'assistant',
        text: "I'm sorry, I'm having trouble responding right now. Please try again in a moment."
      }]);
    } finally {
      setIsSending(false);
    }
  };

  const createLinkCode = async () => {
    try {
      setLinkCodeLoading(true);
      setLinkCodeError('');
      const result = await generateLinkingCode();
      setLinkCode(result.code || result.linking_code || '');
      if (!result.code && !result.linking_code) {
        setLinkCodeError('The server did not return a linking code.');
      }
    } catch (error) {
      setLinkCodeError(error.response?.data?.detail || 'Could not generate a code. Please try again.');
    } finally {
      setLinkCodeLoading(false);
    }
  };

  const copyLinkCode = async () => {
    try {
      await navigator.clipboard.writeText(linkCode);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
    } catch {
      setLinkCodeError('Copy was unavailable. Please select and copy the code manually.');
    }
  };

  const toggleReminder = (id) => {
    setCompleted(previous => previous.includes(id)
      ? previous.filter(item => item !== id)
      : [...previous, id]);
  };

  const answerQuiz = (answer) => {
    if (quizAnswer) return;
    setQuizAnswer(answer);
    if (answer === quizQuestions[quizIndex].answer) setQuizScore(previous => previous + 1);
  };

  const nextQuestion = () => {
    if (quizIndex === quizQuestions.length - 1) {
      setQuizFinished(true);
    } else {
      setQuizIndex(previous => previous + 1);
      setQuizAnswer('');
    }
  };

  const restartQuiz = () => {
    setQuizIndex(0);
    setQuizScore(0);
    setQuizAnswer('');
    setQuizFinished(false);
  };

  const renderChat = () => (
    <section className="patient-chat-card">
      <div className="chat-heading">
        <div className="chat-avatar"><Heart size={25} /></div>
        <div><h2>Your AI companion</h2><p>Here whenever you need a friend.</p></div>
        <span className="online-indicator"><span />{isSending ? 'Thinking' : 'Ready'}</span>
      </div>
      <div className="chat-messages" aria-live="polite" aria-busy={isSending}>
        {messages.map((item, index) => (
          <div key={index} className={`chat-message ${item.role}`}>{item.text}</div>
        ))}
        {isSending && <div className="chat-message assistant" role="status">Just a moment, I'm thinking...</div>}
      </div>
      <div className="quick-prompts">
        <p>Not sure what to say? Try one of these:</p>
        <div className="prompt-buttons">
          <button disabled={isSending} onClick={() => sendMessage('Tell me something nice.')}>Tell me something nice</button>
          <button disabled={isSending} onClick={() => sendMessage('I want to talk about my day.')}>Let's talk about my day</button>
          <button disabled={isSending} onClick={() => sendMessage('Help me remember something.')}>Help me remember</button>
        </div>
      </div>
      <form className="chat-input-area" onSubmit={event => { event.preventDefault(); sendMessage(); }}>
        <input value={message} onChange={event => setMessage(event.target.value)} placeholder="Type something here..." aria-label="Your message" disabled={isSending} />
        <button type="submit" aria-label="Send message" disabled={isSending || !message.trim()}><Send size={21} /><span>Send</span></button>
      </form>
      <p className="chat-disclaimer"><Sparkles size={15} /> A friendly space to talk, share and connect.</p>
    </section>
  );

  const renderHome = () => (
    <div className="patient-home-grid">
      <section className="patient-panel">
        <div className="panel-heading"><div className="panel-icon reminder-icon"><Clock size={22} /></div><div><h2>Today's reminders</h2><p>Your daily activities</p></div></div>
        <div className="reminder-list">
          {dataLoading ? <p>Loading your reminders...</p> : reminders.length ? reminders.map(item => (
            <div className="reminder-item" key={item.id}>
              <button className={`reminder-check ${completed.includes(item.id) ? 'checked' : ''}`} onClick={() => toggleReminder(item.id)} aria-label={`Mark ${item.title} as ${completed.includes(item.id) ? 'incomplete' : 'complete'}`}>
                {completed.includes(item.id) && <CheckCircle2 size={22} />}
              </button>
              <div className="reminder-content"><span>{formatTime(item.time)}</span><h3 className={completed.includes(item.id) ? 'completed-text' : ''}>{item.title}</h3><p>{item.description}</p></div>
            </div>
          )) : <p>No reminders have been added yet.</p>}
        </div>
        <p className="patient-small-note">Completion marks are temporary and reset when you reload this page.</p>
      </section>

      <section className="patient-panel memory-panel">
        <div className="panel-heading"><div className="panel-icon memory-icon"><BookHeart size={22} /></div><div><h2>My memories</h2><p>Little things that matter</p></div></div>
        {dataLoading ? <p>Loading your memories...</p> : memories.length ? memories.slice(0, 3).map(memory => <div className="patient-memory-item" key={memory.id}><strong>{memory.title}</strong><p>{memory.description}</p></div>) : <p>Your caregiver can add familiar people, places and special moments.</p>}
        <button className="care-link-button" onClick={() => setActiveTab('memories')}>See all memories →</button>
      </section>

      <section className="patient-panel">
        <div className="panel-heading"><div className="panel-icon activity-icon"><Sun size={22} /></div><div><h2>Word of the day</h2><p>A small moment of learning</p></div></div>
        <span className="memory-category">TODAY'S WORD</span><h2>{wordOfDay.word}</h2><p>{wordOfDay.meaning}</p><p><em>{wordOfDay.example}</em></p>
        <button className="care-link-button" onClick={() => setActiveTab('word')}>Explore word →</button>
      </section>

      <section className="patient-panel activities-panel">
        <div className="panel-heading"><div className="panel-icon activity-icon"><Puzzle size={22} /></div><div><h2>A little quiz</h2><p>A gentle brain exercise</p></div></div>
        <p>Try five simple questions at your own pace.</p>
        <button className="care-primary-button" onClick={() => { restartQuiz(); setActiveTab('quiz'); }}>Start quiz</button>
      </section>

      <section className="patient-panel patient-link-panel">
        <div className="panel-heading"><div className="panel-icon memory-icon"><Heart size={22} /></div><div><h2>Connect with your caregiver</h2><p>Share access to your care information</p></div></div>
        <p>Generate a one-time code and share it with your caregiver. The code expires in 15 minutes.</p>
        <button className="care-primary-button" onClick={createLinkCode} disabled={linkCodeLoading}>{linkCodeLoading ? 'Generating...' : 'Generate linking code'}</button>
        {linkCode && <div className="patient-link-code"><strong>{linkCode}</strong><button type="button" onClick={copyLinkCode} aria-label="Copy linking code">{copied ? <Check size={18} /> : <Copy size={18} />}{copied ? 'Copied' : 'Copy'}</button></div>}
        {linkCodeError && <p className="care-api-error" role="alert">{linkCodeError}</p>}
      </section>
    </div>
  );

  const renderMemories = () => (
    <section className="patient-panel patient-memory-page">
      <div className="panel-heading"><div className="panel-icon memory-icon"><BookHeart size={22} /></div><div><h2>My memories</h2><p>Familiar people, places and special moments</p></div></div>
      {dataLoading ? <p>Loading memories...</p> : memories.length ? memories.map(memory => <article className="patient-memory-item" key={memory.id}><strong>{memory.title}</strong><p>{memory.description}</p><span className="memory-category">{memory.category || 'Memory'}</span></article>) : <p>Your caregiver has not added any memories yet.</p>}
    </section>
  );

  const renderWord = () => (
    <section className="patient-panel patient-word-page">
      <div className="panel-heading"><div className="panel-icon activity-icon"><Sun size={22} /></div><div><h2>Word of the day</h2><p>Take your time and enjoy a new word</p></div></div>
      <span className="memory-category">TODAY'S WORD</span><h1>{wordOfDay.word}</h1><h3>Meaning</h3><p>{wordOfDay.meaning}</p><h3>Example</h3><p><em>{wordOfDay.example}</em></p>
    </section>
  );

  const renderQuiz = () => {
    if (quizFinished) return <section className="patient-panel patient-quiz-page"><Puzzle size={30} /><h2>Quiz completed!</h2><p>You answered {quizScore} out of {quizQuestions.length} questions correctly.</p><button className="care-primary-button" onClick={restartQuiz}>Try again</button></section>;
    const current = quizQuestions[quizIndex];
    return (
      <section className="patient-panel patient-quiz-page">
        <div className="panel-heading"><div className="panel-icon activity-icon"><Puzzle size={22} /></div><div><h2>A little quiz</h2><p>Question {quizIndex + 1} of {quizQuestions.length}</p></div></div>
        <div className="quiz-progress"><div style={{ width: `${((quizIndex + 1) / quizQuestions.length) * 100}%` }} /></div>
        <h2>{current.question}</h2>
        <div className="quiz-options">
          {current.options.map(option => <button key={option} className={`quiz-option ${quizAnswer && option === current.answer ? 'correct' : ''} ${quizAnswer === option && option !== current.answer ? 'incorrect' : ''}`} disabled={Boolean(quizAnswer)} onClick={() => answerQuiz(option)}>{option}</button>)}
        </div>
        {quizAnswer && <div className="quiz-feedback"><p>{quizAnswer === current.answer ? 'Well done!' : 'Good try!'}</p><span>{current.explanation}</span><button className="care-primary-button" onClick={nextQuestion}>{quizIndex === quizQuestions.length - 1 ? 'See result' : 'Next question'}</button></div>}
      </section>
    );
  };

  const tabs = [
    { id: 'home', label: 'Home', icon: Home },
    { id: 'chat', label: 'My companion', icon: MessageCircle },
    { id: 'memories', label: 'Memories', icon: BookHeart },
    { id: 'word', label: 'Word of the day', icon: Sun },
    { id: 'quiz', label: 'Quiz', icon: Puzzle }
  ];

  return (
    <div className="patient-interface">
      <header className="patient-header">
        <div className="patient-brand"><div className="patient-brand-icon"><Heart size={23} /></div><span>DementiaCare</span></div>
        <button className="patient-exit-button" onClick={() => navigate('/')}><ArrowLeft size={19} />Back to home</button>
      </header>

      <main className="patient-main">
        <section className="patient-welcome">
          <div><div className="patient-date"><Sun size={19} /><span>{today}</span></div><h1>Good afternoon! 👋</h1><p>It's lovely to see you today. What would you like to do?</p></div>
          <div className="welcome-decoration"><Heart size={34} /><span>Every day matters.</span></div>
        </section>

        <nav className="patient-tabs" aria-label="Patient navigation">
          {tabs.map(tab => { const Icon = tab.icon; return <button key={tab.id} className={activeTab === tab.id ? 'active' : ''} onClick={() => setActiveTab(tab.id)}><Icon size={20} />{tab.label}</button>; })}
        </nav>

        {dataError && <p role="alert" className="patient-data-error">{dataError}</p>}
        {activeTab === 'home' && renderHome()}
        {activeTab === 'chat' && renderChat()}
        {activeTab === 'memories' && renderMemories()}
        {activeTab === 'word' && renderWord()}
        {activeTab === 'quiz' && renderQuiz()}

        <footer className="patient-footer">Made with care, patience and connection.</footer>
      </main>
    </div>
  );
}

export default PatientDashboard;
