// Generate a unique session ID and add it to user selections
const sessionId = "session_" + Date.now();
const userSelections = {
  major: '',
  year: '',
  prompt: '',
  session_id: sessionId
};

// Function to provide follow-up suggestions based on major
function getFollowUpSuggestions(major) {
  switch (major) {
    case 'computer_science':
      return [
        "How to manage large group coding projects?",
        "Tips for staying updated with new frameworks?",
        "Balancing coding interviews with class assignments."
      ];
    case 'psychology':
      return [
        "Ways to handle test anxiety more effectively.",
        "How to balance research participation and coursework.",
        "Techniques for better self-reflection and mindfulness."
      ];
    case 'communications':
      return [
        "Methods to overcome public speaking fears.",
        "Strategies for resolving group conflicts smoothly.",
        "Tips for narrowing down media topics effectively."
      ];
    case 'finance':
      return [
        "Approaches to handling market-induced stress.",
        "Best ways to juggle internship applications with classes.",
        "Techniques for improving quantitative coursework."
      ];
    case 'economics':
      return [
        "How to connect economic theory to current events.",
        "Tips for understanding abstract models more intuitively.",
        "Approaches for tackling heavy reading loads."
      ];
    case 'business':
      return [
        "Ideas for effective networking while studying.",
        "How to cope with entrepreneurial uncertainty.",
        "Balancing part-time jobs or internships with coursework."
      ];
    case 'mechanical_engineering':
      return [
        "Time management for intense project deadlines.",
        "How to approach complex design and prototyping tasks.",
        "Techniques for effective lab or workshop collaboration."
      ];
    case 'electrical_engineering':
      return [
        "Managing complex circuit design with coursework.",
        "Staying updated with rapid tech advances in the field.",
        "Balancing hardware-software integration projects."
      ];
    case 'biology':
      return [
        "Tips to memorize vast terminologies effectively.",
        "Balancing lab experiments with lecture studies.",
        "How to manage lab work pressure and protocols."
      ];
    case 'chemistry':
      return [
        "Strategies for understanding complex reactions.",
        "Best practices for safety and efficiency in labs.",
        "Balancing theory with hands-on experiments."
      ];
    case 'environmental_science':
      return [
        "Dealing with climate anxiety and eco-stress.",
        "Overcoming limitations in field studies or research.",
        "Tips for staying motivated in policy setbacks."
      ];
    case 'fine_arts_humanities':
      return [
        "Overcoming creative block and finding inspiration.",
        "Balancing creative work with critical theory.",
        "Navigating lack of funding or recognition."
      ];
    default:
      return [
        "Time management strategies for busy schedules.",
        "How to handle stress when juggling multiple commitments.",
        "Techniques for staying motivated during tough times."
      ];
  }
}

// Grab DOM elements
const steps = document.querySelectorAll('.step');
const majorOptions = document.querySelectorAll('#major-options .option-btn');
const yearOptions = document.querySelectorAll('#year-options .option-btn');
const majorContinue = document.getElementById('major-continue');
const yearContinue = document.getElementById('year-continue');
const promptContinue = document.getElementById('prompt-continue');
const customMajorBtn = document.getElementById('custom-major-btn');
const customMajorInput = document.getElementById('custom-major');
const userPromptInput = document.getElementById('user-prompt');
const supportContent = document.getElementById('support-content');
const restartBtn = document.getElementById('restart-btn');

// For suggestions container
const suggestionsContainer = document.getElementById('suggestions-container');
const suggestionButtonsDiv = document.getElementById('suggestion-buttons');

// Select major from predefined buttons
majorOptions.forEach(btn => {
  btn.addEventListener('click', () => {
    majorOptions.forEach(b => b.classList.remove('selected'));
    btn.classList.add('selected');
    userSelections.major = btn.dataset.value;
  });
});

// Select academic year from predefined buttons
yearOptions.forEach(btn => {
  btn.addEventListener('click', () => {
    yearOptions.forEach(b => b.classList.remove('selected'));
    btn.classList.add('selected');
    userSelections.year = btn.dataset.value;
  });
});

// Custom major input event
customMajorBtn.addEventListener('click', () => {
  const val = customMajorInput.value.trim();
  if (val !== '') {
    majorOptions.forEach(b => b.classList.remove('selected'));
    userSelections.major = val.toLowerCase().replace(/\s+/g, '_');
    customMajorInput.style.borderColor = 'var(--primary-color)';
    majorContinue.removeAttribute('disabled');
  }
});

// Continue from Major step to Year step
majorContinue.addEventListener('click', () => {
  if (userSelections.major) {
    steps[0].classList.remove('active');
    steps[1].classList.add('active');
  } else {
    alert('Please select or enter your major to continue.');
  }
});

// Continue from Year step to Prompt step
yearContinue.addEventListener('click', () => {
  if (userSelections.year) {
    steps[1].classList.remove('active');
    steps[2].classList.add('active');
  } else {
    alert('Please select your academic year to continue.');
  }
});

// "Get Support" button event listener
promptContinue.addEventListener('click', () => {
  userSelections.prompt = userPromptInput.value.trim();
  steps[2].classList.remove('active');

  // Show "Thinking..." immediately
  supportContent.style.display = 'block';
  supportContent.innerHTML = "<p>Thinking...</p>";
  restartBtn.style.display = 'block';

  fetch("/api/get_support", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(userSelections)
  })
  .then(res => res.json())
  .then(data => {
    // Update session_id if returned from backend
    if (data.session_id) {
      userSelections.session_id = data.session_id;
    }
    // Display the fetched response
    displayTypingEffect(data.response);

    // Now provide follow-up suggestion buttons above the chat input
    const suggestions = getFollowUpSuggestions(userSelections.major);
    displaySuggestionButtons(suggestions);
  })
  .catch(err => {
    console.error("Fetch error:", err);
    supportContent.innerHTML = "Sorry, something went wrong fetching support content.";
  });
});

// Display suggestion buttons
function displaySuggestionButtons(suggestions) {
  // Clear any existing buttons
  suggestionButtonsDiv.innerHTML = "";
  // Create new buttons
  suggestions.forEach(s => {
    const btn = document.createElement('button');
    btn.classList.add('suggestion-btn');
    btn.textContent = s;
    btn.addEventListener('click', () => {
      handleSuggestionClick(s);
    });
    suggestionButtonsDiv.appendChild(btn);
  });
  // Show container
  suggestionsContainer.style.display = 'block';
}

// Handle suggestion click
function handleSuggestionClick(suggestion) {
  const chatMessages = document.getElementById('chat-messages');

  // Append user message bubble
  const userMessageDiv = document.createElement('div');
  userMessageDiv.classList.add('chat-message', 'user');
  userMessageDiv.textContent = suggestion;
  chatMessages.appendChild(userMessageDiv);

  // Prepare message object for continuation
  const chatData = {
    major: userSelections.major,
    year: userSelections.year,
    prompt: suggestion,
    session_id: userSelections.session_id
  };

  // Append placeholder for bot response
  const botMessageDiv = document.createElement('div');
  botMessageDiv.classList.add('chat-message', 'bot');
  botMessageDiv.textContent = "Thinking...";
  chatMessages.appendChild(botMessageDiv);

  chatMessages.scrollTop = chatMessages.scrollHeight;

  fetch("/api/get_support", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(chatData)
  })
  .then(res => res.json())
  .then(data => {
    displayTypingEffectInElement(data.response, botMessageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  })
  .catch(err => {
    console.error("Error in continuing chat:", err);
    botMessageDiv.textContent = "Sorry, something went wrong.";
  });
}

// Typing effect for support content display
function displayTypingEffect(htmlResponse) {
  supportContent.innerHTML = htmlResponse;
  // Show the chat container immediately after content is set
  document.getElementById('chat-container').style.display = 'block';
}

// Typing effect for bot messages in a chat bubble element
function displayTypingEffectInElement(htmlResponse, targetElement) {
  targetElement.innerHTML = htmlResponse;
}

// Chat send button event
const chatSendBtn = document.getElementById('chat-send-btn');
chatSendBtn.addEventListener('click', () => {
  const chatInput = document.getElementById('chat-input');
  const chatMessage = chatInput.value.trim();
  if (!chatMessage) return;

  const chatMessages = document.getElementById('chat-messages');

  // Append user message bubble
  const userMessageDiv = document.createElement('div');
  userMessageDiv.classList.add('chat-message', 'user');
  userMessageDiv.textContent = chatMessage;
  chatMessages.appendChild(userMessageDiv);

  // Clear the input
  chatInput.value = "";

  // Prepare message object
  const chatData = {
    major: userSelections.major,
    year: userSelections.year,
    prompt: chatMessage,
    session_id: userSelections.session_id
  };

  // Append placeholder for bot response
  const botMessageDiv = document.createElement('div');
  botMessageDiv.classList.add('chat-message', 'bot');
  botMessageDiv.textContent = "Thinking...";
  chatMessages.appendChild(botMessageDiv);

  chatMessages.scrollTop = chatMessages.scrollHeight;

  fetch("/api/get_support", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(chatData)
  })
  .then(res => res.json())
  .then(data => {
    displayTypingEffectInElement(data.response, botMessageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  })
  .catch(err => {
    console.error("Error in continuing chat:", err);
    botMessageDiv.textContent = "Sorry, something went wrong.";
  });
});

// Restart button event listener
restartBtn.addEventListener('click', () => {
  // Generate a new session ID for a fresh conversation
  userSelections.session_id = "session_" + Date.now();

  // Reset user selections
  userSelections.major = '';
  userSelections.year = '';
  userSelections.prompt = '';

  // Clear UI selections
  majorOptions.forEach(b => b.classList.remove('selected'));
  yearOptions.forEach(b => b.classList.remove('selected'));
  customMajorInput.value = '';
  userPromptInput.value = '';

  // Hide support content and restart button
  supportContent.style.display = 'none';
  restartBtn.style.display = 'none';
  supportContent.innerHTML = "";

  // Hide chat container and clear conversation
  const chatContainer = document.getElementById('chat-container');
  chatContainer.style.display = 'none';
  document.getElementById('chat-input').value = '';
  document.getElementById('chat-messages').innerHTML = "";

  // Hide suggestions
  suggestionsContainer.style.display = 'none';
  suggestionButtonsDiv.innerHTML = "";

  // Show the first step again
  steps.forEach(step => step.classList.remove('active'));
  steps[0].classList.add('active');
});
