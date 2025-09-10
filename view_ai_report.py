#!/usr/bin/env python
import os
import sys
import django
import json
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chidmano.settings')
django.setup()

from store_analysis.models import AnalysisRequest

def view_ai_report():
    print("🤖 AI Analysis Report Viewer")
    print("=" * 60)
    
    # Get the latest analysis request
    latest_request = AnalysisRequest.objects.last()
    
    if not latest_request:
        print("❌ No analysis requests found")
        return
    
    print(f"📋 Analysis Request ID: {latest_request.id}")
    print(f"👤 User: {latest_request.order.user.username}")
    print(f"📊 Status: {latest_request.status}")
    print(f"📅 Created: {latest_request.created_at}")
    print(f"📅 Completed: {latest_request.completed_at}")
    
    if not latest_request.ai_analysis_results:
        print("\n❌ No AI analysis results available")
        return
    
    results = latest_request.ai_analysis_results
    
    print("\n" + "=" * 60)
    print("📊 AI ANALYSIS RESULTS")
    print("=" * 60)
    
    # Overall Score
    if 'overall_score' in results:
        score = results['overall_score']
        print(f"\n🎯 OVERALL SCORE: {score}/10")
        
        if score >= 8:
            print("🌟 Excellent - فروشگاه شما عملکرد عالی دارد!")
        elif score >= 6:
            print("✅ Good - فروشگاه شما عملکرد خوبی دارد")
        elif score >= 4:
            print("⚠️ Fair - نیاز به بهبود دارد")
        else:
            print("❌ Poor - نیاز به تغییرات اساسی دارد")
    
    # Advanced Analysis
    if 'advanced_analysis' in results:
        print(f"\n🔬 ADVANCED ANALYSIS")
        print("-" * 30)
        advanced = results['advanced_analysis']
        
        if 'score' in advanced:
            print(f"Score: {advanced['score']}/10")
        
        if 'insights' in advanced:
            print("\nKey Insights:")
            for i, insight in enumerate(advanced['insights'][:3], 1):
                print(f"  {i}. {insight}")
        
        if 'recommendations' in advanced:
            print("\nRecommendations:")
            for i, rec in enumerate(advanced['recommendations'][:3], 1):
                print(f"  {i}. {rec}")
    
    # Layout Analysis
    if 'layout_analysis' in results:
        print(f"\n🏗️ LAYOUT ANALYSIS")
        print("-" * 30)
        layout = results['layout_analysis']
        
        if 'score' in layout:
            print(f"Score: {layout['score']}/10")
        
        if 'strengths' in layout:
            print("\nStrengths:")
            for i, strength in enumerate(layout['strengths'][:3], 1):
                print(f"  {i}. {strength}")
        
        if 'weaknesses' in layout:
            print("\nAreas for Improvement:")
            for i, weakness in enumerate(layout['weaknesses'][:3], 1):
                print(f"  {i}. {weakness}")
    
    # Traffic Analysis
    if 'traffic_analysis' in results:
        print(f"\n🚶 TRAFFIC ANALYSIS")
        print("-" * 30)
        traffic = results['traffic_analysis']
        
        if 'score' in traffic:
            print(f"Score: {traffic['score']}/10")
        
        if 'patterns' in traffic:
            print("\nTraffic Patterns:")
            for i, pattern in enumerate(traffic['patterns'][:3], 1):
                print(f"  {i}. {pattern}")
    
    # Customer Behavior
    if 'customer_behavior' in results:
        print(f"\n👥 CUSTOMER BEHAVIOR")
        print("-" * 30)
        behavior = results['customer_behavior']
        
        if 'score' in behavior:
            print(f"Score: {behavior['score']}/10")
        
        if 'observations' in behavior:
            print("\nBehavioral Observations:")
            for i, obs in enumerate(behavior['observations'][:3], 1):
                print(f"  {i}. {obs}")
    
    # Key Insights
    if 'key_insights' in results:
        print(f"\n🔍 KEY INSIGHTS")
        print("-" * 30)
        insights = results['key_insights']
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight}")
    
    # Recommendations
    if 'recommendations' in results:
        print(f"\n💡 RECOMMENDATIONS")
        print("-" * 30)
        recommendations = results['recommendations']
        for i, rec in enumerate(recommendations[:10], 1):
            print(f"{i}. {rec}")
    
    # Store Data Summary
    print(f"\n📋 STORE DATA SUMMARY")
    print("-" * 30)
    store_data = latest_request.store_analysis_data
    
    print(f"Store Name: {store_data.get('store_name', 'N/A')}")
    print(f"Store Type: {store_data.get('store_type', 'N/A')}")
    print(f"Store Size: {store_data.get('store_size', 'N/A')}")
    print(f"Lighting Type: {store_data.get('lighting_type', 'N/A')}")
    print(f"Checkout Count: {store_data.get('checkout_count', 'N/A')}")
    print(f"Top Products: {store_data.get('top_selling_products', 'N/A')}")
    
    # Timestamp
    if 'timestamp' in results:
        print(f"\n⏰ Analysis Timestamp: {results['timestamp']}")
    
    print("\n" + "=" * 60)
    print("🏁 Report Complete!")

def list_all_reports():
    print("\n📋 ALL ANALYSIS REQUESTS")
    print("=" * 60)
    
    requests = AnalysisRequest.objects.all().order_by('-created_at')
    
    if not requests:
        print("❌ No analysis requests found")
        return
    
    for req in requests:
        print(f"\n📋 Request ID: {req.id}")
        print(f"👤 User: {req.order.user.username}")
        print(f"📊 Status: {req.status}")
        print(f"📅 Created: {req.created_at}")
        
        if req.ai_analysis_results:
            results = req.ai_analysis_results
            if 'overall_score' in results:
                print(f"🎯 Score: {results['overall_score']}/10")
            print("🤖 AI Results: ✅ Available")
        else:
            print("🤖 AI Results: ❌ Not available")

if __name__ == "__main__":
    print(f"🚀 AI Report Viewer at {datetime.now()}")
    
    # Show all reports first
    list_all_reports()
    
    # Show detailed report
    view_ai_report()
