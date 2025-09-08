#!/usr/bin/env python3
"""
FinOps Agent CLI

Command-line interface for the FinOps agent system.
See PROJECT_DOCUMENTATION.md for complete project information.
"""

import click
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from lib import (
    get_config, create_initial_state, create_scanner_graph, create_cost_analyzer_graph, create_optimizer_graph,
    setup_logging, format_currency, format_duration
)
from lib.agents.reporter import create_reporter_workflow
from lib.state import FinOpsAgentState
from lib.utils import generate_uuid


@click.group()
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.option('--log-level', default='INFO', help='Log level (DEBUG, INFO, WARNING, ERROR)')
def cli(debug: bool, log_level: str):
    """FinOps Agent - Azure Cloud Cost Optimization Tool"""
    # Setup logging
    if debug:
        log_level = 'DEBUG'
    setup_logging(log_level)
    
    # Validate configuration
    try:
        config = get_config()
        if not config.validate():
            click.echo("❌ Configuration validation failed. Check your environment variables.")
            sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Configuration error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--output', '-o', help='Output file path for scan results')
@click.option('--limit', default=50, help='Maximum number of resources to scan')
def scan(output: str, limit: int):
    """Scan Azure resources and analyze infrastructure"""
    click.echo("🔍 Starting Azure resource scan...")
    
    try:
        # Get configuration
        config = get_config()
        
        # Create initial state
        state = create_initial_state(
            session_id=generate_uuid(),
            subscription_id=config.azure.subscription_id,
            tenant_id=config.azure.tenant_id
        )
        
        click.echo(f"📋 Session ID: {state.session_id}")
        click.echo(f"🔑 Subscription: {config.azure.subscription_id}")
        click.echo(f"🏢 Tenant: {config.azure.tenant_id}")
        
        # Create and run scanner graph
        graph = create_scanner_graph()
        result = graph.invoke(state)
        
        # Handle result
        if hasattr(result, 'scan_history'):
            final_state = result
        else:
            from lib.state import load_state_from_dict
            final_state = load_state_from_dict(result)
        
        # Display results
        if final_state.scan_history:
            latest_scan = final_state.scan_history[-1]
            click.echo(f"\n✅ Scan completed successfully!")
            click.echo(f"   📊 Resources found: {latest_scan.resources_found}")
            click.echo(f"   ⏱️  Duration: {format_duration(latest_scan.scan_duration_seconds)}")
            click.echo(f"   📍 Location: {latest_scan.subscription_id}")
            
            # Resource breakdown
            resource_types = {}
            for resource in latest_scan.resources:
                resource_types[resource.type.value] = resource_types.get(resource.type.value, 0) + 1
            
            click.echo(f"\n📋 Resource Breakdown:")
            for resource_type, count in resource_types.items():
                click.echo(f"   {resource_type}: {count}")
            
            # Save to file if requested
            if output:
                from lib.state import save_state_to_file
                save_state_to_file(final_state, output)
                click.echo(f"\n💾 Results saved to: {output}")
        
        # Show any errors or warnings
        if final_state.errors:
            click.echo(f"\n⚠️  Errors encountered: {len(final_state.errors)}")
            for error in final_state.errors[-3:]:  # Show last 3 errors
                click.echo(f"   {error}")
        
        if final_state.warnings:
            click.echo(f"\n⚠️  Warnings: {len(final_state.warnings)}")
            for warning in final_state.warnings[-3:]:  # Show last 3 warnings
                click.echo(f"   {warning}")
                
    except Exception as e:
        click.echo(f"❌ Scan failed: {e}")
        sys.exit(1)


@cli.command()
@click.option('--output', '-o', help='Output file path for analysis results')
def analyze(output: str):
    """Analyze costs for scanned Azure resources"""
    click.echo("💰 Starting Azure cost analysis...")
    
    try:
        # Get configuration
        config = get_config()
        
        # Create initial state
        state = create_initial_state(
            session_id=generate_uuid(),
            subscription_id=config.azure.subscription_id,
            tenant_id=config.azure.tenant_id
        )
        
        click.echo(f"📋 Session ID: {state.session_id}")
        click.echo(f"🔑 Subscription: {config.azure.subscription_id}")
        click.echo(f"🏢 Tenant: {config.azure.tenant_id}")
        
        # First run a scan to get resources
        click.echo("\n🔍 Running resource scan first...")
        scanner_graph = create_scanner_graph()
        state = scanner_graph.invoke(state)
        
        # Handle scanner result
        if hasattr(state, 'scan_history'):
            scanner_state = state
        else:
            from lib.state import load_state_from_dict
            scanner_state = load_state_from_dict(state)
        
        if not scanner_state.scan_history:
            click.echo("❌ No resources found. Cannot analyze costs.")
            sys.exit(1)
        
        click.echo(f"✅ Found {len(scanner_state.scan_history[-1].resources)} resources")
        
        # Now run cost analysis
        click.echo("\n💰 Running cost analysis...")
        analyzer_graph = create_cost_analyzer_graph()
        result = analyzer_graph.invoke(scanner_state)
        
        # Handle analyzer result
        if hasattr(result, 'analysis_history'):
            final_state = result
        else:
            from lib.state import load_state_from_dict
            final_state = load_state_from_dict(result)
        
        # Display results
        if final_state.analysis_history:
            latest_analysis = final_state.analysis_history[-1]
            click.echo(f"\n✅ Cost analysis completed successfully!")
            click.echo(f"   💰 Total cost: {format_currency(latest_analysis.total_cost_usd)}")
            click.echo(f"   📊 Resources analyzed: {len(scanner_state.scan_history[-1].resources)}")
            click.echo(f"   ⏱️  Duration: {format_duration(latest_analysis.analysis_duration_seconds)}")
            
            # Cost breakdown
            click.echo(f"\n💰 Cost Breakdown:")
            for resource_type, cost in latest_analysis.cost_breakdown.items():
                click.echo(f"   {resource_type}: {format_currency(cost)}")
            
            # High-cost resources
            if latest_analysis.high_cost_resources:
                click.echo(f"\n💸 High-Cost Resources (>$100/month):")
                for cost_data in latest_analysis.high_cost_resources[:5]:  # Show top 5
                    click.echo(f"   {cost_data.resource_name}: {format_currency(cost_data.cost_usd)}")
            
            # Cost anomalies
            if latest_analysis.cost_anomalies:
                click.echo(f"\n⚠️  Cost Anomalies:")
                for anomaly in latest_analysis.cost_anomalies:
                    click.echo(f"   {anomaly['resource_name']}: {format_currency(anomaly['cost_usd'])} - {anomaly['reason']}")
            
            # Save to file if requested
            if output:
                from lib.state import save_state_to_file
                save_state_to_file(final_state, output)
                click.echo(f"\n💾 Results saved to: {output}")
        
        # Show any errors or warnings
        if final_state.errors:
            click.echo(f"\n⚠️  Errors encountered: {len(final_state.errors)}")
            for error in final_state.errors[-3:]:  # Show last 3 errors
                click.echo(f"   {error}")
        
        if final_state.warnings:
            click.echo(f"\n⚠️  Warnings: {len(final_state.warnings)}")
            for warning in final_state.warnings[-3:]:  # Show last 3 warnings
                click.echo(f"   {warning}")
                
    except Exception as e:
        click.echo(f"❌ Analysis failed: {e}")
        sys.exit(1)


@cli.command()
@click.option('--output', '-o', help='Output file path for optimization results')
def optimize(output: str):
    """Generate cost optimization recommendations for scanned resources"""
    click.echo("🎯 Starting Azure cost optimization analysis...")
    
    try:
        # Get configuration
        config = get_config()
        
        # Create initial state
        state = create_initial_state(
            session_id=generate_uuid(),
            subscription_id=config.azure.subscription_id,
            tenant_id=config.azure.tenant_id
        )
        
        click.echo(f"📋 Session ID: {state.session_id}")
        click.echo(f"🔑 Subscription: {config.azure.subscription_id}")
        click.echo(f"🏢 Tenant: {config.azure.tenant_id}")
        
        # First run a scan to get resources
        click.echo("\n🔍 Running resource scan first...")
        scanner_graph = create_scanner_graph()
        state = scanner_graph.invoke(state)
        
        # Handle scanner result
        if hasattr(state, 'scan_history'):
            scanner_state = state
        else:
            from lib.state import load_state_from_dict
            scanner_state = load_state_from_dict(state)
        
        if not scanner_state.scan_history:
            click.echo("❌ No resources found. Cannot generate optimizations.")
            sys.exit(1)
        
        click.echo(f"✅ Found {len(scanner_state.scan_history[-1].resources)} resources")
        
        # Now run cost analysis
        click.echo("\n💰 Running cost analysis...")
        analyzer_graph = create_cost_analyzer_graph()
        state = analyzer_graph.invoke(scanner_state)
        
        # Handle analyzer result
        if hasattr(state, 'analysis_history'):
            analyzer_state = state
        else:
            from lib.state import load_state_from_dict
            analyzer_state = load_state_from_dict(state)
        
        if not analyzer_state.analysis_history:
            click.echo("❌ No cost analysis found. Cannot generate optimizations.")
            sys.exit(1)
        
        click.echo(f"✅ Cost analysis completed")
        
        # Now run optimization analysis
        click.echo("\n🎯 Running optimization analysis...")
        optimizer_graph = create_optimizer_graph()
        result = optimizer_graph.invoke(analyzer_state)
        
        # Handle optimizer result
        if hasattr(result, 'recommendations'):
            final_state = result
        else:
            from lib.state import load_state_from_dict
            final_state = load_state_from_dict(result)
        
        # Display results
        if final_state.recommendations:
            click.echo(f"\n✅ Optimization analysis completed successfully!")
            click.echo(f"   💡 Recommendations generated: {len(final_state.recommendations)}")
            click.echo(f"   💰 Total potential savings: {format_currency(final_state.get_total_savings_potential())}")
            
            # Show top recommendations
            click.echo(f"\n💡 Top Optimization Recommendations:")
            for i, rec in enumerate(final_state.recommendations[:5], 1):
                click.echo(f"\n   {i}. {rec.title}")
                click.echo(f"      💰 Potential savings: {format_currency(rec.estimated_savings_usd)}/month")
                click.echo(f"      📊 Priority: {rec.priority.value.upper()}")
                click.echo(f"      🔧 Effort: {rec.implementation_effort}")
                click.echo(f"      📝 Description: {rec.description}")
                
                if rec.implementation_steps:
                    click.echo(f"      📋 Steps:")
                    for step in rec.implementation_steps[:3]:  # Show first 3 steps
                        click.echo(f"         {step}")
                    if len(rec.implementation_steps) > 3:
                        click.echo(f"         ... and {len(rec.implementation_steps) - 3} more steps")
            
            # Show high priority recommendations
            high_priority = final_state.get_high_priority_recommendations()
            if high_priority:
                click.echo(f"\n🚨 High Priority Recommendations ({len(high_priority)}):")
                for rec in high_priority[:3]:
                    click.echo(f"   • {rec.title}: {format_currency(rec.estimated_savings_usd)} savings")
            
            # Save to file if requested
            if output:
                from lib.state import save_state_to_file
                save_state_to_file(final_state, output)
                click.echo(f"\n💾 Results saved to: {output}")
        else:
            click.echo(f"\n✅ Optimization analysis completed!")
            click.echo(f"   💡 No optimization opportunities found")
            click.echo(f"   💰 Your resources are already well-optimized!")
        
        # Show any errors or warnings
        if final_state.errors:
            click.echo(f"\n⚠️  Errors encountered: {len(final_state.errors)}")
            for error in final_state.errors[-3:]:  # Show last 3 errors
                click.echo(f"   {error}")
        
        if final_state.warnings:
            click.echo(f"\n⚠️  Warnings: {len(final_state.warnings)}")
            for warning in final_state.warnings[-3:]:  # Show last 3 warnings
                click.echo(f"   {warning}")
                
    except Exception as e:
        click.echo(f"❌ Optimization failed: {e}")
        sys.exit(1)


@cli.command()
def status():
    """Show current FinOps agent status and configuration"""
    try:
        config = get_config()
        
        click.echo("🔧 FinOps Agent Status")
        click.echo("=" * 40)
        
        click.echo(f"📋 Version: {getattr(config, '__version__', '0.1.0')}")
        click.echo(f"🔑 Subscription: {config.azure.subscription_id}")
        click.echo(f"🏢 Tenant: {config.azure.tenant_id}")
        click.echo(f"🌐 Azure OpenAI Endpoint: {config.azure_openai.endpoint}")
        click.echo(f"🤖 Model: {config.azure_openai.deployment_name}")
        click.echo(f"⚙️  Debug Mode: {config.app.debug}")
        click.echo(f"📝 Log Level: {config.app.log_level}")
        click.echo(f"🔄 Max Retries: {config.app.max_retries}")
        click.echo(f"⏱️  Timeout: {config.app.timeout_seconds}s")
        
        # Test connections
        click.echo("\n🔍 Testing Connections...")
        
        from lib.auth import test_azure_connection
        if test_azure_connection():
            click.echo("✅ All connections successful!")
        else:
            click.echo("❌ Some connections failed")
            
    except Exception as e:
        click.echo(f"❌ Status check failed: {e}")
        sys.exit(1)


@cli.command()
def config():
    """Show current configuration (without sensitive data)"""
    try:
        config = get_config()
        config_dict = config.to_dict()
        
        click.echo("⚙️  Current Configuration")
        click.echo("=" * 40)
        
        for section, values in config_dict.items():
            click.echo(f"\n{section.upper()}:")
            for key, value in values.items():
                click.echo(f"  {key}: {value}")
                
    except Exception as e:
        click.echo(f"❌ Configuration display failed: {e}")
        sys.exit(1)


@cli.command()
def version():
    """Show FinOps agent version"""
    click.echo("FinOps Agent v0.1.0")
    click.echo("Azure Cloud Cost Optimization Tool")


@cli.command()
def run_all():
    """Run complete FinOps analysis: scan → analyze → optimize → report"""
    try:
        click.echo("🚀 Starting Complete FinOps Analysis...")
        click.echo("=" * 50)
        
        # Get configuration and create initial state
        config = get_config()
        state = create_initial_state(
            session_id=generate_uuid(),
            subscription_id=config.azure.subscription_id,
            tenant_id=config.azure.tenant_id
        )
        
        # Step 1: Scan resources
        click.echo("\n🔍 Step 1/4: Scanning Azure resources...")
        scanner_workflow = create_scanner_graph()
        result = scanner_workflow.invoke(state)
        
        # Handle scanner result
        if hasattr(result, 'scan_history'):
            scanner_state = result
        else:
            from lib.state import load_state_from_dict
            scanner_state = load_state_from_dict(result)
        
        if not scanner_state.scan_history:
            click.echo("❌ Resource scanning failed")
            return
        
        click.echo(f"✅ Found {len(scanner_state.scan_history[-1].resources)} resources")
        
        # Step 2: Analyze costs
        click.echo("\n💰 Step 2/4: Analyzing costs...")
        cost_analyzer_workflow = create_cost_analyzer_graph()
        result = cost_analyzer_workflow.invoke(scanner_state)
        
        # Handle analyzer result
        if hasattr(result, 'analysis_history'):
            analyzer_state = result
        else:
            from lib.state import load_state_from_dict
            analyzer_state = load_state_from_dict(result)
        
        if not analyzer_state.analysis_history:
            click.echo("❌ Cost analysis failed")
            return
            
        click.echo(f"✅ Cost analysis completed: {format_currency(analyzer_state.analysis_history[-1].total_cost_usd)}")
        
        # Step 3: Generate optimizations
        click.echo("\n💡 Step 3/4: Generating optimization recommendations...")
        optimizer_workflow = create_optimizer_graph()
        result = optimizer_workflow.invoke(analyzer_state)
        
        # Handle optimizer result
        if hasattr(result, 'recommendations'):
            optimizer_state = result
        else:
            from lib.state import load_state_from_dict
            optimizer_state = load_state_from_dict(result)
        
        click.echo(f"✅ Generated {len(optimizer_state.recommendations)} recommendations")
        
        # Step 4: Generate reports
        click.echo("\n📊 Step 4/4: Generating comprehensive reports...")
        reporter_workflow = create_reporter_workflow()
        result = reporter_workflow.invoke(optimizer_state)
        
        # Handle reporter result
        if hasattr(result, 'reports'):
            final_state = result
        else:
            from lib.state import load_state_from_dict
            final_state = load_state_from_dict(result)
        
        click.echo("✅ Reports generated successfully")
        
        # Final summary
        click.echo("\n🎉 Complete FinOps Analysis Finished!")
        click.echo("=" * 50)
        click.echo(f"📊 Resources analyzed: {len(final_state.scan_history[-1].resources)}")
        click.echo(f"💰 Total monthly cost: {format_currency(final_state.analysis_history[-1].total_cost_usd)}")
        click.echo(f"💡 Recommendations: {len(final_state.recommendations)}")
        
        if final_state.reports:
            total_savings = sum(rec.estimated_savings_usd for rec in final_state.recommendations)
            click.echo(f"🎯 Potential savings: {format_currency(total_savings)}")
            click.echo(f"📁 Reports saved to: reports/{final_state.session_id}/")
        
        click.echo("\n💡 Next steps:")
        click.echo("   1. Review the generated reports")
        click.echo("   2. Implement high-priority recommendations")
        click.echo("   3. Set up cost monitoring")
        click.echo("   4. Schedule regular FinOps reviews")
        
    except Exception as e:
        click.echo(f"❌ Complete analysis failed: {e}")
        sys.exit(1)


@cli.command()
@click.option('--format', 'output_format', type=click.Choice(['json', 'html', 'csv', 'all']), 
              default='all', help='Output format for reports')
@click.option('--output-dir', default='reports', help='Output directory for reports')
def report(output_format: str, output_dir: str):
    """Generate comprehensive FinOps analysis reports"""
    try:
        click.echo("📊 Starting FinOps Report Generation...")
        
        # Load existing state or create new one
        config = get_config()
        state = create_initial_state(
            session_id=generate_uuid(),
            subscription_id=config.azure.subscription_id,
            tenant_id=config.azure.tenant_id
        )
        
        # Check if we have data to report on
        if not state.scan_history and not state.analysis_history and not state.recommendations:
            click.echo("⚠️  No analysis data found. Run 'scan', 'analyze', and 'optimize' first.")
            click.echo("💡 Tip: Run 'finops-cli run-all' to perform complete analysis")
            return
        
        # Create and run reporter workflow
        reporter_workflow = create_reporter_workflow()
        
        click.echo("🔍 Generating comprehensive reports...")
        result = reporter_workflow.invoke(state)
        
        # Display summary
        if result.reports:
            click.echo("\n✅ Report Generation Complete!")
            click.echo("=" * 50)
            
            # Executive Summary
            if "executive_summary" in result.reports:
                summary = result.reports["executive_summary"]
                click.echo(f"📊 Total Resources: {summary.get('overview', {}).get('total_resources', 'N/A')}")
                click.echo(f"💰 Monthly Cost: {summary.get('financial_impact', {}).get('total_monthly_cost_formatted', 'N/A')}")
                click.echo(f"💡 Potential Savings: {summary.get('recommendations_summary', {}).get('total_potential_savings_formatted', 'N/A')}")
            
            # Key Findings
            if "executive_summary" in result.reports and result.reports["executive_summary"].get("key_findings"):
                click.echo("\n🔍 Key Findings:")
                for finding in result.reports["executive_summary"]["key_findings"]:
                    click.echo(f"   • {finding}")
            
            # Recommendations Summary
            if "optimization_recommendations" in result.reports:
                opt_report = result.reports["optimization_recommendations"]
                click.echo(f"\n💡 Recommendations: {opt_report.get('summary', {}).get('total_recommendations', 0)}")
                click.echo(f"🎯 High Priority: {opt_report.get('summary', {}).get('high_priority_count', 0)}")
            
            # Action Items
            if "action_items" in result.reports:
                action_items = result.reports["action_items"]
                immediate_actions = len(action_items.get("immediate_actions", []))
                click.echo(f"\n🎯 Immediate Actions: {immediate_actions}")
                
                if immediate_actions > 0:
                    click.echo("   Top immediate actions:")
                    for action in action_items["immediate_actions"][:3]:
                        click.echo(f"   • {action['title']} - {action['estimated_savings_formatted']} savings")
            
            # File locations
            click.echo(f"\n📁 Reports saved to: {output_dir}/{result.session_id}/")
            click.echo("   📄 JSON: Complete data export")
            click.echo("   🌐 HTML: Executive summary")
            click.echo("   📊 CSV: Cost analysis data")
            
        else:
            click.echo("❌ No reports were generated")
            
    except Exception as e:
        click.echo(f"❌ Report generation failed: {e}")
        sys.exit(1)


@cli.command()
def docs():
    """Show documentation information"""
    click.echo("📚 FinOps Agent Documentation")
    click.echo("=" * 40)
    click.echo("📖 Complete project documentation: PROJECT_DOCUMENTATION.md")
    click.echo("🚀 Quick start: See Quick Start Guide section")
    click.echo("🔧 Development: See Development Workflow section")
    click.echo("🐛 Issues: See Troubleshooting section")
    click.echo("\n💡 Tip: Use '--help' with any command for detailed usage")


if __name__ == '__main__':
    cli()
