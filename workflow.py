import json
import asyncio
import os
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
    Context,
    Workflow,
    step
)
from llama_index.core.llms import LLM
from llama_index.core.prompts import ChatPromptTemplate
from llama_index.llms.openai import OpenAI
from llama_index.core.retrievers import BaseRetriever
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
from llama_index.core.vector_stores.types import (
    MetadataInfo,
    MetadataFilters,
)

# Comprehensive Schemas
class ClaimInfo(BaseModel):
    """Extracted Insurance claim information."""
    claim_number: str
    policy_number: str
    claimant_name: str
    date_of_loss: str
    loss_description: str
    estimated_repair_cost: float
    vehicle_details: Optional[str] = None

class PolicyQueries(BaseModel):
    queries: List[str] = Field(
        default_factory=list,
        description="A list of query strings to retrieve relevant policy sections."
    )

class PolicyRecommendation(BaseModel):
    """Policy recommendation regarding a given claim."""
    policy_section: str = Field(..., description="The policy section or clause that applies.")
    recommendation_summary: str = Field(..., description="A concise summary of coverage determination.")
    deductible: Optional[float] = Field(None, description="The applicable deductible amount.")
    settlement_amount: Optional[float] = Field(None, description="Recommended settlement payout.")

class ClaimDecision(BaseModel):
    claim_number: str
    covered: bool
    deductible: float
    recommended_payout: float
    notes: Optional[str] = None

# Enhanced Parsing Functions
def parse_claim(file_path: str) -> ClaimInfo:
    """Parse claim data from JSON file and validate with ClaimInfo schema"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Convert legacy format to new format if needed
        if 'damage_amount' in data:
            data['estimated_repair_cost'] = data.pop('damage_amount')
        if 'policyholder_name' in data:
            data['claimant_name'] = data.pop('policyholder_name')
        if 'date_of_incident' in data:
            data['date_of_loss'] = data.pop('date_of_incident')
        if 'description' in data:
            data['loss_description'] = data.pop('description')
            
        return ClaimInfo.model_validate(data)
    except FileNotFoundError:
        raise FileNotFoundError(f"Claim file not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Error parsing claim file {file_path}: {e}")

def get_declarations_docs(policy_retriever, policy_number: str, top_k: int = 1):
    """Get declarations documents for a specific policy number"""
    try:
        if hasattr(policy_retriever, 'retrieve'):
            # Use filters if available
            filters = MetadataFilters.from_dicts([
                {"key": "policy_number", "value": policy_number}
            ])
            docs = policy_retriever.retrieve(
                f"declarations page for {policy_number}",
                filters=filters
            )
            return docs[:top_k] if docs else []
        else:
            # Fallback for mock implementation
            return []
    except Exception as e:
        print(f"Warning: Could not retrieve declarations for {policy_number}: {e}")
        return []

# Event Classes
class ClaimInfoEvent(Event):
    claim_info: ClaimInfo

class PolicyQueryEvent(Event):
    queries: PolicyQueries

class PolicyMatchedEvent(Event):
    policy_text: str

class RecommendationEvent(Event):
    recommendation: PolicyRecommendation

class DecisionEvent(Event):
    decision: ClaimDecision

class LogEvent(Event):
    msg: str
    delta: bool = False

# Prompts
GENERATE_POLICY_QUERIES_PROMPT = """\
You are an assistant tasked with determining what insurance policy sections to consult for a given auto claim.

**Instructions:**
1. Review the claim data, including the type of loss, estimated repair cost, and policy number.
2. Identify what aspects of the policy we need:
   - Coverage conditions for the type of damage
   - Deductible application
   - Any special endorsements related to the incident
   - Exclusions that might apply
3. Produce 3-5 queries that can be used against a vector index of insurance policies to find relevant clauses.

Claim Data:
{claim_info}

Return a JSON object matching the PolicyQueries schema.
"""

POLICY_RECOMMENDATION_PROMPT = """\
Given the retrieved policy sections for this claim, determine:
- If the incident is covered under the policy
- The applicable deductible amount
- Recommended settlement amount (repair cost minus deductible if covered)
- Which specific policy section applies
- Any exclusions or special conditions

Claim Info:
{claim_info}

Policy Text:
{policy_text}

Return a JSON object matching PolicyRecommendation schema.
"""

# Advanced Auto Insurance Workflow
class AutoInsuranceWorkflow(Workflow):
    def __init__(
        self, 
        policy_retriever: Optional[BaseRetriever] = None, 
        llm: Optional[LLM] = None, 
        verbose: bool = False,
        timeout: Optional[float] = None,
        **kwargs
    ) -> None:
        super().__init__(verbose=verbose, timeout=timeout, **kwargs)
        self.policy_retriever = policy_retriever
        # Only initialize OpenAI if API key is available
        if llm:
            self.llm = llm
        elif os.getenv("OPENAI_API_KEY"):
            try:
                self.llm = OpenAI(model="gpt-4o")
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI LLM: {e}")
                self.llm = None
        else:
            self.llm = None
        self._verbose = verbose

    @step
    async def load_claim_info(self, ctx: Context, ev: StartEvent) -> ClaimInfoEvent:
        """Load and validate claim information from JSON file"""
        if self._verbose:
            ctx.write_event_to_stream(LogEvent(msg=">> Loading Claim Info"))
        
        claim_info = parse_claim(ev.claim_json_path)
        await ctx.set("claim_info", claim_info)
        
        if self._verbose:
            ctx.write_event_to_stream(LogEvent(msg=f">> Loaded claim: {claim_info.claim_number}"))
        
        return ClaimInfoEvent(claim_info=claim_info)

    @step
    async def generate_policy_queries(self, ctx: Context, ev: ClaimInfoEvent) -> PolicyQueryEvent:
        """Generate queries to retrieve relevant policy sections"""
        if self._verbose:
            ctx.write_event_to_stream(LogEvent(msg=">> Generating Policy Queries"))
        
        # Use LLM if available, otherwise generate basic queries
        if self.llm:
            try:
                prompt = ChatPromptTemplate.from_messages([("user", GENERATE_POLICY_QUERIES_PROMPT)])
                queries = await self.llm.astructured_predict(
                    PolicyQueries,
                    prompt,
                    claim_info=ev.claim_info.model_dump_json()
                )
            except Exception as e:
                if self._verbose:
                    ctx.write_event_to_stream(LogEvent(msg=f">> LLM query generation failed, using fallback: {e}"))
                queries = self._generate_fallback_queries(ev.claim_info)
        else:
            queries = self._generate_fallback_queries(ev.claim_info)
        
        if self._verbose:
            ctx.write_event_to_stream(LogEvent(msg=f">> Generated {len(queries.queries)} queries"))
        
        return PolicyQueryEvent(queries=queries)

    def _generate_fallback_queries(self, claim_info: ClaimInfo) -> PolicyQueries:
        """Generate basic queries when LLM is not available"""
        queries = [
            f"Coverage conditions for {claim_info.policy_number}",
            f"Deductible application for collision damage",
            f"Settlement amount calculation for vehicle damage",
            f"Exclusions for {claim_info.loss_description.lower()}",
            f"Policy limits and coverage details"
        ]
        return PolicyQueries(queries=queries)

    @step
    async def retrieve_policy_text(self, ctx: Context, ev: PolicyQueryEvent) -> PolicyMatchedEvent:
        """Retrieve relevant policy sections based on queries"""
        if self._verbose:
            ctx.write_event_to_stream(LogEvent(msg=">> Retrieving policy sections"))

        claim_info = await ctx.get("claim_info")
        combined_docs = {}
        
        if self.policy_retriever:
            try:
                for query in ev.queries.queries:
                    if self._verbose:
                        ctx.write_event_to_stream(LogEvent(msg=f">> Query: {query}"))
                    
                    # Fetch policy text
                    if hasattr(self.policy_retriever, 'aretrieve'):
                        docs = await self.policy_retriever.aretrieve(query)
                    else:
                        docs = self.policy_retriever.retrieve(query)
                    
                    for d in docs:
                        combined_docs[d.id_] = d

                # Try to fetch declarations page
                declarations_docs = get_declarations_docs(
                    self.policy_retriever, 
                    claim_info.policy_number
                )
                for d_doc in declarations_docs:
                    combined_docs[d_doc.id_] = d_doc
                    
            except Exception as e:
                if self._verbose:
                    ctx.write_event_to_stream(LogEvent(msg=f">> Policy retrieval failed: {e}"))
        
        if combined_docs:
            policy_text = "\n\n".join([doc.get_content() for doc in combined_docs.values()])
        else:
            # Fallback policy text for demo purposes
            policy_text = self._get_fallback_policy_text(claim_info)
        
        await ctx.set("policy_text", policy_text)
        
        if self._verbose:
            ctx.write_event_to_stream(LogEvent(msg=f">> Retrieved {len(policy_text)} characters of policy text"))
        
        return PolicyMatchedEvent(policy_text=policy_text)

    def _get_fallback_policy_text(self, claim_info: ClaimInfo) -> str:
        """Generate fallback policy text for demo purposes"""
        return f"""
CALIFORNIA PERSONAL AUTO POLICY
Policy Number: {claim_info.policy_number}

PART D - COVERAGE FOR DAMAGE TO YOUR AUTO
COLLISION COVERAGE
We will pay for direct and accidental loss to your covered auto caused by collision with another object or by upset of your covered auto.

DEDUCTIBLE
For each loss, our limit of liability will be reduced by the applicable deductible amount shown in the Declarations.
Standard collision deductible: $500
Comprehensive deductible: $250

LIMITS OF LIABILITY
Our limit of liability for loss will be the lesser of:
1. The actual cash value of the stolen or damaged property; or
2. The amount necessary to repair or replace the property.

EXCLUSIONS
We do not provide coverage for:
1. Loss to your covered auto which occurs while it is used to carry persons or property for compensation
2. Loss due to wear and tear, freezing, mechanical breakdown
3. Loss to equipment designed for the reproduction of sound
        """

    @step
    async def generate_recommendation(self, ctx: Context, ev: PolicyMatchedEvent) -> RecommendationEvent:
        """Generate policy recommendation based on claim and policy text"""
        if self._verbose:
            ctx.write_event_to_stream(LogEvent(msg=">> Generating Policy Recommendation"))
        
        claim_info = await ctx.get("claim_info")
        
        if self.llm:
            try:
                prompt = ChatPromptTemplate.from_messages([("user", POLICY_RECOMMENDATION_PROMPT)])
                recommendation = await self.llm.astructured_predict(
                    PolicyRecommendation,
                    prompt,
                    claim_info=claim_info.model_dump_json(),
                    policy_text=ev.policy_text
                )
            except Exception as e:
                if self._verbose:
                    ctx.write_event_to_stream(LogEvent(msg=f">> LLM recommendation failed, using fallback: {e}"))
                recommendation = self._generate_fallback_recommendation(claim_info, ev.policy_text)
        else:
            recommendation = self._generate_fallback_recommendation(claim_info, ev.policy_text)
        
        if self._verbose:
            ctx.write_event_to_stream(LogEvent(msg=f">> Recommendation: {recommendation.model_dump_json()}"))
        
        return RecommendationEvent(recommendation=recommendation)

    def _generate_fallback_recommendation(self, claim_info: ClaimInfo, policy_text: str) -> PolicyRecommendation:
        """Generate fallback recommendation using rule-based logic"""
        # Simple rule-based logic for demo
        covered = claim_info.estimated_repair_cost < 15000  # Coverage limit
        deductible = 500.0  # Standard deductible
        settlement_amount = max(0, claim_info.estimated_repair_cost - deductible) if covered else 0.0
        
        summary = f"Claim {claim_info.claim_number} for ${claim_info.estimated_repair_cost:.2f} damage"
        if covered:
            summary += f" is covered. Settlement: ${settlement_amount:.2f} after ${deductible:.2f} deductible."
        else:
            summary += " exceeds policy limits and is not covered."
        
        return PolicyRecommendation(
            policy_section="PART D - COLLISION COVERAGE",
            recommendation_summary=summary,
            deductible=deductible,
            settlement_amount=settlement_amount
        )

    @step
    async def finalize_decision(self, ctx: Context, ev: RecommendationEvent) -> DecisionEvent:
        """Finalize the claim decision based on policy recommendation"""
        if self._verbose:
            ctx.write_event_to_stream(LogEvent(msg=">> Finalizing Decision"))
        
        claim_info = await ctx.get("claim_info")
        rec = ev.recommendation
        
        covered = ("covered" in rec.recommendation_summary.lower() and 
                  "not covered" not in rec.recommendation_summary.lower()) or \
                 (rec.settlement_amount is not None and rec.settlement_amount > 0)
        
        deductible = rec.deductible if rec.deductible is not None else 0.0
        recommended_payout = rec.settlement_amount if rec.settlement_amount else 0.0
        
        decision = ClaimDecision(
            claim_number=claim_info.claim_number,
            covered=covered,
            deductible=deductible,
            recommended_payout=recommended_payout,
            notes=rec.recommendation_summary
        )
        
        if self._verbose:
            ctx.write_event_to_stream(LogEvent(msg=f">> Final Decision: Covered={covered}, Payout=${recommended_payout:.2f}"))
        
        return DecisionEvent(decision=decision)

    @step
    async def output_result(self, ctx: Context, ev: DecisionEvent) -> StopEvent:
        """Output the final decision result"""
        if self._verbose:
            ctx.write_event_to_stream(LogEvent(msg=f">> Decision: {ev.decision.model_dump_json()}"))
        
        return StopEvent(result={"decision": ev.decision})

    # Compatibility method for the Streamlit app
    async def run(self, claim_json_path: str) -> Dict[str, Any]:
        """Run the workflow with a claim JSON file path"""
        try:
            handler = super().run(claim_json_path=claim_json_path)
            result = await handler
            return result
        except Exception as e:
            if self._verbose:
                print(f"Workflow error: {e}")
            raise e