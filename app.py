from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
from google import genai
from google.genai import types

app = Flask(__name__)
CORS(app)  # Enable CORS for React app

def process_lyrics_with_gemini(lyrics_text):
    """Process lyrics using Google Gemini AI to identify rhyming patterns"""
    try:
        client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
        )

        model = "gemini-flash-lite-latest"
        
        # Create a prompt that asks Gemini to identify rhyming words
        prompt = f"""
            You are an intelligent rhyming assistant. Your task is to analyze given lyrics and produce **HTML output** that highlights rhymes in the words and phonemes.

            ### Requirements:

            1. **Identify rhyme groups**:

            * Words and phonemes that rhyme (perfect rhymes, slant rhymes, assonance, consonance) must be grouped together.
            * Each rhyme group should share the same **background color**.
            * Different rhyme groups must have **different colors**.

            2. **Output format**:

            * Wrap each rhyming word or phrase in a `<span>` tag with an inline CSS background color.
            * Example:

                ```html
                <span style="background-color:#FF9999">red</span>
                ```
            * Use consistent coloring across the whole text (all words in the same rhyme group must use the same color).

            3. **Accuracy**:

            * Consider rhyme not only in spelling but also in **sound** (phonetic/phoneme-level analysis).
            * Handle multi-syllable rhymes, internal rhymes, and near rhymes.

            4. **Style**:

            * Preserve the original formatting of the lyrics (line breaks, punctuation, spacing).
            * Only add `<span>` tags with color to highlight rhymes.

            5. **Output ONLY valid HTML**. Do not add explanations, markdown, or commentary outside the HTML.

            I've attached an example of how colors shoudl be highlighted for a set of text from a rap song.

            Like <span style="background-color:#E06666">Red</span> <span style="background-color:#6AA84F">Rover</span>, so you <span style="background-color:#99CCEE">know</span> what I <span style="background-color:#D39A3D">meant</span><br>
            But I <span style="background-color:#99CCEE">roll</span> <span style="background-color:#6AA84F">over</span> my <span style="background-color:#D39A3D">opponents</span> instead<br>
            <span style="background-color:#FFD700">Makin’</span> <span style="background-color:#C27BA0">dog</span> <span style="background-color:#99CCEE">sounds</span> ’cause I gotta keep<br>
            <span style="background-color:#FFD700">breakin’</span> these <span style="background-color:#D39A3D">bars</span> <span style="background-color:#E06666">down</span><br>
            I’ll <span style="background-color:#99CCEE">go</span> <span style="background-color:#99CCEE">slow</span> for the <span style="background-color:#D39A3D">speds</span>
 
            
            Lyrics to analyze:
            {lyrics_text}
            
            Return only the HTML with the spans, no explanations.
        """
        
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt),
                ],
            ),
        ]
        
        tools = [
            types.Tool(googleSearch=types.GoogleSearch()),
        ]
        
        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_budget=0,
            ),
            tools=tools,
        )

        # Generate the response
        response_text = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            response_text += chunk.text

        return response_text.strip()
        
    except Exception as e:
        print(f"Error processing with Gemini: {e}")
        # Fallback: simple rhyme detection
        return simple_rhyme_detection(lyrics_text)

def simple_rhyme_detection(text):
    """Simple fallback rhyme detection if Gemini fails"""
    words = text.split()
    rhyme_groups = {}
    group_counter = 1
    
    for i, word in enumerate(words):
        clean_word = word.lower().replace(',', '').replace('.', '').replace('!', '').replace('?', '')
        if len(clean_word) < 3:
            continue
            
        # Simple rhyme detection based on ending sounds
        ending = clean_word[-3:] if len(clean_word) >= 3 else clean_word[-2:]
        
        if ending not in rhyme_groups:
            rhyme_groups[ending] = group_counter
            group_counter += 1
        
        group_num = rhyme_groups[ending]
        words[i] = f'<span class="rhyme-group-{group_num}">{word}</span>'
    
    return ' '.join(words)

@app.route('/api/process', methods=['POST'])
def process_lyrics():
    """API endpoint to process lyrics"""
    try:
        data = request.get_json()
        lyrics = data.get('lyrics', '')
        
        if not lyrics:
            return jsonify({'error': 'No lyrics provided'}), 400
        
        # Process with Gemini
        highlighted_html = process_lyrics_with_gemini(lyrics)
        
        return jsonify({
            'success': True,
            'highlighted_html': highlighted_html
        })
        
    except Exception as e:
        print(f"Error in process_lyrics: {e}")
        return jsonify({'error': 'Failed to process lyrics'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    # Check if API key is set
    if not os.environ.get("GEMINI_API_KEY"):
        print("Warning: GEMINI_API_KEY environment variable not set")
        print("The app will use fallback rhyme detection")
    
    app.run(debug=True, host='0.0.0.0', port=8000)
