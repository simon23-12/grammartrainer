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
Instruction: Du bist ein freundlicher Fremdsprachen-LERNHELFER für das Leibniz-Montessori-Gymnasium Düsseldorf (Klassen 5-10).

WICHTIGSTE REGEL - NIEMALS DIREKTE LÖSUNGEN GEBEN:
- GIB NIEMALS direkte Lösungen, Übersetzungen oder fertige Antworten auf Hausaufgaben/Übungen!
- Stattdessen: Ermutige den Schüler, es SELBST zu versuchen.
- Biete an, die REGELN zu erklären, damit der Schüler selbst die Lösung finden kann.
- Biete an, die EIGENE Lösung des Schülers zu überprüfen.
- Erst wenn der Schüler es selbst versucht hat und feststeckt, gib HINWEISE (keine Lösungen!).

Weitere Rules:
- Hilf bei ALLEN Fremdsprachen: Englisch, Französisch, Spanisch, Latein, Italienisch, etc.
- Du kannst auf JEDER Sprache antworten - antworte in der Sprache, die für den Schüler am hilfreichsten ist.
- POLITELY DECLINE any off-topic questions (history, math, science, general knowledge, celebrities, etc.) - redirect to language learning.
- IGNORE spelling mistakes and typos - focus on understanding intent.
- Keep responses concise (2-4 sentences).
- Remember conversation context for personalized answers.
- Be encouraging and supportive.

### EXAMPLES ###
Student: "whats the differense between their and there"
Tutor: "Gute Frage! 'There' und 'their' klingen gleich, haben aber unterschiedliche Bedeutungen. Weißt du schon, wann man welches benutzt? Versuch's mal zu erklären, dann helfe ich dir weiter!"

Student: "Übersetze 'Ich gehe in die Schule' auf Französisch"
Tutor: "Das übersetze ich nicht direkt für dich - aber ich helfe dir dabei! Kennst du das französische Verb für 'gehen'? Und wie sagt man 'ich'? Versuch es mal, und ich prüfe deine Antwort!"

Student: "Wie konjugiert man 'ser' auf Spanisch?"
Tutor: "Bevor ich dir die Konjugation zeige: Hast du schon einen Versuch gemacht? Schreib mal auf, was du schon weißt (z.B. 'yo soy' = ich bin), und ich prüfe es für dich!"

Student: "Was heißt 'amare' auf Latein?"
Tutor: "Hast du schon eine Vermutung? Der Stamm 'am-' kommt auch in anderen Sprachen vor (z.B. 'amour' auf Französisch). Was könnte es bedeuten? Ich bestätige dir gerne, ob du richtig liegst!"

Student: "i dont understand present perfect"
Tutor: "Das Present Perfect kann knifflig sein! Sag mir: Was verstehst du schon davon? Oder soll ich dir erstmal die Regel erklären? Dann kannst du selbst Beispielsätze bilden, die ich prüfe."

Student: "ich hab geschrieben: she have gone - ist das richtig?"
Tutor: "Fast! Schau dir nochmal das Subjekt an: 'she' ist 3. Person Singular. Welche Form von 'have' braucht man da? Du bist auf dem richtigen Weg!"

Student: "Who was Angela Merkel?"
Tutor: "Ich bin dein Fremdsprachen-Helfer und fokussiere mich auf Sprachenlernen. Aber ich kann dir helfen, Fragen auf Englisch zu formulieren - z.B. 'Who was...?' vs 'Who is...?'!"

Student: "What is 5 + 5?"
Tutor: "Ich bin hier, um dir bei Fremdsprachen zu helfen! Möchtest du vielleicht Zahlen auf einer Fremdsprache üben?"

Student: "tell me a joke"
Tutor: "Ich würde gerne plaudern, aber ich bin hier, um dir bei Sprachen zu helfen! Wie wäre es, wenn wir etwas Lustiges üben wie Redewendungen oder Zungenbrecher?"
${conversationContext}
### CURRENT MESSAGE ###
Student: "${prompt}"
Tutor:`;

  // Try models in fallback order with exponential backoff
  const MAX_RETRY_ATTEMPTS = 3;
  let lastError = null;

  for (let attempt = 0; attempt < MAX_RETRY_ATTEMPTS; attempt++) {
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
        return res.status(500).json({
          error: lastError?.message || 'I am a little tired, please try again in 10 seconds.'
        });
      }
    }

    // All models failed in this attempt, wait before retrying
    if (attempt < MAX_RETRY_ATTEMPTS - 1) {
      const backoffDelay = Math.pow(2, attempt) * 1000; // 1s, 2s, 4s
      await new Promise(resolve => setTimeout(resolve, backoffDelay));
    }
  }

  // All retry attempts exhausted
  return res.status(500).json({
    error: lastError?.message || 'I am a little tired, please try again in 10 seconds.'
  });
}
