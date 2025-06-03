import './App.css';
import QuestionDisplay from './QuestionDisplay';

function App() {
  const sampleQuestions = [
    {
      id: 1,
      question_text: "What is the primary function of a CPU?",
      question_type: "Short Answer",
      difficulty_level: 2
    },
    {
      id: 2,
      question_text: "Select all prime numbers: 2, 4, 5, 7, 9",
      question_type: "Multiple Choice",
      difficulty_level: 1
    },
    {
      id: 3,
      question_text: "Describe the process of mitosis.",
      question_type: "Essay",
      difficulty_level: 3
    }
  ];

  return (
    <div className="App">
      <header className="App-header">
        <h1>Assessment Module Questions</h1>
      </header>
      <main>
        {sampleQuestions.map(q => (
          <QuestionDisplay
            key={q.id} // Important: key prop for lists
            question_text={q.question_text}
            question_type={q.question_type}
            difficulty_level={q.difficulty_level}
          />
        ))}
      </main>
    </div>
  );
}

export default App;
