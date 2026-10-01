// ==========================================
// EduGenie Frontend JavaScript
// ==========================================


// ------------------------------------------
// Helper function
// ------------------------------------------

function showResult(elementId, message) {
    const element = document.getElementById(elementId);

    if (element) {
        element.innerHTML = message;
    }
}


// ------------------------------------------
// Ask Question
// ------------------------------------------

async function askQuestion() {

    const questionInput = document.getElementById("question");
    const question = questionInput.value.trim();

    if (!question) {
        showResult(
            "qa-result",
            "<p>Please enter a question.</p>"
        );
        return;
    }

    showResult(
        "qa-result",
        "<p>Thinking...</p>"
    );

    try {

        const response = await fetch(
            `/qa?question=${encodeURIComponent(question)}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Unable to answer the question."
            );
        }

        showResult(
            "qa-result",
            `
            <h3>Answer</h3>
            <p>${formatText(data.answer)}</p>
            `
        );

    } catch (error) {

        showResult(
            "qa-result",
            `<p>Error: ${escapeHtml(error.message)}</p>`
        );
    }
}


// ------------------------------------------
// Explain Topic
// ------------------------------------------

async function explainTopic() {

    const topicInput = document.getElementById("topic");
    const topic = topicInput.value.trim();

    if (!topic) {
        showResult(
            "explain-result",
            "<p>Please enter a topic.</p>"
        );
        return;
    }

    showResult(
        "explain-result",
        "<p>Generating explanation...</p>"
    );

    try {

        const response = await fetch("/explain", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                topic: topic
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Unable to explain the topic."
            );
        }

        showResult(
            "explain-result",
            `
            <h3>Explanation</h3>
            <p>${formatText(data.explanation)}</p>
            `
        );

    } catch (error) {

        showResult(
            "explain-result",
            `<p>Error: ${escapeHtml(error.message)}</p>`
        );
    }
}


// ------------------------------------------
// Summarize Text
// ------------------------------------------

async function summarizeText() {

    const textInput = document.getElementById("summary-text");
    const text = textInput.value.trim();

    if (!text) {
        showResult(
            "summary-result",
            "<p>Please enter some text.</p>"
        );
        return;
    }

    showResult(
        "summary-result",
        "<p>Creating summary...</p>"
    );

    try {

        const response = await fetch("/summarize", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Unable to summarize the text."
            );
        }

        showResult(
            "summary-result",
            `
            <h3>Summary</h3>
            <p>${formatText(data.summary)}</p>
            `
        );

    } catch (error) {

        showResult(
            "summary-result",
            `<p>Error: ${escapeHtml(error.message)}</p>`
        );
    }
}


// ------------------------------------------
// Generate Quiz
// ------------------------------------------

async function generateQuiz() {

    const textInput = document.getElementById("quiz-text");
    const text = textInput.value.trim();

    if (!text) {
        showResult(
            "quiz-result",
            "<p>Please enter study material.</p>"
        );
        return;
    }

    showResult(
        "quiz-result",
        "<p>Generating quiz...</p>"
    );

    try {

        const response = await fetch("/quiz", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Unable to generate the quiz."
            );
        }

        showResult(
            "quiz-result",
            `
            <h3>Quiz</h3>
            <pre>${escapeHtml(
                JSON.stringify(data.quiz, null, 2)
            )}</pre>
            `
        );

    } catch (error) {

        showResult(
            "quiz-result",
            `<p>Error: ${escapeHtml(error.message)}</p>`
        );
    }
}


// ------------------------------------------
// Learning Path
// ------------------------------------------

async function getLearningPath() {

    const topicInput =
        document.getElementById("learning-topic");

    const topic = topicInput.value.trim();

    if (!topic) {
        showResult(
            "learning-result",
            "<p>Please enter a topic.</p>"
        );
        return;
    }

    showResult(
        "learning-result",
        "<p>Creating learning path...</p>"
    );

    try {

        const response = await fetch(
            `/learn/recommendations?topic=${encodeURIComponent(topic)}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Unable to create learning path."
            );
        }

        showResult(
            "learning-result",
            `
            <h3>Recommended Learning Path</h3>
            <p>${formatText(data.recommendation)}</p>
            `
        );

    } catch (error) {

        showResult(
            "learning-result",
            `<p>Error: ${escapeHtml(error.message)}</p>`
        );
    }
}


// ------------------------------------------
// Security / Display Helpers
// ------------------------------------------

function escapeHtml(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


function formatText(text) {

    if (!text) {
        return "";
    }

    return escapeHtml(text)
        .replace(/\n/g, "<br>");
}