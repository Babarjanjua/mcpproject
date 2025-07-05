# Multilingual Learning Path Generator

An agentic application that generates adaptive, multilingual study plans from MOOC catalogs, tracks progress, quizzes learners, and syncs to Google Classroom.

## 🚀 Features

- **Course Search & Recommendations**: Search across multiple MOOC platforms (edX, MIT OCW, etc.)
- **Multilingual Support**: Translate course content and interface
- **Adaptive Learning Paths**: Generate personalized study plans
- **Progress Tracking**: Monitor learning progress with analytics
- **Quiz Generation**: Create assessments based on course content
- **Google Classroom Integration**: Sync with Google Classroom
- **Learning Analytics**: AI-powered insights and recommendations

## 🏗️ Architecture

```
mcpproject/
├── backend/                 # FastAPI backend
│   ├── agents/             # LangGraph/LangChain agents
│   ├── api/                # API endpoints
│   ├── services/           # MCP client integrations
│   ├── db/                 # Database models
│   └── tests/              # Backend tests
├── frontend/               # Streamlit frontend
│   ├── components/         # UI components
│   ├── services/           # API calls
│   └── tests/              # Frontend tests
├── mcp_servers/            # MCP servers (external tools)
│   ├── mooc_server/        # Course search & details
│   ├── translation_server/ # Multilingual support
│   ├── classroom_server/   # Google Classroom sync
│   └── analytics_server/   # Learning analytics
└── config_mcp.json         # MCP server configuration
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Production-ready web framework
- **LangChain/LangGraph**: Agent orchestration
- **SQLAlchemy**: Database ORM
- **Pydantic**: Data validation

### Frontend
- **Streamlit**: Interactive web interface

### MCP Servers
- **FastMCP**: Model Context Protocol servers
- **External APIs**: MOOC platforms, translation services, Google Classroom

### Infrastructure
- **uv**: Fast Python package manager
- **SQLite**: Database (can be upgraded to PostgreSQL)
- **Docker**: Containerization (optional)

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mcpproject
   ```

2. **Install dependencies**
   ```bash
   uv pip install -r <(uv pip compile)
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the backend**
   ```bash
   uvicorn backend.main:app --reload
   ```

5. **Run the frontend**
   ```bash
   streamlit run frontend/app.py
   ```

## 🔧 Configuration

### MCP Servers

The application uses 4 MCP servers for external tool integration:

1. **MOOC Server** (`mcp_servers/mooc_server/`)
   - Course search across platforms
   - Course details and metadata
   - Integration with edX, MIT OCW, etc.

2. **Translation Server** (`mcp_servers/translation_server/`)
   - Text translation between languages
   - Language detection
   - Support for 10+ languages

3. **Classroom Server** (`mcp_servers/classroom_server/`)
   - Google Classroom integration
   - Course creation and management
   - Student enrollment and progress sync

4. **Analytics Server** (`mcp_servers/analytics_server/`)
   - Learning progress tracking
   - Personalized insights
   - Course recommendations

### API Endpoints

- `GET /courses` - Search and list courses
- `GET /courses/{course_id}` - Get course details
- `POST /learning-path` - Generate learning path
- `POST /progress` - Update learning progress
- `POST /quiz` - Generate quiz
- `POST /sync` - Sync with Google Classroom

## 🎯 Usage

### For Learners
1. Search for courses in your preferred language
2. Get personalized learning paths
3. Track your progress with analytics
4. Take quizzes to test knowledge
5. Sync progress with Google Classroom

### For Educators
1. Create courses in Google Classroom
2. Monitor student progress
3. Generate adaptive learning paths
4. Access learning analytics

## 🔌 API Integration

### Adding New MOOC Platforms
1. Update `mcp_servers/mooc_server/main.py`
2. Add API integration for the new platform
3. Update the course search logic

### Adding New Languages
1. Update `mcp_servers/translation_server/main.py`
2. Add language support to translation API
3. Update the supported languages list

## 🧪 Testing

```bash
# Run backend tests
pytest backend/tests/

# Run frontend tests
pytest frontend/tests/

# Run all tests
pytest
```

## 🚀 Deployment

### Local Development
```bash
# Backend
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
streamlit run frontend/app.py --server.port 8501
```

### Production Deployment
1. **Vercel**: Deploy FastAPI backend
2. **Streamlit Cloud**: Deploy frontend
3. **Database**: Use PostgreSQL for production
4. **MCP Servers**: Deploy as separate services

## 📊 Monitoring & Observability

- **Logging**: Structured logging with loguru
- **Tracing**: OpenTelemetry integration
- **Metrics**: Performance monitoring
- **Error Tracking**: Exception handling and reporting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Join our community discussions

## 🔮 Roadmap

- [ ] Real MOOC API integrations (edX, Coursera, Udemy)
- [ ] Advanced ML models for recommendations
- [ ] Mobile app development
- [ ] Multi-tenant architecture
- [ ] Advanced analytics dashboard
- [ ] Integration with more LMS platforms
