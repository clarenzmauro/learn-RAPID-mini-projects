import React, { useState, useEffect } from 'react';
import './App.css';
// import QuestionDisplay from './QuestionDisplay';

// Define the base URL for your Django API
const API_URL = 'http://localhost:8000/api';

function App() {
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answerText, setAnswerText] = useState('');
  const [studentIdentifier, setStudentIdentifier] = useState('student001'); // Example
  const [message, setMessage] = useState(''); // For success/error messages
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch questions when the component mounts
  useEffect(() => {
    const fetchQuestions = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await fetch(`${API_URL}/questions/`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setQuestions(data);
        if (data.length === 0) {
          setMessage('No questions found.');
        }
      } catch (e) {
        console.error("Failed to fetch questions:", e);
        setError("Failed to load questions. Please try again later.");
        setMessage(''); // Clear any previous messages
      } finally {
        setIsLoading(false);
      }
    };

    fetchQuestions();
  }, []); // Empty dependency array means this effect runs once on mount

  const handleAnswerChange = (event) => {
    setAnswerText(event.target.value);
  };

  const handleStudentIdentifierChange = (event) => {
    setStudentIdentifier(event.target.value);
  };

  const handleSubmitAnswer = async (event) => {
    event.preventDefault(); // Prevent default form submission
    setMessage(''); // Clear previous messages
    setError(null);

    if (questions.length === 0 || !questions[currentQuestionIndex]) {
      setMessage('No question selected or available.');
      return;
    }

    const currentQuestion = questions[currentQuestionIndex];

    try {
      const response = await fetch(`${API_URL}/submit_answer/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Django's CSRF token would be handled here in a full setup
          // For now, we rely on @csrf_exempt in Django for easier testing
        },
        body: JSON.stringify({
          question_id: currentQuestion.id,
          student_identifier: studentIdentifier,
          answer_text: answerText,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error occurred' }));
        throw new Error(`HTTP error! status: ${response.status} - ${errorData.detail || errorData.error || 'Failed to submit'}`);
      }

      const result = await response.json();
      setMessage(`Answer submitted successfully! Submission ID: ${result.id}`);
      setAnswerText(''); // Clear the input field
      // Optionally, move to the next question or give feedback
    } catch (e) {
      console.error("Failed to submit answer:", e);
      setError(`Failed to submit answer: ${e.message}`);
    }
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setAnswerText(''); // Clear answer for new question
      setMessage('');
      setError(null);
    }
  };

  const handlePrevQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
      setAnswerText('');
      setMessage('');
      setError(null);
    }
  };


  if (isLoading) {
    return <div className="App"><p>Loading questions...</p></div>;
  }

  // We handle the error display more explicitly now
  // if (error) {
  //   return <div className="App"><p>Error loading questions: {error}</p></div>;
  // }

  const currentQuestion = questions.length > 0 ? questions[currentQuestionIndex] : null;

  return (
    <div className="App">
      <header className="App-header">
        <h1>Assessment Module</h1>
      </header>
      <main>
        {error && <p style={{ color: 'red' }}>Error: {error}</p>}
        {message && <p style={{ color: 'green' }}>{message}</p>}

        {questions.length === 0 && !isLoading && !error && (
          <p>No questions available at the moment.</p>
        )}

        {currentQuestion && (
          <div className="question-container" style={{ border: '1px solid #ccc', margin: '20px', padding: '20px' }}>
            <h2>Question {currentQuestionIndex + 1} of {questions.length}</h2>
            <p><strong>ID:</strong> {currentQuestion.id}</p>
            <p><strong>Type:</strong> {currentQuestion.question_type}</p>
            <p><strong>Difficulty:</strong> {currentQuestion.difficulty_level}</p>
            <p style={{ fontSize: '1.2em', fontWeight: 'bold' }}>{currentQuestion.question_text}</p>

            <form onSubmit={handleSubmitAnswer}>
              <div>
                <label htmlFor="studentId">Student Identifier: </label>
                <input
                  type="text"
                  id="studentId"
                  value={studentIdentifier}
                  onChange={handleStudentIdentifierChange}
                  required
                  style={{ margin: '10px 0', padding: '5px' }}
                />
              </div>
              <div>
                <label htmlFor="answer">Your Answer: </label>
                <textarea
                  id="answer"
                  value={answerText}
                  onChange={handleAnswerChange}
                  rows="4"
                  cols="50"
                  required
                  style={{ margin: '10px 0', padding: '5px' }}
                />
              </div>
              <button type="submit" style={{ padding: '10px 15px', marginTop: '10px' }}>Submit Answer</button>
            </form>
            <div className="navigation-buttons" style={{ marginTop: '20px' }}>
              <button onClick={handlePrevQuestion} disabled={currentQuestionIndex === 0} style={{ marginRight: '10px' }}>
                Previous Question
              </button>
              <button onClick={handleNextQuestion} disabled={currentQuestionIndex === questions.length - 1 || questions.length === 0}>
                Next Question
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;