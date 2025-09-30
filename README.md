# 🎤 LyricRhymer

A React web application that uses AI to highlight rhyming patterns in rap lyrics. Users can input their rap lyrics and get a color-coded visualization showing which parts rhyme.

## Features

- **Modern React UI**: Clean, responsive interface with gradient backgrounds and smooth animations
- **AI-Powered Analysis**: Uses Google Gemini AI to identify rhyming patterns in lyrics
- **Color-Coded Highlights**: Different rhyme groups are highlighted with distinct colors
- **Real-time Processing**: Instant feedback as you input your lyrics
- **Python Backend**: Flask API that integrates with Google Gemini for intelligent rhyme detection

## Project Structure

```
lyricrhymer/
├── src/                    # React frontend
│   ├── components/         # React components
│   ├── api/               # API integration
│   └── ...
├── app.py                 # Python Flask backend
├── gemini.py             # Original Gemini integration
├── requirements.txt      # Python dependencies
└── package.json          # Node.js dependencies
```

## Setup Instructions

### Prerequisites

- Node.js (v14 or higher)
- Python 3.7+
- Google Gemini API key

### Frontend Setup (React)

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

The React app will be available at `http://localhost:3000`

### Backend Setup (Python)

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your environment variables:
```bash
# Create a .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

3. Start the Flask server:
```bash
python app.py
```

The API will be available at `http://localhost:8000`

### Getting a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

## Usage

1. Start both the React frontend and Python backend
2. Open your browser to `http://localhost:3000`
3. Paste your rap lyrics in the left textarea
4. Click "Highlight Rhymes" to process with AI
5. View the color-coded results on the right side

## API Endpoints

- `POST /api/process` - Process lyrics and return highlighted HTML
- `GET /health` - Health check endpoint

## Technologies Used

- **Frontend**: React, CSS3, Axios
- **Backend**: Python Flask, Google Gemini AI
- **Styling**: Custom CSS with gradients and animations
- **API Integration**: RESTful API with CORS support

## Development

The app includes both a simulation mode (for testing without API key) and real AI processing. The Python backend includes fallback rhyme detection if the Gemini API is unavailable.

## License

MIT License