import React from 'react';
import SignEvaluator from './components/SignEvaluator';

function App() {
  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>Smart SLSL Learner Platform</h1>
      <SignEvaluator currentSignId="S01_amma" />
    </div>
  );
}

export default App;