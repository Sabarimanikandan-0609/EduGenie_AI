const $ = (id) => {
  return document.getElementById(id);
};


/* -------------------------
   HTML SECURITY
------------------------- */

function escapeHtml(value) {

  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}


/* -------------------------
   OUTPUT
------------------------- */

function setOutput(
  id,
  content,
  isError = false
) {

  const element = $(id);

  element.className =
    `output${isError ? " error" : ""}`;

  element.innerHTML = content;
}


/* -------------------------
   API REQUEST
------------------------- */

async function requestJson(
  url,
  options = {}
) {

  const response = await fetch(
    url,
    {
      headers: {
        "Content-Type":
          "application/json",

        ...(options.headers || {})
      },

      ...options
    }
  );


  const data =
    await response
      .json()
      .catch(() => ({}));


  if (!response.ok) {

    throw new Error(
      data.detail ||
      data.error ||
      `Request failed (${response.status})`
    );
  }


  return data;
}


/* -------------------------
   FORM HELPER
------------------------- */

function bindForm(
  formId,
  loadingText,
  handler
) {

  $(formId).addEventListener(
    "submit",
    async (event) => {

      event.preventDefault();


      const button =
        event.currentTarget
          .querySelector(
            "button[type=submit]"
          );


      const originalText =
        button.textContent;


      button.disabled = true;

      button.textContent =
        loadingText;


      try {

        await handler();

      }

      catch (error) {

        console.error(error);

      }

      finally {

        button.disabled = false;

        button.textContent =
          originalText;

      }

    }
  );
}


/* -------------------------
   Q&A
------------------------- */

bindForm(
  "qaForm",
  "Thinking...",
  async () => {

    try {

      const question =
        $("question")
          .value
          .trim();


      if (!question) {

        setOutput(
          "qaResult",
          "Please enter a question.",
          true
        );

        return;
      }


      const data =
        await requestJson(
          `/api/qna?question=${encodeURIComponent(question)}`
        );


      setOutput(
        "qaResult",

        `
        <strong>Answer</strong>
        <br><br>
        ${escapeHtml(data.answer)}
        `
      );

    }

    catch (error) {

      setOutput(
        "qaResult",
        escapeHtml(error.message),
        true
      );

    }

  }
);


/* -------------------------
   EXPLANATION
------------------------- */

bindForm(
  "explainForm",
  "Explaining...",
  async () => {

    try {

      const topic =
        $("topic")
          .value
          .trim();


      const data =
        await requestJson(
          "/api/explain",
          {
            method: "POST",

            body: JSON.stringify({
              topic: topic
            })
          }
        );


      setOutput(
        "explanationResult",

        `
        <strong>
          Explanation
        </strong>

        <br><br>

        ${escapeHtml(
          data.explanation
        )}
        `
      );

    }

    catch (error) {

      setOutput(
        "explanationResult",
        escapeHtml(error.message),
        true
      );

    }

  }
);


/* -------------------------
   SUMMARIZER
------------------------- */

bindForm(
  "summaryForm",
  "Summarizing...",
  async () => {

    try {

      const text =
        $("summaryText")
          .value
          .trim();


      const data =
        await requestJson(
          "/api/summarize",
          {
            method: "POST",

            body: JSON.stringify({
              text: text
            })
          }
        );


      setOutput(
        "summaryResult",

        `
        <strong>
          Summary
        </strong>

        <br><br>

        ${escapeHtml(
          data.summary
        )}
        `
      );

    }

    catch (error) {

      setOutput(
        "summaryResult",
        escapeHtml(error.message),
        true
      );

    }

  }
);


/* -------------------------
   QUIZ
------------------------- */

bindForm(
  "quizForm",
  "Generating...",
  async () => {

    try {

      const text =
        $("quizText")
          .value
          .trim();


      const data =
        await requestJson(
          "/api/quiz",
          {
            method: "POST",

            body: JSON.stringify({
              text: text
            })
          }
        );


      renderQuiz(
        data.quiz
      );

    }

    catch (error) {

      setOutput(
        "quizResult",
        escapeHtml(error.message),
        true
      );

    }

  }
);


/* -------------------------
   RENDER QUIZ
------------------------- */

function renderQuiz(quiz) {

  const html =
    quiz
      .map(
        (item, index) => {

          return `

          <div
            class="quiz-question"
          >

            <strong>
              Q${index + 1}.
              ${escapeHtml(
                item.question
              )}
            </strong>

            <div class="quiz-options">

              ${item.options
                .map(
                  (option) => {

                    return `

                    <div
                      class="quiz-option"
                    >

                      <button
                        type="button"
                        data-answer="${escapeHtml(
                          option
                        )}"
                      >
                        ${escapeHtml(
                          option
                        )}
                      </button>

                    </div>

                    `;

                  }
                )
                .join("")}

            </div>

          </div>

          `;

        }
      )
      .join("");


  setOutput(
    "quizResult",
    html
  );


  document
    .querySelectorAll(
      "#quizResult button[data-answer]"
    )
    .forEach(
      (button) => {

        button.addEventListener(
          "click",
          () => {

            const question =
              button.closest(
                ".quiz-question"
              );


            const index =
              [
                ...question
                  .parentElement
                  .children
              ].indexOf(question);


            const correct =
              quiz[index].answer;


            const buttons =
              question.querySelectorAll(
                "button[data-answer]"
              );


            buttons.forEach(
              (item) => {
                item.disabled = true;
              }
            );


            if (
              button.dataset.answer ===
              correct
            ) {

              button.classList.add(
                "correct"
              );

            }

            else {

              button.classList.add(
                "wrong"
              );


              const correctButton =
                [
                  ...buttons
                ].find(
                  (item) =>
                    item.dataset.answer ===
                    correct
                );


              if (correctButton) {

                correctButton.classList.add(
                  "correct"
                );

              }

            }

          }
        );

      }
    );
}


/* -------------------------
   LEARNING PATH
------------------------- */

bindForm(
  "learningForm",
  "Building...",
  async () => {

    try {

      const topic =
        $("learningTopic")
          .value
          .trim();


      const data =
        await requestJson(
          `/api/learn/recommendations?topic=${encodeURIComponent(topic)}`
        );


      setOutput(
        "learningResult",

        `
        <strong>
          Learning Path:
          ${escapeHtml(
            data.topic
          )}
        </strong>

        <br><br>

        ${escapeHtml(
          data.recommendation
        )}
        `
      );

    }

    catch (error) {

      setOutput(
        "learningResult",
        escapeHtml(error.message),
        true
      );

    }

  }
);


/* -------------------------
   SERVER STATUS
------------------------- */

async function loadStatus() {

  try {

    const data =
      await requestJson(
        "/api/health"
      );


    if (
      data.gemini_configured
    ) {

      $("status").textContent =
        `🟢 AI Ready • ${data.model}`;

      $("status").classList.add(
        "ready"
      );

    }

    else {

      $("status").textContent =
        "🔴 Gemini API key not configured";

      $("status").classList.add(
        "not-ready"
      );

    }

  }

  catch (error) {

    $("status").textContent =
      "🔴 Backend unavailable";

  }

}


loadStatus();