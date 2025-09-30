import React, { useState } from 'react';
import axios from 'axios';
import { processLyricsWithGemini } from '../api/lyricProcessor';
import './LyricRhymer.css';

const LyricRhymer = () => {
  const [inputText, setInputText] = useState('');
  const [highlightedHtml, setHighlightedHtml] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const processLyrics = async () => {
    if (!inputText.trim()) {
      setError('Please enter some lyrics to process');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      // Call the Python backend API
      const highlightedHtml = await processLyricsWithGemini(inputText);
      setHighlightedHtml(highlightedHtml);
    } catch (err) {
      setError('Failed to process lyrics. Please try again.');
      console.error('Error processing lyrics:', err);
    } finally {
      setIsLoading(false);
    }
  };


  const clearAll = () => {
    setInputText('');
    setHighlightedHtml('');
    setError('');
  };

  return (
    <div className="lyric-rhymer">
      <div className="input-section">
        <h2>Enter Your Rap Lyrics</h2>
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Paste your rap lyrics here..."
          className="lyrics-input"
          rows={12}
        />
        <div className="button-group">
          <button 
            onClick={processLyrics} 
            disabled={isLoading || !inputText.trim()}
            className="process-btn"
          >
            {isLoading ? 'Processing...' : 'Highlight Rhymes'}
          </button>
          <button onClick={clearAll} className="clear-btn">
            Clear All
          </button>
        </div>
        {error && <div className="error-message">{error}</div>}
      </div>

      <div className="output-section">
        <h2>Highlighted Rhymes</h2>
        <div className="output-container">
          {highlightedHtml ? (
            <div 
              className="highlighted-lyrics"
              dangerouslySetInnerHTML={{ __html: highlightedHtml }}
            />
          ) : (
            <div className="placeholder">
              <p>Your highlighted lyrics will appear here</p>
              <p>Rhyming words will be colored to show patterns</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LyricRhymer;
