# FinOps Agent Suite

> AI-powered Azure cloud cost optimization tool that identifies $650+ monthly savings opportunities

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Azure](https://img.shields.io/badge/Azure-Cloud-orange.svg)](https://azure.microsoft.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-AI-green.svg)](https://langchain.com/langgraph)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-purple.svg)](https://openai.com)

## 🚀 Quick Start

```bash
# Clone and setup
git clone <your-repo-url>
cd finops-agent
uv sync

# Activate virtual environment (REQUIRED)
source .venv/bin/activate  # Linux/Mac
# or on Windows: .venv\Scripts\activate

# Run complete analysis
python finops_cli.py run-all
```

## ✨ Features

- 🔍 **Resource Scanning**: Azure Resource Graph integration (50+ resources in <2 seconds)
- 💰 **Cost Analysis**: Real Azure Cost Management API data (not estimates)
- 🤖 **AI Optimization**: GPT-4 powered recommendations with realistic savings
- 📊 **Professional Reports**: JSON, HTML, CSV outputs for stakeholders
- 🛡️ **Production Ready**: Comprehensive error handling and logging

## 📊 Results

| Metric | Value |
|--------|-------|
| **Resources Analyzed** | 50+ |
| **Analysis Time** | <60 seconds |
| **Total Monthly Cost** | $1,600+ |
| **Potential Savings** | $650+ (40%+) |
| **Recommendations** | 5 actionable insights |

## 🎯 Demo

```bash
# Run the professional demo
./demo.sh
```

**What the demo shows:**
- Complete Azure resource scanning
- Real cost data analysis
- AI-generated optimization recommendations
- Professional report generation
- Production-ready error handling

## 🏗️ Architecture

```
finops-agent/
├── lib/                    # Core library
│   ├── agents/            # LangGraph agent nodes
│   │   ├── scanner.py     # Resource scanner
│   │   ├── cost_analyzer.py # Cost analysis
│   │   ├── optimizer.py   # AI optimization
│   │   └── reporter.py    # Report generation
│   ├── config.py          # Configuration management
│   ├── auth.py            # Azure authentication
│   └── state.py           # State management
├── finops_cli.py          # Professional CLI
├── demo.sh               # Demo script
└── pyproject.toml        # Dependencies
```

## 🛠️ Technical Stack

- **LangGraph**: Multi-agent orchestration
- **Azure OpenAI**: GPT-4 for intelligent recommendations
- **Azure SDK**: Resource Graph & Cost Management APIs
- **Pydantic**: Data validation and serialization
- **Click**: Professional CLI framework

## 📋 Prerequisites

- Python 3.12+
- Azure subscription with Resource Graph access
- Azure OpenAI service deployed
- Service principal with appropriate permissions

## ⚙️ Configuration

Create `.env` file:

```bash
# Azure Configuration
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_SUBSCRIPTION_ID=your-subscription-id

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your-openai-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
```

## 🎮 Usage

### Complete Analysis
```bash
python finops_cli.py run-all
```

### Individual Agents
```bash
python finops_cli.py scan      # Scan resources
python finops_cli.py analyze   # Analyze costs
python finops_cli.py optimize  # Generate recommendations
python finops_cli.py report    # Generate reports
```

### Debug Mode
```bash
python finops_cli.py --debug run-all
```

## 📈 Output

The tool generates three types of reports:

- **📄 HTML Report**: Executive summary for stakeholders
- **📊 CSV Report**: Spreadsheet-compatible cost breakdown
- **🔍 JSON Report**: Complete data for programmatic analysis

## 🎯 Use Cases

### For Cloud Engineers
- Automated resource discovery and cost analysis
- AI-powered optimization recommendations
- Professional reporting for stakeholders

### For FinOps Teams
- Real-time cost optimization insights
- Automated cost anomaly detection
- Scalable cost management workflows

### For Portfolio/Interviews
- Demonstrates Azure integration expertise
- Shows AI/ML implementation skills
- Production-ready code quality

## 🔧 Development

### Setup Development Environment
```bash
git clone <your-repo>
cd finops-agent
uv sync
source .venv/bin/activate
```

### Run Tests
```bash
python finops_cli.py status  # Test connections
./demo.sh                    # Run complete demo
```

### Code Quality
- Type hints throughout
- Comprehensive error handling
- Professional logging
- Pydantic data validation

## 📚 Documentation

- [Complete Documentation](PROJECT_DOCUMENTATION.md) - Comprehensive project guide
- [CLI Help](finops_cli.py --help) - Command-line interface reference
- [Demo Script](demo.sh) - Professional demonstration

## 🚀 Performance

| Resource Count | Scan Time | Analysis Time | Total Time |
|----------------|-----------|---------------|------------|
| 10-50 resources | 1-2 seconds | 15-30 seconds | 20-35 seconds |
| 50-100 resources | 2-3 seconds | 30-60 seconds | 35-65 seconds |
| 100+ resources | 3-5 seconds | 60+ seconds | 65+ seconds |

## 🎉 Key Achievements

- ✅ **Real Azure Integration**: Uses actual Cost Management APIs, not estimates
- ✅ **AI-Powered Insights**: GPT-4 generates realistic, actionable recommendations
- ✅ **Production Ready**: Comprehensive error handling and professional logging
- ✅ **Scalable Architecture**: LangGraph multi-agent system
- ✅ **Professional Quality**: Clean code, type hints, comprehensive documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `./demo.sh`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangGraph](https://langchain.com/langgraph) for multi-agent orchestration
- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) for AI capabilities
- [Azure Cost Management](https://azure.microsoft.com/en-us/products/cost-management) for cost data

---

**FinOps Agent Suite** - Building the future of cloud cost optimization with AI 🚀

*Perfect for demonstrating Azure expertise, AI/ML skills, and production-ready development practices in job interviews and portfolio presentations.*
