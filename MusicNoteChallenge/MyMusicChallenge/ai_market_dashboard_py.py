import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="AI Market Dynamics Predictor",
    page_icon="🤖",
    layout="wide"
)

# Title and description
st.title("🤖 AI Market Dynamics Predictor")
st.markdown("""
            *Explore how competing variables shape the future of the AI landscape*
            
            Note: This is not scientific AT ALL, with NO attempt to properly scale the arguments.
            It's just a deliberately crude attempt to explore different variables in relation to each other.
            Undoubtedly, there are missing variables too.
            """)

# Create columns for layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📊 Market Variables")
    
    # Sliders for the four key variables
    cost = st.slider(
        "💰 Cost of Running AI",
        min_value=0,
        max_value=100,
        value=90,  # Very high starting point
        help="How expensive is it to run AI systems (infrastructure, compute, talent)"
    )
    
    value = st.slider(
        "💎 Value Derived from AI",
        min_value=0,
        max_value=100,
        value=20,  # Low starting point
        help="How much value do customers actually get from AI solutions"
    )
    
    price = st.slider(
        "💵 Price Charged for AI",
        min_value=0,
        max_value=100,
        value=15,  # Low starting point
        help="How much companies can charge customers for AI services"
    )
    
    quality = st.slider(
        "⭐ Quality of AI",
        min_value=0,
        max_value=100,
        value=85,  # High starting point
        help="How good/reliable/accurate are current AI systems"
    )
    
    employment_impact = st.slider(
        "👥 Employment Impact",
        min_value=0,
        max_value=100,
        value=70,  # High negative impact starting point
        help="Employment disruption (0=job creation, 50=neutral, 100=massive job losses)"
    )

with col2:
    st.header("📈 Current Metrics")
    
    # Calculate key metrics
    profit_margin = price - cost
    value_to_price_ratio = value / price if price > 0 else 0
    quality_to_cost_ratio = quality / cost if cost > 0 else 0
    employment_disruption = employment_impact  # Higher = more negative
    
    # Display metrics with color coding
    col2a, col2b = st.columns(2)
    
    with col2a:
        # Profit Margin - Green if positive, Red if negative
        if profit_margin > 0:
            st.success(f"💰 **Profit Margin**: {profit_margin:.1f} (Profitable)")
        else:
            st.error(f"💸 **Profit Margin**: {profit_margin:.1f} (Loss-making)")
        
        # Value/Price Ratio - Green if >1, Red if ≤1
        if value_to_price_ratio > 1:
            st.success(f"💎 **Value/Price Ratio**: {value_to_price_ratio:.2f}x (Good deal)")
        else:
            st.error(f"💔 **Value/Price Ratio**: {value_to_price_ratio:.2f}x (Poor value)")
    
    with col2b:
        # Quality/Cost Ratio - Green if >1 (efficient), Red if ≤1 (inefficient)
        if quality_to_cost_ratio > 1:
            st.success(f"⚡ **Quality/Cost Ratio**: {quality_to_cost_ratio:.2f}x (Efficient)")
        else:
            st.error(f"🐌 **Quality/Cost Ratio**: {quality_to_cost_ratio:.2f}x (Inefficient)")
        
        # Employment Impact - Green if <40 (job creation), Yellow if 40-60 (neutral), Red if >60 (job losses)
        if employment_disruption < 40:
            st.success(f"📈 **Employment Impact**: {employment_disruption:.0f} (Job creation)")
        elif employment_disruption < 60:
            st.warning(f"⚖️ **Employment Impact**: {employment_disruption:.0f} (Neutral)")
        else:
            st.error(f"📉 **Employment Impact**: {employment_disruption:.0f} (Job displacement)")
    
    # Sustainability score calculation
    sustainability = (profit_margin + value_to_price_ratio * 20 + quality_to_cost_ratio * 10) / 3
    
    # Show sustainability calculation
    st.markdown("### 🧮 Sustainability Calculation")
    st.code(f"""
Sustainability = (Profit Margin + Value/Price Ratio × 20 + Quality/Cost Ratio × 10) ÷ 3
              = ({profit_margin:.1f} + {value_to_price_ratio:.2f} × 20 + {quality_to_cost_ratio:.2f} × 10) ÷ 3
              = {sustainability:.1f}
    """)
    
    if sustainability >= 0:
        st.success(f"📈 **Overall Sustainability**: {sustainability:.1f} (Sustainable)")
    else:
        st.error(f"📉 **Overall Sustainability**: {sustainability:.1f} (Unsustainable)")

# Big prediction button
st.markdown("---")
if st.button("🔮 PREDICT THE FUTURE", type="primary", use_container_width=True):
    
    def generate_prediction(cost, value, price, quality, employment_impact):
        # Calculate key metrics
        profit_margin = price - cost
        value_to_price_ratio = value / price if price > 0 else 0
        quality_to_cost_ratio = quality / cost if cost > 0 else 0
        sustainability = (profit_margin + value_to_price_ratio * 20 + quality_to_cost_ratio * 10) / 3
        employment_disruption = employment_impact
        
        # Determine primary outcome
        if sustainability < -20:
            outcome = "🔥 Market Collapse Imminent"
            reasoning = "The fundamental economics are catastrophically broken. "
        elif sustainability < -10:
            outcome = "💀 Mass AI Company Extinction"
            reasoning = "Current business models are completely unsustainable. "
        elif sustainability < 0:
            outcome = "⚠️ Industry Consolidation Crisis"
            reasoning = "Only the largest players with deep pockets will survive. "
        elif sustainability < 10:
            outcome = "🤔 Precarious Equilibrium"
            reasoning = "The market is barely holding together. "
        elif sustainability < 20:
            outcome = "📈 Cautious Optimism"
            reasoning = "Signs of a sustainable business model are emerging. "
        elif sustainability < 30:
            outcome = "🚀 AI Boom Incoming"
            reasoning = "Strong fundamentals suggest rapid growth ahead. "
        else:
            outcome = "🌟 AI Utopia Achieved"
            reasoning = "Perfect market conditions for explosive AI adoption. "
        
        # Add specific insights based on variables
        insights = []
        
        # Cost analysis
        if cost > 80:
            insights.append("🔥 **Critical Cost Crisis**: Infrastructure costs are crushing profit margins. Expect massive investments in efficiency or market exit.")
        elif cost > 60:
            insights.append("💸 **High Cost Pressure**: Companies are burning cash fast. Only those with strong unit economics will survive.")
        elif cost > 40:
            insights.append("⚖️ **Moderate Cost Burden**: Manageable but requires careful optimization.")
        else:
            insights.append("✅ **Cost Advantage**: Low operational costs enable competitive pricing and healthy margins.")
        
        # Value analysis
        if value > 80:
            insights.append("💎 **High Value Delivery**: Customers see massive ROI. This creates strong demand and pricing power.")
        elif value > 60:
            insights.append("📊 **Solid Value Proposition**: Clear benefits justify AI investments.")
        elif value > 40:
            insights.append("🤷 **Questionable Value**: Some benefits but customers remain skeptical.")
        else:
            insights.append("❌ **Value Crisis**: Customers can't justify AI spending. Expect demand collapse.")
        
        # Price analysis
        if price > 80:
            insights.append("💰 **Premium Pricing**: High prices either reflect strong value or market bubble.")
        elif price > 60:
            insights.append("💵 **Healthy Pricing**: Good balance between accessibility and profitability.")
        elif price > 40:
            insights.append("🏷️ **Competitive Pricing**: Moderate prices to drive adoption.")
        else:
            insights.append("🔥 **Race to the Bottom**: Unsustainably low prices destroying industry profits.")
        
        # Quality analysis
        if quality > 80:
            insights.append("⭐ **Exceptional Quality**: AI systems deliver reliable, impressive results.")
        elif quality > 60:
            insights.append("✅ **Good Quality**: Systems work well for most use cases.")
        elif quality > 40:
            insights.append("⚠️ **Inconsistent Quality**: Results are hit-or-miss, limiting adoption.")
        else:
            insights.append("💥 **Quality Crisis**: Poor AI performance is destroying customer trust.")
        
        # Employment impact analysis
        if employment_disruption > 80:
            insights.append("🚨 **Employment Catastrophe**: Massive job displacement causing social unrest and political backlash.")
        elif employment_disruption > 60:
            insights.append("⚠️ **Significant Job Displacement**: Major employment disruption in multiple sectors.")
        elif employment_disruption > 40:
            insights.append("⚖️ **Employment Transition**: Moderate job displacement balanced by new opportunities.")
        elif employment_disruption > 20:
            insights.append("📈 **Job Market Shift**: Some displacement but strong new job creation.")
        else:
            insights.append("🌟 **Employment Boom**: AI creating more jobs than it eliminates.")
        
        # Market dynamics
        if profit_margin > 20:
            insights.append("📈 **Healthy Margins**: Strong profitability attracts new entrants and investment.")
        elif profit_margin > 0:
            insights.append("💼 **Thin Margins**: Barely profitable, vulnerable to market shifts.")
        elif profit_margin > -20:
            insights.append("📉 **Burning Cash**: Unsustainable losses require rapid improvement or exit.")
        else:
            insights.append("🚨 **Financial Disaster**: Catastrophic losses will bankrupt most companies.")
        
        # Future timeline
        if sustainability > 15:
            timeline = "**Next 6-12 months**: Rapid market expansion and new player entry."
        elif sustainability > 0:
            timeline = "**Next 1-2 years**: Gradual market maturation with selective growth."
        elif sustainability > -10:
            timeline = "**Next 6-18 months**: Significant market consolidation and company failures."
        else:
            timeline = "**Next 3-6 months**: Industry-wide crisis and potential market collapse."
        
        return outcome, reasoning, insights, timeline
    
    # Generate and display prediction
    outcome, reasoning, insights, timeline = generate_prediction(cost, value, price, quality, employment_impact)
    
    st.markdown("## 🔮 Market Prediction")
    st.markdown(f"### {outcome}")
    st.write(reasoning)
    
    st.markdown("### 📋 Key Insights")
    for insight in insights:
        st.markdown(f"- {insight}")
    
    st.markdown("### ⏰ Timeline")
    st.markdown(timeline)
    
    # Risk factors
    st.markdown("### 🚨 Key Risk Factors")
    risk_factors = []
    
    if cost > 70 and price < 30:
        risk_factors.append("**Profit Squeeze**: High costs with low prices create unsustainable unit economics")
    
    if value < 30 and price > 50:
        risk_factors.append("**Value-Price Mismatch**: Customers won't pay high prices for low value")
    
    if quality < 40:
        risk_factors.append("**Quality Crisis**: Poor AI performance will destroy market confidence")
    
    if cost > 80 and quality < 60:
        risk_factors.append("**Efficiency Crisis**: High costs not delivering proportional quality")
    
    if len(risk_factors) == 0:
        st.success("No major risk factors detected in current configuration!")
    else:
        for risk in risk_factors:
            st.warning(risk)

# Sidebar with additional info
st.sidebar.header("ℹ️ About This Model")
st.sidebar.markdown("""
This dashboard models the AI market using five key variables:

**Cost**: Infrastructure, compute, talent, and operational expenses

**Value**: Actual benefits customers receive from AI solutions

**Price**: What companies can charge for AI services

**Quality**: Reliability, accuracy, and effectiveness of AI systems

**Employment Impact**: Job displacement vs creation (0=job creation, 100=massive losses)

The sustainability model weighs profit margins, value delivery, and operational efficiency to predict market viability.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("*Adjust the sliders and click 'Predict the Future' to explore different scenarios!*")