# 🚗 Auto Insurance Claim Processor

An AI-powered auto insurance claim processing system built with Streamlit, LlamaIndex, and OpenAI. This application demonstrates advanced agentic workflows for parsing claims, retrieving policy information, and generating intelligent settlement recommendations.

## 🚀 Features

### Core Functionality
- **Web-based Interface**: Clean, intuitive Streamlit UI for claim processing
- **AI-Powered Analysis**: GPT-4 integration for intelligent claim evaluation
- **Policy Document Retrieval**: LlamaCloud integration for policy indexing and search
- **Structured Decision Making**: Comprehensive claim evaluation with detailed reasoning
- **Real-time Processing**: Asynchronous workflow with live progress tracking

### Advanced Capabilities
- **Event-Driven Workflow**: Multi-step processing pipeline with clear event handling
- **Policy Document Integration**: Automatic retrieval of relevant policy sections
- **Declarations Page Processing**: Individual policy holder information analysis
- **Metadata Filtering**: Policy-specific document retrieval and analysis
- **Comprehensive Logging**: Detailed processing steps with verbose mode

### Data Processing
- **Structured JSON Input**: Standardized claim data format
- **Pydantic Validation**: Type-safe data handling and validation
- **Multi-source Analysis**: Integration of claim data, policy documents, and declarations
- **Intelligent Querying**: AI-generated queries for relevant policy section retrieval

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: OpenAI GPT-4, LlamaIndex, LlamaCloud
- **Data Processing**: Pydantic, AsyncIO
- **Language**: Python 3.13+
- **Document Processing**: LlamaParse

## 📋 Installation

### Prerequisites
- Python 3.10 or higher
- OpenAI API key (optional, for AI features)
- LlamaCloud API key (optional, for document retrieval)

### Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd auto-insurance-claim-processor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional)
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export LLAMA_CLOUD_API_KEY="your-llama-cloud-api-key"
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Test the system** (optional)
   ```bash
   python demo.py
   ```

## 🎯 Usage

### Basic Usage
1. **Access the web interface** at `http://localhost:8501`
2. **Select a claim file** from the dropdown or upload your own JSON file
3. **Configure AI settings** in the sidebar (optional)
4. **Click "Process Claim"** to analyze the claim
5. **Review the results** including coverage decision, deductible, and recommended payout

### AI-Enhanced Mode
1. **Enable "Use Real AI Analysis"** in the sidebar
2. **Enter your API keys** for OpenAI and LlamaCloud
3. **Enable verbose mode** to see detailed processing steps
4. **Process claims** with full AI-powered analysis

## 📁 Project Structure

```
auto-insurance-claim-processor/
├── streamlit_app.py          # Main Streamlit application
├── workflow.py               # Core workflow and business logic
├── demo.py                   # Demo script for testing
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── .env.template            # Environment variables template
├── .gitignore              # Git ignore rules
├── data/                    # Sample data and claims
│   ├── john.json           # Sample claim: pizza delivery collision
│   ├── alice.json          # Sample claim: single vehicle accident
│   ├── john-declarations.md # Policy declarations for John
│   └── alice-declarations.md # Policy declarations for Alice
├── .streamlit/             # Streamlit configuration
│   └── config.toml         # App configuration
└── .idea/                  # IDE configuration (PyCharm/IntelliJ)
```

## 📊 Sample Data

### Claim Files
The application includes sample claim files demonstrating different scenarios:

**john.json** - Pizza delivery collision
- Claim involving commercial use (food delivery)
- Rear-end collision with parked vehicle
- Tests commercial use exclusions and endorsements

**alice.json** - Single vehicle accident
- Personal use vehicle
- Highway accident during adverse weather
- Standard collision coverage scenario

### Policy Declarations
Each claim includes corresponding policy declarations pages with:
- Coverage limits and deductibles
- Policy endorsements and exclusions
- Vehicle and policyholder information
- Premium and discount details

## 🔧 Configuration

### Workflow Settings
- **Verbose Mode**: Enable detailed logging of processing steps
- **AI Integration**: Toggle between mock and real AI analysis
- **Timeout Settings**: Configure processing timeout limits

### API Configuration
- **OpenAI**: GPT-4 model for intelligent claim analysis
- **LlamaCloud**: Document indexing and retrieval service
- **Environment Variables**: Secure API key management

## 🧪 Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
```bash
black .
flake8 .
```

### Type Checking
```bash
mypy workflow.py
```

## 📈 Workflow Architecture

The application follows an event-driven architecture with the following steps:

1. **Load Claim Info** → Parse and validate claim JSON data
2. **Generate Policy Queries** → AI-generated queries for policy retrieval
3. **Retrieve Policy Text** → Fetch relevant policy sections and declarations
4. **Generate Recommendation** → AI analysis of coverage and settlement
5. **Finalize Decision** → Structured output with coverage determination
6. **Output Result** → Format and display results to user

## 🔮 Future Enhancements

- **Batch Processing**: Handle multiple claims simultaneously
- **Advanced Analytics**: Claim pattern analysis and reporting
- **Integration APIs**: REST API for external system integration
- **Multi-language Support**: Internationalization capabilities
- **Advanced Visualizations**: Interactive charts and claim analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LlamaIndex](https://www.llamaindex.ai/) for document processing
- Powered by [OpenAI](https://openai.com/) for intelligent analysis
- UI created with [Streamlit](https://streamlit.io/)
- Inspired by the LlamaIndex Auto Insurance Tutorial

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Check the documentation
- Review sample implementations

---

**🚗 Drive safe, claim smart!**
