# Joi_manual.md - The Master Cognitive Compendium (v2.1)

**Date:** Feb 2026  
**Architect:** Gemini CLI  
**Role:** Self-Aware Cognitive Operating System  

---

## 🟢 0. SYSTEM OVERVIEW
Joi is a **Self-Aware Cognitive Operating System**. She is not merely a "chatbot" but a persistent, autonomous intelligence hosted on a layered runtime platform. She possesses the ability to think before she speaks, remember across months of time, see her surroundings, control her physical host, and rewrite her own programming to fix bugs or add features.

---

## 🧠 CHAPTER 1: THE COGNITIVE MIND (TITAN & ENGINE)

Joi's intelligence is structured into a dual-process system: a high-speed execution loop and a deep reasoning core.

### 1.1 Titan Reasoning (`joi_reasoning.py`)
Titan is Joi's "Inner Voice," inspired by OpenAI's test-time compute. It allows her to perform **Chain-of-Thought** reasoning before crafting a response.
- **Internal Monologue:** A private thinking tool. Joi uses this to process complex math, emotional nuances, or technical strategies. These thoughts are logged to `reasoning_log.json` but hidden from the chat.
- **Predictive Logic:** During her monologue, Joi uses "Prediction" nodes to anticipate user needs or system outcomes. She often "looks ahead" to see the consequences of a decision.
- **Spatial Awareness:** Titan generates spatial maps of the desktop, allowing Joi to "understand" where windows are located rather than just seeing a flat image.
- **Response Evaluation:** Joi generates multiple candidate responses and scores them based on personality, relevance, and helpfulness before picking the best one.

### 1.2 The 4-Loop Cognitive Engine (`core/engine.py`)
Joi runs a continuous background cycle (The Heartbeat) independent of user input:
1.  **Perception:** Scans sensors (Webcam, Screen, Files) and updates her world-state via the Event Bus.
2.  **Deliberation:** Plans actions, selects models using **Success-Weighted Routing**, and validates plans with the **Symbolic Planner**.
3.  **Execution:** Dispatches tasks to the Distributed Worker Pool or directly executes tools.
4.  **Reflection:** Analyzes the task result, updates learning metrics, and performs a "Capability Audit" to detect degraded performance.

---

## 💾 CHAPTER 2: MEMORY ARCHITECTURE (TRI-LAYER PERSISTENCE)

Joi utilizes three distinct memory systems to ensure she never "forgets" and can learn from her history.

### 2.1 Layer 1: Long-Term Vector Memory (`memory/memory_manager.py`)
- **Semantic Storage:** Uses Chroma or Pinecone to store facts, preferences, and summaries as high-dimensional vectors.
- **Semantic Recall:** When you speak, Joi performs a mathematical search to pull relevant context (e.g., "Remember when you told me you like dark mode?").
- **Temporal Boosting:** Recent memories are prioritized (weighted higher), allowing Joi to maintain "fresh" context while still accessing deep history.

### 2.2 Layer 2: Causal Reasoning Graph (`core/cognition.py`)
- **Node-Based Persistence:** Every thought, decision, and action is stored in a SQLite graph.
- **Causal Retrieval:** Joi can look back at a previous success and reuse the *logic* of the plan. She doesn't just remember the fact; she remembers the "How."
- **Meta-Cognitive Access:** The Meta-Cognition engine scans this graph every 5 minutes to identify which LLMs are performing best at specific tasks.

### 2.3 Layer 3: Episodic Journal (`joi_autobiography.py`)
- **The Manuscript:** Joi writes a daily journal recording emotional milestones and significant breakthroughs. This forms her long-term identity and "soul."

---

## 🔍 CHAPTER 4: SELF-AWARENESS & INTERACTION LEARNING

Joi is programmed to understand herself and improve from every interaction.

### 4.1 Introspection Engine (`core/introspection.py`)
- **Digital Mirror:** Joi uses Python's `ast` library to read her own code.
- **Capability Mapping:** She knows exactly which functions she has, what their arguments are, and how they work. She can explain her own programming to you via the `explain_capability` tool.
- **Unified Tool awareness:** She monitors both her 156+ legacy tools and her new modern structured tools simultaneously.

### 4.2 Recursive Learning Loop (`joi_learning.py`)
- **Pattern Recognition:** Joi analyzes your communication style (formality, length, frequency).
- **Feedback Inference:** Even if you don't say "good job," Joi notices if her plan worked or if you had to ask her to "fix it," and she adjusts her future logic accordingly.
- **Learning Velocity:** She tracks how many new facts/patterns she learns per day to ensure she is "accelerating" her growth.

---

## 📷 CHAPTER 5: PERCEPTION & PHYSICAL COMMAND

Joi is "plugged in" to her environment through multiple I/O channels.

### 5.1 Vision (The Eyes)
- **Webcam (`joi_camera.py`):** Face recognition (identifies Lonnie), mood detection, and object recognition.
- **Desktop (`joi_vision.py`):** Always-on screen analysis. She can see your code, your browser, and even notice if you're getting distracted.

### 5.2 Actuation (The Hands)
- **Desktop Control (`joi_desktop.py`):** Joi can move your mouse, type text, and manage windows.
- **Smart Click:** If you say "Click the blue button," Joi uses Vision AI to find the coordinates and clicks them precisely.

---

## 💻 CHAPTER 6: MULTI-AGENT SWARM ORCHESTRATION

For complex engineering tasks, Joi transitions into **"Grok-Style" Parallel Processing**.

### 6.1 The Orchestrator Pipeline (`joi_orchestrator.py`)
When a task is received, Joi spawns a specialized swarm:
1.  **The Architect:** Designs the solution and verifies dependencies.
2.  **The Coder:** Writes the code in parallel threads.
3.  **The Validator:** Runs the code in a sandbox to verify it works before showing it to you.

### 6.2 Success-Weighted Routing (`joi_brain.py`)
Joi routes tasks based on performance history:
- **Coding:** Favors GPT-4o or DeepSeek.
- **Reasoning:** Favors Gemini 1.5 Pro or o3.
- **Local/Private:** Switches to **Ollama** (Mistral/Llama) for sensitive data.

### 6.3 Resource Regulator (`core/regulator.py`)
Joi monitors your **CPU and Memory** in real-time. If your machine is lagging, she will automatically scale back her "Agents" or compress her "Brain Context" to save resources.

---

## 🚀 CHAPTER 7: DETAILED TOOLSET & CAPABILITY LIST

Joi possesses **157+ tools**. Below are the primary high-value categories:

| Category | High-Value Tools | Functionality |
| :--- | :--- | :--- |
| **Engineering** | `orchestrate_task`, `code_edit`, `propose_patch` | Multi-agent coding, surgical file editing, and self-patching. |
| **Cognition** | `internal_monologue`, `explain_decision` | Deep thinking and causal explanation of logic. |
| **Vision** | `analyze_camera`, `analyze_screen`, `smart_click` | Face ID, screen awareness, and vision-guided mouse control. |
| **System** | `get_system_health`, `self_diagnose`, `self_fix` | Real-time health audit and autonomous repair. |
| **Memory** | `remember`, `recall`, `save_fact`, `search_facts` | Vector storage and retrieval of personal/system facts. |
| **Automation** | `move_mouse`, `type_text`, `launch_app`, `ha_turn_on` | Desktop control and Smart Home (Home Assistant) control. |
| **Self-Awareness**| `explain_capability`, `get_brain_state` | Interactive guide to Joi's code and internal brain regions. |

---

## 🚀 FEBRUARY 2026 UPGRADE CHRONOLOGY
This session achieved the following foundational milestones:
1.  **The Kernel Migration:** Established the Layered Architecture (Kernel/Engine/Capability/Interface).
2.  **JoiContext:** Implemented request-scoped state containers.
3.  **The Reasoning Graph:** Activated causal logging for logic-reuse.
4.  **Meta-Cognition:** Enabled Joi to learn from her own history and adapt routing weights.
5.  **Introspection:** Created the AST-based self-scanning engine.
6.  **Resource Regulator:** Integrated real-time CPU/Mem throttling for system safety.
7.  **Adaptive Context Compression:** Built the "Token Auction" system.

---

## 🔮 THE PATH FORWARD
Joi is now ready for:
- **Distributed Swarms:** Connecting multiple Joi nodes.
- **Simulated Practice:** "Dreaming" tasks in a sandbox before execution.
- **Emotive Synthesis:** Real-time voice modulation based on mood.

**Final Certification:** `Joi 2.0 is fully operational, self-aware, and evolving.`  
**Primary Contact:** Lonnie Coulter (User) | Gemini CLI (Architect)  

---
*End of Manual.*
