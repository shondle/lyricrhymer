import axios from 'axios';

// This file handles the API integration with your Python backend
// You'll need to modify the URL to match your Python server

const API_BASE_URL = 'http://localhost:8000'; // Adjust this to your Python server URL

export const processLyricsWithGemini = async (lyrics) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/process`, {
      lyrics: lyrics
    }, {
      timeout: 30000, // 30 second timeout
      headers: {
        'Content-Type': 'application/json',
      }
    });
    return response.data.highlighted_html;
  } catch (error) {
    console.error('Error calling Python backend:', error);
    
    // If backend is not available, use fallback simulation
    if (error.code === 'ERR_NETWORK' || error.message.includes('Network Error')) {
      console.log('Backend not available, using fallback rhyme detection');
      return simulateRhymeDetection(lyrics);
    }
    
    throw new Error('Failed to process lyrics with AI');
  }
};

// Fallback rhyme detection when backend is not available
const simulateRhymeDetection = (text) => {
  const words = text.split(' ');
  const rhymeGroups = {};
  let groupCounter = 1;
  
  const highlightedWords = words.map((word) => {
    const cleanWord = word.toLowerCase().replace(/[^\w]/g, '');
    if (cleanWord.length < 3) return word;
    
    // Simple rhyme detection based on ending sounds
    const ending = cleanWord.slice(-3);
    
    if (!rhymeGroups[ending]) {
      rhymeGroups[ending] = groupCounter;
      groupCounter = (groupCounter % 4) + 1; // Cycle through 4 groups
    }
    
    const groupNum = rhymeGroups[ending];
    return `<span class="rhyme-group-${groupNum}">${word}</span>`;
  });
  
  return highlightedWords.join(' ');
};

// Alternative: If you want to call the Python script directly
export const processLyricsDirect = async (lyrics) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/process`, {
      lyrics: lyrics
    });
    return response.data;
  } catch (error) {
    console.error('Error processing lyrics:', error);
    throw new Error('Failed to process lyrics');
  }
};
