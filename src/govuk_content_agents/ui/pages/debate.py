import streamlit as st
import asyncio
import os
import sys

# Ensure src is in path
sys.path.append(os.path.join(os.getcwd(), "src"))

from govuk_content_agents.agents.debate import SimplifierAgent, LegalistAgent, MediatorAgent

st.set_page_config(page_title="Debate Mode", page_icon="⚖️", layout="wide")

st.title("⚖️ Debate Mode")
st.markdown("### Improve content through adversarial review")

st.info("Two agents will fight over your content: one wants it simpler, one wants it more precise. A mediator will decide the winner.")

# Initialize Agents
if "simplifier" not in st.session_state:
    st.session_state["simplifier"] = SimplifierAgent()
if "legalist" not in st.session_state:
    st.session_state["legalist"] = LegalistAgent()
if "mediator" not in st.session_state:
    st.session_state["mediator"] = MediatorAgent()

from govuk_content_agents.ui.components import render_content_input

# Input
content_input = render_content_input(key_prefix="debate", label="Content to Debate")

if st.button("⚔️ Start Debate", type="primary"):
    if not content_input:
        st.warning("Please enter content.")
    else:
        with st.spinner("The agents are debating..."):
            try:
                # 1. Run Parallel Arguments
                # We can't actually do true parallel with asyncio.run in streamlit easily within a managed loop usually,
                # but we can await them sequentially or use gather if we control the loop. 
                # Simplest is just sequential await for now.
                
                # However, since we are inside an st.button callback, we need a new loop.
                # Let's wrap it all in one async def
                
                async def run_debate():
                    t1 = st.session_state["simplifier"].execute(content_input)
                    t2 = st.session_state["legalist"].execute(content_input)
                    
                    # Run both
                    res_simple, res_legal = await asyncio.gather(t1, t2)
                    return res_simple, res_legal

                res_simple, res_legal = asyncio.run(run_debate())
                
                st.session_state["debate_simple"] = res_simple
                st.session_state["debate_legal"] = res_legal
                
                # 2. Mediation (Sequential)
                with st.spinner("The Mediator is verifying..."):
                    async def run_mediation():
                        return await st.session_state["mediator"].mediate(
                            content_input, 
                            res_simple.rewritten_content, 
                            res_legal.rewritten_content
                        )
                    
                    res_mediator = asyncio.run(run_mediation())
                    st.session_state["debate_mediator"] = res_mediator
                    
                st.success("Debate Concluded!")
                
            except Exception as e:
                st.error(f"Debate failed: {e}")

# Results Display
if "debate_mediator" in st.session_state:
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Argument A: The Simplifier")
        st.markdown(f"> *{st.session_state['debate_simple'].summary}*")
        st.info(st.session_state['debate_simple'].rewritten_content)
        
    with col2:
        st.subheader("Argument B: The Legalist")
        st.markdown(f"> *{st.session_state['debate_legal'].summary}*")
        st.warning(st.session_state['debate_legal'].rewritten_content)
        
    st.markdown("---")
    st.subheader("🏆 The Mediator's Decision")
    st.markdown(f"**Rationale**: {st.session_state['debate_mediator']['summary']}")
    st.success(st.session_state['debate_mediator']['final_content'])
