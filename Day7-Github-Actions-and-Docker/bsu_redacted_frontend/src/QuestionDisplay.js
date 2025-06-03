import React from 'react';

function QuestionDisplay(props) {
  // Destructure props for easier access
  const { question_text, question_type, difficulty_level } = props;

  return (
    <div style={{ border: '1px solid #ccc', margin: '10px', padding: '10px', borderRadius: '5px' }}>
      <h3>Question:</h3>
      <p>{question_text}</p>
      <p><strong>Type:</strong> {question_type}</p>
      <p><strong>Difficulty:</strong> {difficulty_level}</p>
    </div>
  );
}

export default QuestionDisplay;