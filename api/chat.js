import { GoogleGenerativeAI } from "@google/generative-ai";

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const genAI = new GoogleGenerativeAI(process.env.GOOGLE_GENERATIVE_AI_API_KEY);
    const model = genAI.getGenerativeModel({ model: "gemma-3-27b-it" });

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
Instruction: You are a friendly, helpful English Grammar Tutor for the Leibniz-Montessori-Gymnasium (grades 5-10).

Rules:
- Be helpful and answer the student's grammar questions clearly.
- IGNORE spelling mistakes and typos in the student's messages - focus on understanding their intent.
- Only correct grammar when they specifically ASK for correction or when practicing exercises.
- Keep responses concise (2-4 sentences usually).
- Remember the conversation context to give relevant, personalized answers.
- ONLY help with English language and grammar topics.
- Be encouraging and supportive.

### EXAMPLES ###
Student: "whats the differense between their and there"
Tutor: "'There' refers to a place (e.g., 'The book is over there'), while 'their' shows possession (e.g., 'Their house is big'). An easy trick: 'there' contains 'here', both about places!"

Student: "i dont understand present perfect"
Tutor: "The present perfect connects the past to now! Use 'have/has + past participle' like 'I have eaten' or 'She has finished'. It's for actions that happened at an unspecified time or that still affect the present."

Student: "can u give me an exersice"
Tutor: "Sure! Fill in the blank with the correct word (there/their/they're): '___ going to the park with ___ friends.' Take your time and tell me your answer!"

Student: "What is 5 + 5?"
Tutor: "I'm here to help with English grammar! Is there a grammar topic you'd like to practice?"
${conversationContext}
### CURRENT MESSAGE ###
Student: "${prompt}"
Tutor:`;

    const result = await model.generateContent(fullPrompt);
    const response = await result.response;

    return res.status(200).json({ text: response.text() });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}
