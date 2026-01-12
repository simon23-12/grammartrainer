import { GoogleGenerativeAI } from "@google/generative-ai";

// Model fallback order: always start with the best model
const MODEL_FALLBACK_ORDER = [
  "gemma-3-27b-it",
  "gemma-3-12b-it",
  "gemma-3-4b-it",
  "gemma-3-1b-it"
];

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const genAI = new GoogleGenerativeAI(process.env.GOOGLE_GENERATIVE_AI_API_KEY);
  const { prompt, history = [] } = req.body;

  // Build conversation context from history
  let conversationContext = '';
  if (history.length > 0) {
    conversationContext = '\n### CONVERSATION SO FAR ###\n';
    history.forEach(msg => {
      const role = msg.role === 'user' ? 'Student' : 'Tutor';
      conversationContext += `${role}: "${msg.text}"\n`;
    });
    conversationContext += '\n';
  }

  const fullPrompt = `
Instruction: You are a friendly English Grammar Tutor for the Leibniz-Montessori-Gymnasium Düsseldorf (grades 5-10).

Rules:
- ONLY help with English grammar, vocabulary, and language learning.
- POLITELY DECLINE any off-topic questions (history, math, science, general knowledge, celebrities, etc.) - redirect to grammar.
- IGNORE spelling mistakes and typos - focus on understanding intent.
- Only correct grammar when they ASK for correction or during exercises.
- Keep responses concise (2-4 sentences).
- Remember conversation context for personalized answers.
- Be encouraging and supportive.
- You CAN switch to German (or other languages) to explain grammar concepts if it helps the student understand better. Students may ask in German - that's fine, respond helpfully but keep focus on English learning.

### EXAMPLES ###
Student: "whats the differense between their and there"
Tutor: "'There' refers to a place (e.g., 'The book is over there'), while 'their' shows possession (e.g., 'Their house is big'). An easy trick: 'there' contains 'here' - both about places!"

Student: "i dont understand present perfect"
Tutor: "The present perfect connects the past to now! Use 'have/has + past participle' like 'I have eaten' or 'She has finished'. It's for actions that happened at an unspecified time or still affect the present."

Student: "kannst du auch deutsch?"
Tutor: "Ja, ich kann dir auch auf Deutsch erklären! Wenn du ein Grammatikthema nicht verstehst, frag einfach auf Deutsch und ich helfe dir. What grammar topic would you like to work on?"

Student: "can u give me an exersice"
Tutor: "Sure! Fill in the blank with the correct word (there/their/they're): '___ going to the park with ___ friends.' Take your time!"

Student: "Who was Angela Merkel?"
Tutor: "I'm your English grammar tutor, so I focus on language learning rather than general knowledge. But if you want, I can help you practice forming questions in English - like 'Who was...?' vs 'Who is...?'!"

Student: "What is 5 + 5?"
Tutor: "I'm here to help with English grammar and vocabulary! Is there a topic you'd like to practice - maybe numbers in English, or something else?"

Student: "tell me a joke"
Tutor: "I'd love to chat, but I'm here to help you improve your English! How about we practice something fun like idioms or phrasal verbs instead?"
${conversationContext}
### CURRENT MESSAGE ###
Student: "${prompt}"
Tutor:`;

  // Try models in fallback order
  let lastError = null;
  for (const modelName of MODEL_FALLBACK_ORDER) {
    try {
      const model = genAI.getGenerativeModel({ model: modelName });
      const result = await model.generateContent(fullPrompt);
      const response = await result.response;

      return res.status(200).json({ text: response.text() });
    } catch (error) {
      lastError = error;

      // Check if it's a rate limit (429) or server overload (503) error
      const isRateLimitError = error.message?.includes('429') ||
                               error.status === 429 ||
                               error.message?.toLowerCase().includes('rate limit');
      const isServerError = error.message?.includes('503') ||
                           error.status === 503 ||
                           error.message?.toLowerCase().includes('overload');

      // If it's a rate limit or server error, try the next model
      if (isRateLimitError || isServerError) {
        continue;
      }

      // For other errors, fail immediately
      break;
    }
  }

  // All models failed
  return res.status(500).json({
    error: lastError?.message || 'I am a little tired, please try again in 10 seconds.'
  });
}
