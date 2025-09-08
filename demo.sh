#!/bin/bash

# FinOps Agent Suite - Professional Demo Script
# This script demonstrates the complete Azure cost optimization workflow

set -e  # Exit on any error

echo "🚀 FinOps Agent Suite - Professional Demo"
echo "=========================================="
echo "📅 Date: $(date)"
echo "🎯 Purpose: Demonstrate Azure cost optimization with AI"
echo ""

# Check if we're in the right directory
if [ ! -f "finops_cli.py" ]; then
    echo "❌ Error: Please run this script from the finops-agent directory"
    echo "   Current directory: $(pwd)"
    echo "   Expected files: finops_cli.py, pyproject.toml"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Error: Virtual environment not found"
    echo "   Please run: uv sync"
    exit 1
fi

echo "✅ Environment check passed"
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Verify activation
if ! which python | grep -q "\.venv"; then
    echo "❌ Error: Virtual environment not activated correctly"
    echo "   Python path: $(which python)"
    exit 1
fi

echo "✅ Virtual environment activated"
echo "   Python path: $(which python)"
echo ""

# Check system status
echo "🔍 Checking system status..."
python finops_cli.py status
echo ""

# Create demo output directory
DEMO_DIR="./demo-$(date +%Y%m%d_%H%M%S)"
echo "📁 Creating demo output directory: $DEMO_DIR"
mkdir -p "$DEMO_DIR"

# Run complete analysis
echo "🚀 Running complete FinOps analysis..."
echo "   This will:"
echo "   - Scan Azure resources"
echo "   - Analyze costs with real Azure APIs"
echo "   - Generate AI-powered optimization recommendations"
echo "   - Create professional reports"
echo ""

# Run the analysis with progress indication
python finops_cli.py run-all 2>&1 | while IFS= read -r line; do
    echo "   $line"
done

# Copy existing reports to demo directory
echo "📊 Copying reports to demo directory..."
if [ -d "reports" ]; then
    # Find the most recent report directory
    LATEST_REPORT=$(find reports -type d -name "*" | sort | tail -1)
    if [ -n "$LATEST_REPORT" ]; then
        echo "   Copying from: $LATEST_REPORT"
        cp -r "$LATEST_REPORT"/* "$DEMO_DIR/" 2>/dev/null || true
        echo "   ✅ Reports copied successfully"
    else
        echo "   ⚠️  No reports found to copy"
    fi
else
    echo "   ⚠️  No reports directory found"
fi

echo ""
echo "🎉 Demo completed successfully!"
echo ""
echo "📊 Results Summary:"
echo "=================="

# Show results if they exist
if [ -d "$DEMO_DIR" ]; then
    echo "📁 Output directory: $DEMO_DIR"
    
    # Count files
    FILE_COUNT=$(find "$DEMO_DIR" -type f | wc -l)
    echo "📄 Files generated: $FILE_COUNT"
    
    # List files
    echo "📋 Generated files:"
    find "$DEMO_DIR" -type f -exec basename {} \; | sort | while read -r file; do
        echo "   - $file"
    done
    
    # Show file sizes
    echo ""
    echo "📏 File sizes:"
    find "$DEMO_DIR" -type f -exec ls -lh {} \; | awk '{print "   - " $9 ": " $5}'
    
    echo ""
    echo "🔍 Quick preview of results:"
    echo "============================"
    
    # Show JSON summary if available
    JSON_FILE=$(find "$DEMO_DIR" -name "finops_reports_*.json" | head -1)
    if [ -n "$JSON_FILE" ]; then
        echo "📊 Analysis Summary:"
        python -c "
import json
try:
    with open('$JSON_FILE', 'r') as f:
        data = json.load(f)
    
    # Extract key metrics
    total_cost = data.get('analysis_result', {}).get('total_monthly_cost', 0)
    resource_count = len(data.get('scan_result', {}).get('resources', []))
    recommendations = len(data.get('analysis_result', {}).get('optimization_recommendations', []))
    potential_savings = sum(rec.get('estimated_savings', 0) for rec in data.get('analysis_result', {}).get('optimization_recommendations', []))
    
    print(f'   💰 Total monthly cost: \${total_cost:,.2f}')
    print(f'   📊 Resources analyzed: {resource_count}')
    print(f'   💡 Optimization recommendations: {recommendations}')
    print(f'   💵 Potential monthly savings: \${potential_savings:,.2f}')
    if total_cost > 0:
        savings_percentage = (potential_savings / total_cost) * 100
        print(f'   📈 Savings percentage: {savings_percentage:.1f}%')
except Exception as e:
    print(f'   ⚠️  Could not parse results: {e}')
"
    fi
fi

echo ""
echo "🎯 Next Steps:"
echo "=============="
echo "1. 📖 Review the generated reports in: $DEMO_DIR"
echo "2. 📊 Open the HTML report for executive summary"
echo "3. 📈 Import CSV data into Excel/Google Sheets"
echo "4. 🔍 Use JSON data for programmatic analysis"
echo ""
echo "💡 This demo showcases:"
echo "   - Azure Resource Graph integration"
echo "   - Real Azure Cost Management API usage"
echo "   - AI-powered optimization recommendations"
echo "   - Professional report generation"
echo "   - Production-ready error handling"
echo ""
echo "🚀 FinOps Agent Suite - Building the future of cloud cost optimization with AI"
echo ""

# Deactivate virtual environment
deactivate
echo "✅ Demo script completed successfully!"
