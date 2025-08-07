# AI Blog Creation System with OpenAI Agents SDK

This system uses multiple specialized AI agents built with the **OpenAI Agents SDK** to create complete blog posts automatically. Each agent is optimized for specific tasks and configured with detailed instructions for their respective roles.

## 🌟 Features

- **Specialized Agents**: Each agent (Researcher, Writer, SEO Checker, etc.) is built using the OpenAI Agents SDK with role-specific instructions
- **Sequential Workflow**: Agents work in a coordinated sequence, with each agent building upon the previous agent's output
- **Advanced Agent Architecture**: Leverages the OpenAI Agents SDK for better performance, error handling, and agent management
- **SEO Optimization**: Built-in SEO analysis and content optimization using specialized agents
- **Professional Quality**: Multi-stage review process ensures high-quality, polished content

## 🚀 Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your API keys:**
   - Copy `.env.example` to `.env`
   - Add your API keys to the `.env` file:
     ```
     OPENAI_API_KEY=sk-your-key-here
     SERPER_API_KEY=your-serper-api-key-here
     ```

3. **Run the program:**
   ```bash
   python main.py
   ```

## 🔍 Web Search Integration

The Research Assistant now includes **real-time web search capabilities** using the Serper API:

- **Current Information**: Gathers the latest facts, statistics, and trends
- **News Integration**: Includes recent news and developments
- **Multiple Search Types**: General search, news search, and statistical data search
- **Source Citations**: Provides sources and links for better credibility

### Getting Serper API Key:
1. Visit [Serper.dev](https://serper.dev)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add it to your `.env` file

## 🔧 Monitoring Tool Usage

To verify that the web search tool is working and being used:

### Quick Check:
```bash
python web_search_monitor.py
```

### Test the Enhanced Researcher:
```bash
python test_researcher.py
```

### Real-time Monitoring:
The system includes comprehensive logging that shows:
- ✅ When web searches are initiated
- 📊 Number of results found
- 📰 News vs. general search activities
- ❌ Any API errors or issues
- 📈 Usage statistics

### Features for Tracking Tool Usage:
- **Console Logging**: Real-time search activities with emojis
- **Search Statistics**: Track total searches and timing
- **Usage Reports**: Historical data and session tracking
- **Error Monitoring**: Clear error messages for troubleshooting

## 🤖 Agent Architecture

The system includes seven specialized agents built with the OpenAI Agents SDK:

### 1. **Research Assistant** 🔍
- **Role**: Gathers comprehensive information and insights with real-time web search
- **Specialization**: Fact-finding, statistics, current information, news analysis
- **Features**: 
  - Real-time web search using Serper API
  - News integration for latest developments
  - Statistical data gathering
  - Source citations and links
- **Output**: Detailed research summary with current data

### 2. **SEO Keyword Expert**
- **Role**: Identifies SEO-relevant keywords and phrases
- **Specialization**: Keyword research, search optimization
- **Output**: Optimized keyword list

### 3. **Blog Trend Analyst**
- **Role**: Analyzes current trends and popular angles
- **Specialization**: Trend identification, content angles
- **Output**: Trending approaches and perspectives

### 4. **Blog Outline Creator**
- **Role**: Structures content in a logical format
- **Specialization**: Content organization, flow planning
- **Output**: Comprehensive blog outline

### 5. **Professional Blog Writer**
- **Role**: Creates engaging and informative content
- **Specialization**: Content creation, storytelling
- **Output**: Complete blog draft

### 6. **SEO Optimization Expert**
- **Role**: Optimizes content for search engines
- **Specialization**: On-page SEO, keyword integration
- **Output**: SEO-optimized content

### 7. **Professional Proofreader**
- **Role**: Ensures grammar, spelling, and style quality
- **Specialization**: Editorial review, final polish
- **Output**: Publication-ready blog post

## 📝 Usage

1. **Run the program:**
   ```bash
   python main.py
   ```

2. **Enter a blog topic** when prompted

3. **Watch the agents work** - The system will show progress as each agent completes their task:
   - 🔍 Researching topic
   - 🔑 Finding relevant keywords
   - 📈 Analyzing current trends
   - 📋 Creating content outline
   - ✍️ Writing blog content
   - 🔍 Optimizing for SEO
   - 📝 Final proofreading

4. **Get your blog post** - The final blog will be saved as a Markdown file in the `output/` directory

## 📁 Output

The system saves the final blog content to a Markdown file in the `output/` directory with automatic naming based on topic and timestamp (e.g., `blog_machine_learning_20250807_171345.md`).

## 🔧 OpenAI Agents SDK Benefits

### **Task Specialization**
- Each agent is configured with specific instructions for their role
- Better performance through focused expertise

### **Enhanced Error Handling**
- Robust error management and recovery
- Graceful handling of API issues

### **Better Context Management**
- Improved handling of conversation context
- More consistent agent behavior

### **Performance Optimization**
- Better resource utilization
- Optimized response times
- Asynchronous processing support

### **Tracing and Monitoring**
- Built-in tracing capabilities
- Agent performance monitoring
- Debugging support through OpenAI Dashboard

## 🛠 Technical Implementation

The system uses the OpenAI Agents SDK's `Agent` and `Runner` classes:

```python
from agents import Agent, Runner

# Create specialized agent
agent = Agent(
    name="Research Assistant",
    instructions="Detailed role-specific instructions..."
)

# Run agent with input
result = await Runner.run(agent, user_input)
```

Each agent is initialized with:
- **Name**: Descriptive agent identifier
- **Instructions**: Detailed role and behavior specifications
- **Specialized prompts**: Task-specific input formatting

## 📊 Workflow

```
Topic Input → Research Agent → Keyword Agent → Trend Agent → 
Outline Agent → Writer Agent → SEO Agent → Proofreader Agent → 
Final Blog Post
```

Each agent builds upon the previous agent's output, creating a comprehensive and professional blog post through collaborative AI intelligence.
