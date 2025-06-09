# AI Hiring Assistant Chatbot

An intelligent hiring assistant that automates technical interviews for software engineering roles. Built with LangGraph and LangChain, this bot conducts structured conversations to screen candidates efficiently.

## What This Project Does

This AI hiring assistant streamlines the initial screening process by conducting automated technical interviews. It walks candidates through a complete evaluation process including personal information gathering, tech stack assessment, and technical questioning.

The bot maintains conversation context throughout the interview and generates personalized questions based on each candidate's technical background. It's designed to feel natural while ensuring consistent evaluation criteria across all candidates.

## Key Features

- **Structured Interview Flow**: Guides candidates through greeting, information collection, tech assessment, and technical evaluation
- **Smart Question Generation**: Creates relevant questions based on the candidate's mentioned technologies
- **Memory Management**: Remembers the conversation context and previous responses
- **Automated Scoring**: Evaluates performance and provides detailed feedback
- **Multi-stage Routing**: Intelligently moves between different interview phases

## Getting Started

### What You'll Need

- Python 3.8 or newer
- A Groq API key (for the LLM)
- LangSmith API key (for tracking conversations)

### Installation

First, clone this repository:
```bash
git clone <your-repository-url>
cd hiring-assistant-chatbot
```

Since this project uses Poetry for dependency management, install Poetry first if you don't have it:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Install the project dependencies:
```bash
poetry install
```

Create a `.env` file in the root directory with your API keys:
```env
GROQ_API_KEY=your_groq_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=hiring-assistant
```

Run the application:
```bash
poetry run python main.py
```

## How to Use

When you start the bot, it will introduce itself as a TalentScout AI Hiring Assistant. The interview process has four main stages:

**Stage 1: Greeting**
The bot introduces itself and explains the process.

**Stage 2: Information Gathering**
You'll be asked to provide basic details. The required information differs based on your experience level:
- **New graduates**: Email, desired position, location, phone number
- **Experienced professionals**: Email, years of experience, desired position, location, phone number

**Stage 3: Tech Stack Assessment**
List the technologies you're comfortable with. Be honest and only mention things you have real experience with. This includes programming languages, frameworks, databases, tools, and cloud platforms.

**Stage 4: Technical Questions**
You'll answer 4 questions tailored to your tech stack:
- 2 multiple choice questions
- 1 code debugging task
- 1 descriptive technical question

The questions progress from easy to hard, and you have 50 minutes total. You need 50/100 to pass (70/100 if you're a fresher).

To exit at any time, type "exit" or "quit".

## Technical Implementation

### Architecture

The bot uses a graph-based conversation flow powered by LangGraph. Each stage is a separate node that processes user input and determines the next step:

```
Greeting → Info Collection → Tech Assessment → Technical Questions → Results
```

### Technologies Used

- **LangChain with Groq**: Powers the conversational AI using Llama3-70B
- **LangGraph**: Manages the conversation flow and state transitions
- **Poetry**: Handles dependency management and virtual environments
- **LangSmith**: Tracks conversations and performance metrics

### How the State Management Works

The bot keeps track of where you are in the interview using flags:
- `greeting_done`: Whether the introduction is complete
- `info_done`: Whether personal info has been collected
- `tech_done`: Whether tech stack assessment is finished
- `hiring_question_count`: How many technical questions have been asked

It also maintains the last few messages of your conversation to provide context for generating appropriate responses.

### Prompt Engineering Strategy

Each stage uses carefully designed prompts:

**Greeting prompts** are warm and professional to put candidates at ease.

**Information gathering prompts** use clear formatting requirements to ensure consistent data collection.

**Tech stack prompts** encourage honest self-assessment across multiple technical domains.

**Hiring prompts** dynamically generate questions based on the candidate's background while maintaining evaluation consistency.

The system maintains conversation history by keeping the last 4 messages, which provides enough context without overwhelming the language model.

## Challenges We Solved

### Managing Complex Conversation State
Initially, keeping track of where each candidate was in the interview process was tricky. We solved this by implementing a clear state machine with boolean flags for each stage completion, making it easy to resume conversations and ensure no steps are skipped.

### Generating Relevant Technical Questions
Creating meaningful questions for candidates with diverse tech backgrounds was challenging. We addressed this by designing flexible prompt templates that adapt to user input while maintaining consistent evaluation standards across different technology stacks.

### Balancing Context and Performance
Keeping enough conversation history for natural responses while avoiding context overload required careful tuning. We settled on a sliding window of the last 4 messages, which provides sufficient context while keeping API calls efficient.

### Ensuring Fair Evaluation
Maintaining consistent scoring across different candidates and tech stacks required standardized question types and clear evaluation criteria. We implemented structured assessment with defined difficulty levels and scoring rubrics.

### Handling Unexpected User Inputs
Users don't always follow instructions perfectly, so we built robust error handling and conversation recovery mechanisms. The bot can gracefully handle off-topic responses and guide users back to the interview flow.

## Performance Monitoring

The application integrates with LangSmith to track:
- Conversation quality and flow
- Response times and API usage
- User engagement patterns
- Common failure points

This data helps improve the interview experience over time.

## Contributing

If you'd like to contribute:

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Test thoroughly
5. Submit a pull request

We welcome improvements to question generation, conversation flow, or evaluation criteria.

## Project Structure

```
├── main.py              # Main application entry point
├── templates.py         # Prompt templates for each stage
├── smith.py            # LangSmith integration
├── back_end/
│   └── config.py       # Configuration settings
├── pyproject.toml      # Poetry dependency configuration
└── .env               # API keys (create this file)
```

## Future Improvements

- Add support for more programming languages and frameworks
- Implement video interview capabilities
- Create detailed analytics dashboard
- Add multi-language support
- Integrate with HR management systems

---

This project demonstrates how conversational AI can streamline hiring processes while maintaining the human touch that candidates appreciate. The structured approach ensures fair evaluation while the natural language interface keeps the experience engaging.