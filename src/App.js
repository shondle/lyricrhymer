import React from 'react';
import LyricRhymer from './components/LyricRhymer';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>🎤 LyricRhymer</h1>
        <p>Highlight rhyming parts in your rap lyrics with AI</p>
      </header>
      <main>
        <LyricRhymer />
      </main>
    </div>
  );
}

export default App;
