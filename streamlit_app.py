import streamlit as st
import asyncio
import os
from workflow import AutoInsuranceWorkflow, ClaimDecision, parse_claim

st.set_page_config(
    page_title="Auto Insurance Claim Processor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚗 Auto Insurance Claim Processor")
st.markdown("### AI-Powered Claim Analysis & Settlement Recommendations")

# Sidebar Configuration
st.sidebar.header("⚙️ Configuration")

# API Key Configuration
use_real_ai = st.sidebar.checkbox(
    "Use Real AI Analysis",
    value=False,
    help="Enable this to use OpenAI GPT-4 and LlamaCloud for advanced analysis"
)

if use_real_ai:
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key for GPT-4 analysis"
    )
    
    llama_cloud_key = st.sidebar.text_input(
        "LlamaCloud API Key", 
        type="password",
        help="Enter your LlamaCloud API key for document retrieval"
    )
    
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key
    if llama_cloud_key:
        os.environ["LLAMA_CLOUD_API_KEY"] = llama_cloud_key

# Workflow Configuration
verbose_mode = st.sidebar.checkbox(
    "Verbose Mode",
    value=False,
    help="Show detailed processing steps"
)

# Initialize Workflow
@st.cache_resource
def initialize_workflow(use_ai: bool, verbose: bool):
    """Initialize the workflow with appropriate settings"""
    policy_retriever = None
    llm = None
    
    if use_ai and "OPENAI_API_KEY" in os.environ:
        try:
            from llama_index.llms.openai import OpenAI
            llm = OpenAI(model="gpt-4o")
            
            if "LLAMA_CLOUD_API_KEY" in os.environ:
                from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
                try:
                    index = LlamaCloudIndex(
                        name="auto_insurance_policies_0",
                        project_name="llamacloud_demo",
                    )
                    policy_retriever = index.as_retriever(rerank_top_n=3)
                    st.sidebar.success("✅ LlamaCloud connected")
                except Exception as e:
                    st.sidebar.warning(f"⚠️ LlamaCloud connection failed: {str(e)}")
            
            st.sidebar.success("✅ OpenAI connected")
        except Exception as e:
            st.sidebar.error(f"❌ AI initialization failed: {str(e)}")
    
    return AutoInsuranceWorkflow(
        policy_retriever=policy_retriever,
        llm=llm,
        verbose=verbose,
        timeout=None,
    )

workflow = initialize_workflow(use_real_ai, verbose_mode)

# Main Interface
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📄 Claim Processing")
    
    # File upload option
    uploaded_file = st.file_uploader(
        "Upload Claim JSON File",
        type=['json'],
        help="Upload a JSON file containing claim information"
    )
    
    # Or select from existing files
    claim_file_path = st.selectbox(
        "Or Select Existing Claim File",
        ["john.json", "alice.json"],
        help="Choose from sample claim files"
    )
    
    # Process button
    if st.button("🔍 Process Claim", type="primary"):
        try:
            # Determine which file to process
            if uploaded_file is not None:
                # Save uploaded file temporarily
                temp_path = f"data/temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                file_to_process = temp_path
            else:
                file_to_process = f"data/{claim_file_path}"
            
            # Show processing status
            with st.spinner("Processing claim..."):
                
                # Create a container for verbose output
                if verbose_mode:
                    verbose_container = st.expander("🔍 Processing Details", expanded=True)
                    with verbose_container:
                        progress_placeholder = st.empty()
                
                # Run Workflow
                async def run_workflow():
                    response_dict = await workflow.run(claim_json_path=file_to_process)
                    return response_dict["decision"]

                decision = asyncio.run(run_workflow())
            
            # Display Results
            st.success("✅ Claim processed successfully!")
            
            # Clean up temp file
            if uploaded_file is not None and os.path.exists(file_to_process):
                os.remove(file_to_process)

        except FileNotFoundError:
            st.error(f"❌ Error: Claim file '{claim_file_path}' not found in the 'data/' directory.")
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
            decision = None

with col2:
    st.subheader("📊 System Status")
    
    # System status indicators
    ai_status = "🟢 AI Enabled" if use_real_ai and "OPENAI_API_KEY" in os.environ else "🟡 Mock Mode"
    st.write(f"**Status:** {ai_status}")
    
    cloud_status = "🟢 Connected" if use_real_ai and "LLAMA_CLOUD_API_KEY" in os.environ else "🔴 Disconnected"
    st.write(f"**LlamaCloud:** {cloud_status}")
    
    st.write(f"**Verbose:** {'🟢 On' if verbose_mode else '🔴 Off'}")

# Display Decision Results
if 'decision' in locals() and decision:
    st.markdown("---")
    st.subheader("📋 Claim Decision")
    
    # Create result columns
    result_col1, result_col2, result_col3 = st.columns(3)
    
    with result_col1:
        st.metric(
            label="Coverage Status",
            value="COVERED" if decision.covered else "NOT COVERED",
            delta="Approved" if decision.covered else "Denied"
        )
    
    with result_col2:
        st.metric(
            label="Deductible",
            value=f"${decision.deductible:.2f}"
        )
    
    with result_col3:
        st.metric(
            label="Recommended Payout",
            value=f"${decision.recommended_payout:.2f}",
            delta=f"${decision.recommended_payout:.2f}" if decision.covered else "No payout"
        )
    
    # Detailed information
    st.subheader("📝 Details")
    
    details_col1, details_col2 = st.columns(2)
    
    with details_col1:
        st.write(f"**Claim Number:** {decision.claim_number}")
        st.write(f"**Coverage Decision:** {'✅ Covered' if decision.covered else '❌ Not Covered'}")
    
    with details_col2:
        st.write(f"**Deductible Amount:** ${decision.deductible:.2f}")
        st.write(f"**Settlement Amount:** ${decision.recommended_payout:.2f}")
    
    if decision.notes:
        st.subheader("💬 Analysis Notes")
        st.info(decision.notes)

# Instructions and Information
st.sidebar.markdown("---")
st.sidebar.header("📖 Instructions")
st.sidebar.markdown("""
### Quick Start
1. **Select a claim file** or upload your own
2. **Configure AI settings** (optional)
3. **Click 'Process Claim'** to analyze

### AI Features
- **GPT-4 Analysis**: Intelligent claim evaluation
- **LlamaCloud**: Policy document retrieval
- **Verbose Mode**: Detailed processing logs

### Sample Files
- `john.json`: Pizza delivery collision
- `alice.json`: Single vehicle accident

### File Format
```json
{
  "claim_number": "CLAIM-001",
  "policy_number": "POLICY-123",
  "claimant_name": "John Doe",
  "date_of_loss": "2025-06-20",
  "loss_description": "Vehicle damage",
  "estimated_repair_cost": 5000.00,
  "vehicle_details": "2022 Honda Civic"
}
```
""")

st.sidebar.markdown("---")
st.sidebar.markdown("**Powered by LlamaIndex & OpenAI**")
