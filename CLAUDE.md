# LMG Grammar Trainer

**Type:** HTML, JS, CSS
**Purpose:** English grammar training chatbot for students grade 5 to 10 at Leibniz-Montessori-Gymnasium Düsseldorf

## Structure
- `index.html` - Main page with chat interface (single-page app with embedded CSS and JS)
- `TODO.md` - Todos and ideas for future development
- `api/chat.js` - Vercel serverless function that handles chat API requests
- `api/package.json` - Package configuration for the API
- `images/schoollogoonly.png` - School logo image

## Tech Stack
- **Frontend:** Vanilla HTML/CSS/JavaScript (no framework)
- **Backend:** Vercel serverless functions
- **AI Model:** Google Gemma 3 27B (`gemma-3-27b-it`) via `@google/generative-ai` SDK
- **Styling:** CSS custom properties with light/dark theme support, Font Awesome icons
- **Hosting:** Designed for Vercel deployment

## Architecture
- Frontend sends POST requests to `/api/chat` with user prompts
- Backend constructs a prompt with system instructions and sends to Gemma API
- Bot is instructed to only answer English grammar questions, correct mistakes, and explain rules simply (max 3 sentences)

## Frugal Coding Rules
- Keep it simple - vanilla JS, no unnecessary dependencies
- Single-file frontend approach (embedded CSS/JS in HTML)
- Minimal API footprint

## Error handling
- Rate limit/server errors: Continue to next model
- Other errors: Fail immediately without retrying
- All models exhausted: Wait and retry entire circulation (exponential backoff)
