# 🚗 Auto Insurance Claim Processor

An AI-powered auto insurance claim processing system built with Streamlit, LlamaIndex, and OpenAI. This application demonstrates advanced agentic workflows for parsing claims, retrieving policy information, and generating intelligent settlement recommendations.

## 🚀 Features

### Core Functionality
- **Web-based Interface**: Clean, intuitive Streamlit UI for claim processing
- **Agentic AI Reasoning**: Gemini 2.5 Flash orchestrates FNOL intelligence, triage, fraud scanning, and settlement drafting
- **Policy Document Retrieval**: (Optional) hook for LlamaCloud or local retrieval to ground coverage decisions
- **Structured Decision Making**: Comprehensive claim evaluation with detailed reasoning
- **Real-time Processing**: Asynchronous workflow with live progress tracking

### Advanced Capabilities
- **Event-Driven Workflow**: Multi-step processing pipeline with clear event handling
- **FNOL Intelligence Agent**: Summarizes intake narrative, severity, and next best actions
- **Smart Triage Agent**: Assigns adjusters, service levels, and workload routing
- **Fraud Radar Agent**: Generates SIU signals before settlement
- **Coverage Brain Agent**: Aligns policy sections, deductibles, and payouts
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
- **AI/ML**: Gemini 2.5 Flash (via Google Generative AI), LlamaIndex runtime, optional LlamaCloud for retrieval
- **Data Processing**: Pydantic, AsyncIO
- **Language**: Python 3.13+
- **Document Processing**: LlamaParse

## 📋 Installation

### Prerequisites
- Python 3.10 or higher
- OpenAI API key (optional, for AI features)
- LlamaCloud API key (optional, for document retrieval)

## 🧠 Agentic Opportunities Across The Claim Journey

| Journey Stage | Pain Today | Agentic Opportunity |
| --- | --- | --- |
| **FNOL Intake** | Free-form narratives require manual summarization | FNOL Intelligence agent normalizes facts, severity, and required evidence |
| **Triage & Assignment** | Work routing depends on adjuster experience | Smart Triage agent scores priority, matches adjuster persona, and sets SLA |
| **Investigation & Adjudication** | Policy lookup + fraud checks split across systems | Coverage Brain agent composes policy queries, while Fraud Radar agent pre-screens anomalies |
| **Settlement & Payout** | Decisions stored in static notes | Recommendation agent returns structured deductible/payout package for downstream systems |

## 🎯 MVP Scope & Prioritization

1. **FNOL Intelligence (Must-Have)** – unlocks instant understanding for every intake call, enabling downstream automation.
2. **Smart Triage (Must-Have)** – ensures carriers see value fast via better workload routing + SLA commitments.
3. **Fraud Radar (Should-Have)** – lightweight SIU signal that can plug into existing queues without new tooling.
4. **Coverage Brain (Must-Have)** – converts the above insights into actionable settlement instructions.

These four agents form the MVP because they touch every stakeholder: intake specialists, adjusters, SIU leads, and claims managers. Additional document retrieval integrations remain optional extensions.

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

3. **Set up environment variables**
   ```bash
   export GEMINI_API_KEY="your-google-ai-studio-key"
   # optional: export LLAMA_CLOUD_API_KEY for managed retrieval
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
3. **Optionally enable Gemini Agentic AI** with your API key for live reasoning
4. **Click "Process Claim"** to watch FNOL → Triage → Fraud → Settlement agents run
5. **Review the results** including coverage decision, deductible, recommended payout, severity, triage plan, and SIU signals

### Agentic Mode (Gemini)
1. **Enable "Use Gemini Agentic AI"** in the sidebar
2. **Enter your Google AI Studio key** (Gemini 2.5 Flash)
3. **Toggle verbose mode** to stream every workflow step
4. **Process claims** with live FNOL summaries, routing, fraud checks, and coverage reasoning

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

The event-driven workflow now mirrors the carrier journey:

1. **Load Claim Info** → Parse & validate FNOL JSON (Pydantic safeguards)
2. **FNOL Intelligence Agent** → Gemini summarizes incident, impact, severity, and next actions
3. **Smart Triage Agent** → Determines priority, adjuster persona, and target SLA
4. **Fraud Radar Agent** → Produces SIU risk score + flags
5. **Policy Query Agent** → Generates retrieval queries (or uses fallback library text)
6. **Coverage Brain** → Crafts deductible + payout recommendation tied to policy section
7. **Decision Formatter** → Surfaces claim decision alongside agentic insights in UI + API

Each agent falls back to deterministic heuristics when Gemini is unavailable, ensuring the prototype always runs.

## 🔮 Future Enhancements

- **Batch Processing**: Handle multiple claims simultaneously
- **Advanced Analytics**: Claim pattern analysis and reporting
- **Integration APIs**: REST API for external system integration
- **Multi-language Support**: Internationalization capabilities
- **Advanced Visualizations**: Interactive charts and claim analytics
- **Adjuster Co-Pilot**: Surface recommended questions and negotiation levers during live calls
- **Automated Repair Partnering**: Trigger DRP shop selection and digital payments

## 🖼️ Presentation Deck

A concise 5-slide briefing that covers agentic opportunities, MVP scope, product story, and next steps is available at `docs/presentation.md`.

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
