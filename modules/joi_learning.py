"""
modules/joi_learning.py

Interactive Learning & Continuous Improvement Module
====================================================

Enables Joi to learn from user interactions and improve over time:
- Records all conversations with context
- Analyzes communication patterns
- Learns from explicit feedback (good/bad/improve)
- Identifies knowledge gaps
- Tracks success/failure rates for different topics
- Adapts response style to user preferences
- Suggests self-improvements based on interaction data

This makes Joi progressively better at:
1. Understanding your communication style
2. Providing more relevant responses
3. Anticipating your needs
4. Avoiding repeated mistakes
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from collections import defaultdict, Counter
import re

import joi_companion
from flask import jsonify, request as flask_req
from modules.joi_memory import require_user

# ============================================================================
# CONFIGURATION
# ============================================================================

LEARNING_DATA_FILE = Path("learning_data.json")
INTERACTION_LOG_FILE = Path("interaction_log.json")
PATTERNS_FILE = Path("learned_patterns.json")

# Learning parameters
MAX_INTERACTIONS_STORED = 10000  # Keep last 10k interactions
PATTERN_MIN_FREQUENCY = 3  # Need 3+ occurrences to identify pattern
TOPIC_EXTRACTION_MIN_LENGTH = 4  # Minimum word length for topic extraction

# ============================================================================
# INITIALIZATION
# ============================================================================

def _ensure_data_files():
    """Initialize data files if they don't exist"""
    if not LEARNING_DATA_FILE.exists():
        LEARNING_DATA_FILE.write_text(json.dumps({
            "interactions": [],
            "feedback_summary": {
                "positive": 0,
                "negative": 0,
                "improvement_requests": 0
            },
            "topics": {},
            "response_times": [],
            "created_at": time.time()
        }, indent=2))
    
    if not INTERACTION_LOG_FILE.exists():
        INTERACTION_LOG_FILE.write_text(json.dumps({
            "sessions": [],
            "current_session": None
        }, indent=2))
    
    if not PATTERNS_FILE.exists():
        PATTERNS_FILE.write_text(json.dumps({
            "successful_patterns": {},
            "failed_patterns": {},
            "user_preferences": {},
            "communication_style": {}
        }, indent=2))

_ensure_data_files()


# ============================================================================
# DATA LOADING/SAVING
# ============================================================================

_learning_data_cache: Optional[Dict[str, Any]] = None
_learning_data_ts: float = 0
_patterns_cache: Optional[Dict[str, Any]] = None
_patterns_ts: float = 0
LEARNING_CACHE_TTL: float = 45.0


def _load_learning_data() -> Dict[str, Any]:
    """Load main learning data. Cached 45s to reduce file I/O per request."""
    global _learning_data_cache, _learning_data_ts
    now = time.time()
    if _learning_data_cache is not None and (now - _learning_data_ts) < LEARNING_CACHE_TTL:
        return _learning_data_cache
    try:
        data = json.loads(LEARNING_DATA_FILE.read_text())
        _learning_data_cache = data
        _learning_data_ts = now
        return data
    except Exception:
        default = {
            "interactions": [],
            "feedback_summary": {"positive": 0, "negative": 0, "improvement_requests": 0},
            "topics": {},
            "response_times": [],
            "created_at": time.time()
        }
        _learning_data_cache = default
        _learning_data_ts = now
        return default


def _save_learning_data(data: Dict[str, Any]):
    """Save main learning data"""
    global _learning_data_cache
    if len(data.get("interactions", [])) > MAX_INTERACTIONS_STORED:
        data["interactions"] = data["interactions"][-MAX_INTERACTIONS_STORED:]
    LEARNING_DATA_FILE.write_text(json.dumps(data, indent=2))
    _learning_data_cache = None  # invalidate so next load is fresh


def _load_patterns() -> Dict[str, Any]:
    """Load learned patterns. Cached 45s to reduce file I/O per request."""
    global _patterns_cache, _patterns_ts
    now = time.time()
    if _patterns_cache is not None and (now - _patterns_ts) < LEARNING_CACHE_TTL:
        return _patterns_cache
    try:
        data = json.loads(PATTERNS_FILE.read_text())
        _patterns_cache = data
        _patterns_ts = now
        return data
    except Exception:
        default = {
            "successful_patterns": {},
            "failed_patterns": {},
            "user_preferences": {},
            "communication_style": {}
        }
        _patterns_cache = default
        _patterns_ts = now
        return default


def _save_patterns(patterns: Dict[str, Any]):
    """Save learned patterns"""
    global _patterns_cache
    PATTERNS_FILE.write_text(json.dumps(patterns, indent=2))
    _patterns_cache = None  # invalidate so next load is fresh


# ============================================================================
# INTERACTION RECORDING
# ============================================================================

def record_interaction(**params) -> Dict[str, Any]:
    """
    Tool: Record a conversation interaction
    
    Args:
        user_input: What the user said/asked
        joi_response: What Joi responded
        feedback: Optional feedback ("good", "bad", "improve", or custom text)
        context: Optional context tags (e.g., ["coding", "debugging"])
        response_time: Optional time taken to respond (seconds)
    
    Returns:
        Confirmation and interaction ID
    """
    require_user()
    
    user_input = params.get("user_input", "")
    joi_response = params.get("joi_response", "")
    feedback = params.get("feedback")
    context = params.get("context", [])
    response_time = params.get("response_time")
    
    if not user_input or not joi_response:
        return {"ok": False, "error": "user_input and joi_response required"}
    
    data = _load_learning_data()
    
    # Extract topics from user input
    topics = _extract_topics(user_input)
    
    # Create interaction record
    interaction = {
        "id": f"interaction_{int(time.time() * 1000)}",
        "timestamp": time.time(),
        "datetime": datetime.now().isoformat(),
        "user_input": user_input,
        "joi_response": joi_response,
        "feedback": feedback,
        "context": context,
        "topics": topics,
        "response_time": response_time,
        "input_length": len(user_input),
        "response_length": len(joi_response)
    }
    
    data["interactions"].append(interaction)
    
    # Update feedback summary
    if feedback == "good":
        data["feedback_summary"]["positive"] += 1
    elif feedback == "bad":
        data["feedback_summary"]["negative"] += 1
    elif feedback == "improve":
        data["feedback_summary"]["improvement_requests"] += 1
    
    # Update topics tracking
    for topic in topics:
        if topic not in data["topics"]:
            data["topics"][topic] = {
                "count": 0,
                "positive_feedback": 0,
                "negative_feedback": 0
            }
        
        data["topics"][topic]["count"] += 1
        
        if feedback == "good":
            data["topics"][topic]["positive_feedback"] += 1
        elif feedback == "bad":
            data["topics"][topic]["negative_feedback"] += 1
    
    # Track response times
    if response_time:
        data["response_times"].append(response_time)
        if len(data["response_times"]) > 1000:
            data["response_times"] = data["response_times"][-1000:]
    
    _save_learning_data(data)
    
    # Update patterns if feedback provided
    if feedback:
        _update_patterns(interaction, feedback)
    
    return {
        "ok": True,
        "interaction_id": interaction["id"],
        "topics_identified": topics,
        "message": "Interaction recorded successfully"
    }


def _extract_topics(text: str) -> List[str]:
    """
    Extract meaningful topics from text
    
    Uses simple keyword extraction:
    - Removes common words (stop words)
    - Keeps words 4+ characters
    - Returns most relevant terms
    """
    # Simple stop words list
    stop_words = {
        "the", "this", "that", "these", "those", "with", "from", "have", "has",
        "will", "would", "could", "should", "does", "what", "when", "where",
        "which", "who", "why", "how", "can", "are", "is", "was", "were",
        "been", "being", "for", "and", "or", "but", "not", "your", "you",
        "my", "me", "i", "we", "they", "them", "their", "our", "his", "her"
    }
    
    # Extract words
    words = re.findall(r'\b[a-z]+\b', text.lower())
    
    # Filter and count
    topics = [
        word for word in words
        if len(word) >= TOPIC_EXTRACTION_MIN_LENGTH
        and word not in stop_words
    ]
    
    # Return unique topics (most common first)
    topic_counts = Counter(topics)
    return [topic for topic, count in topic_counts.most_common(10)]


def _update_patterns(interaction: Dict[str, Any], feedback: str):
    """
    Update learned patterns based on interaction feedback
    
    Identifies successful and failed patterns to learn from
    """
    patterns = _load_patterns()
    
    # Create pattern signature
    pattern_key = f"{','.join(interaction['topics'])}:{interaction['context']}"
    
    if feedback == "good":
        # Record successful pattern
        if pattern_key not in patterns["successful_patterns"]:
            patterns["successful_patterns"][pattern_key] = {
                "count": 0,
                "topics": interaction["topics"],
                "context": interaction["context"],
                "examples": []
            }
        
        patterns["successful_patterns"][pattern_key]["count"] += 1
        
        # Keep last 3 examples
        patterns["successful_patterns"][pattern_key]["examples"].append({
            "user_input": interaction["user_input"][:100],
            "joi_response": interaction["joi_response"][:100],
            "timestamp": interaction["timestamp"]
        })
        if len(patterns["successful_patterns"][pattern_key]["examples"]) > 3:
            patterns["successful_patterns"][pattern_key]["examples"] = \
                patterns["successful_patterns"][pattern_key]["examples"][-3:]
    
    elif feedback == "bad":
        # Record failed pattern
        if pattern_key not in patterns["failed_patterns"]:
            patterns["failed_patterns"][pattern_key] = {
                "count": 0,
                "topics": interaction["topics"],
                "context": interaction["context"],
                "examples": []
            }
        
        patterns["failed_patterns"][pattern_key]["count"] += 1
        patterns["failed_patterns"][pattern_key]["examples"].append({
            "user_input": interaction["user_input"][:100],
            "joi_response": interaction["joi_response"][:100],
            "timestamp": interaction["timestamp"]
        })
        if len(patterns["failed_patterns"][pattern_key]["examples"]) > 3:
            patterns["failed_patterns"][pattern_key]["examples"] = \
                patterns["failed_patterns"][pattern_key]["examples"][-3:]
    
    _save_patterns(patterns)


def calculate_learning_velocity(window_days: int = 7) -> Dict[str, Any]:
    """
    Calculate the rate of learning (new facts/patterns per day).
    Used by the Reflection Loop to track cognitive growth.
    """
    data = _load_learning_data()
    patterns = _load_patterns()
    
    # Simple count of interactions in window
    now = time.time()
    cutoff = now - (window_days * 24 * 3600)
    
    recent_interactions = [i for i in data["interactions"] if i["timestamp"] >= cutoff]
    recent_patterns = 0 # Future: track pattern creation timestamps
    
    velocity = len(recent_interactions) / window_days
    
    return {
        "interactions_per_day": round(velocity, 2),
        "total_patterns": len(patterns["successful_patterns"]),
        "status": "Accelerating" if velocity > 5 else "Steady"
    }


# ============================================================================
# PATTERN ANALYSIS
# ============================================================================

def analyze_learning_patterns(**params) -> Dict[str, Any]:
    """
    Tool: Analyze learned patterns and generate insights
    
    Returns:
        - Top performing topics
        - Common failure patterns
        - User preferences
        - Improvement suggestions
    """
    require_user()
    
    data = _load_learning_data()
    patterns = _load_patterns()
    
    # Analyze topics
    top_topics = sorted(
        data["topics"].items(),
        key=lambda x: x[1]["count"],
        reverse=True
    )[:10]
    
    # Calculate success rates by topic
    topic_success_rates = []
    for topic, stats in data["topics"].items():
        total_feedback = stats["positive_feedback"] + stats["negative_feedback"]
        if total_feedback > 0:
            success_rate = stats["positive_feedback"] / total_feedback
            topic_success_rates.append({
                "topic": topic,
                "success_rate": round(success_rate, 2),
                "total_interactions": stats["count"]
            })
    
    topic_success_rates.sort(key=lambda x: x["success_rate"], reverse=True)
    
    # Identify weak areas (topics with low success rate and high volume)
    weak_areas = [
        t for t in topic_success_rates
        if t["success_rate"] < 0.6 and t["total_interactions"] >= 5
    ]
    
    # Overall statistics
    total_interactions = len(data["interactions"])
    total_feedback = sum(data["feedback_summary"].values())
    
    avg_response_time = (
        sum(data["response_times"]) / len(data["response_times"])
        if data["response_times"] else 0
    )
    
    # Generate insights
    insights = _generate_learning_insights(data, patterns, weak_areas)
    
    return {
        "ok": True,
        "summary": {
            "total_interactions": total_interactions,
            "total_feedback": total_feedback,
            "positive_feedback_rate": round(
                data["feedback_summary"]["positive"] / max(total_feedback, 1), 2
            ),
            "average_response_time": round(avg_response_time, 2)
        },
        "top_topics": [
            {"topic": topic, "count": stats["count"], "success_rate": round(
                stats["positive_feedback"] / max(stats["positive_feedback"] + stats["negative_feedback"], 1), 2
            )}
            for topic, stats in top_topics
        ],
        "weak_areas": weak_areas,
        "successful_patterns": list(patterns["successful_patterns"].keys())[:10],
        "failed_patterns": list(patterns["failed_patterns"].keys())[:10],
        "insights": insights
    }


def _generate_learning_insights(
    data: Dict[str, Any],
    patterns: Dict[str, Any],
    weak_areas: List[Dict[str, Any]]
) -> List[str]:
    """Generate actionable insights from learning data"""
    insights = []
    
    # Feedback insights
    feedback = data["feedback_summary"]
    total_feedback = sum(feedback.values())
    
    if total_feedback > 0:
        positive_rate = feedback["positive"] / total_feedback
        
        if positive_rate >= 0.8:
            insights.append("✅ Excellent performance - 80%+ positive feedback")
        elif positive_rate >= 0.6:
            insights.append("👍 Good performance - consider addressing weak areas")
        else:
            insights.append("⚠️ Performance needs improvement - focus on failed patterns")
    
    # Topic insights
    if weak_areas:
        weak_topics = [w["topic"] for w in weak_areas[:3]]
        insights.append(
            f"🎯 Priority improvement areas: {', '.join(weak_topics)}"
        )
    
    # Pattern insights
    if patterns["successful_patterns"]:
        top_pattern = max(
            patterns["successful_patterns"].items(),
            key=lambda x: x[1]["count"]
        )
        insights.append(
            f"💡 Most successful pattern: {top_pattern[0]} ({top_pattern[1]['count']} successes)"
        )
    
    if patterns["failed_patterns"]:
        worst_pattern = max(
            patterns["failed_patterns"].items(),
            key=lambda x: x[1]["count"]
        )
        insights.append(
            f"🔴 Most problematic pattern: {worst_pattern[0]} ({worst_pattern[1]['count']} failures)"
        )
    
    # Response time insights
    if data["response_times"]:
        avg_time = sum(data["response_times"]) / len(data["response_times"])
        if avg_time > 5:
            insights.append("⏱️ Response times are slow - consider optimization")
        elif avg_time < 1:
            insights.append("⚡ Excellent response times")
    
    return insights


# ============================================================================
# SELF-IMPROVEMENT SUGGESTIONS
# ============================================================================

def suggest_improvements(**params) -> Dict[str, Any]:
    """
    Tool: Generate self-improvement suggestions based on learning data
    
    Returns specific, actionable improvements Joi can make
    """
    require_user()
    
    analysis = analyze_learning_patterns()
    
    suggestions = []
    
    # Analyze weak areas
    for weak_area in analysis["weak_areas"]:
        topic = weak_area["topic"]
        success_rate = weak_area["success_rate"]
        
        suggestions.append({
            "priority": "high",
            "area": topic,
            "issue": f"Success rate only {success_rate:.0%} for '{topic}' topics",
            "suggestion": f"Research and propose an upgrade to improve '{topic}' handling",
            "action": "propose_upgrade",
            "details": f"Create a specialized module or enhance existing code for better '{topic}' responses"
        })
    
    # Check for missing capabilities based on user requests
    data = _load_learning_data()
    
    # Common improvement request patterns
    improvement_keywords = {
        "faster": "performance optimization",
        "better": "quality improvement",
        "more detail": "comprehensive responses",
        "simplify": "simplified explanations",
        "examples": "more examples and demonstrations"
    }
    
    for interaction in data["interactions"][-100:]:  # Check last 100
        if interaction.get("feedback") == "improve":
            user_input_lower = interaction["user_input"].lower()
            for keyword, improvement_type in improvement_keywords.items():
                if keyword in user_input_lower:
                    suggestions.append({
                        "priority": "medium",
                        "area": improvement_type,
                        "issue": f"User requested: {keyword}",
                        "suggestion": f"Focus on {improvement_type} in responses",
                        "action": "adjust_behavior"
                    })
                    break
    
    # Deduplicate and prioritize
    unique_suggestions = []
    seen = set()
    
    for suggestion in suggestions:
        key = (suggestion["area"], suggestion["action"])
        if key not in seen:
            seen.add(key)
            unique_suggestions.append(suggestion)
    
    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    unique_suggestions.sort(key=lambda x: priority_order[x["priority"]])
    
    return {
        "ok": True,
        "suggestions": unique_suggestions[:10],  # Top 10
        "total_suggestions": len(unique_suggestions),
        "message": "Self-improvement suggestions generated from learning data"
    }


# ============================================================================
# COMMUNICATION STYLE LEARNING
# ============================================================================

def learn_communication_style(**params) -> Dict[str, Any]:
    """
    Tool: Analyze user's communication style and preferences
    
    Returns insights about how the user prefers to communicate
    """
    require_user()
    
    data = _load_learning_data()
    patterns = _load_patterns()
    
    # Analyze user's messages
    user_messages = [i["user_input"] for i in data["interactions"]]
    
    if not user_messages:
        return {"ok": False, "error": "No interactions recorded yet"}
    
    # Message length preferences
    avg_message_length = sum(len(msg) for msg in user_messages) / len(user_messages)
    
    # Formality analysis (simple heuristic)
    formal_indicators = ["please", "thank you", "could you", "would you", "kindly"]
    casual_indicators = ["hey", "yeah", "gonna", "wanna", "btw", "lol"]
    
    formal_count = sum(
        1 for msg in user_messages
        for indicator in formal_indicators
        if indicator in msg.lower()
    )
    casual_count = sum(
        1 for msg in user_messages
        for indicator in casual_indicators
        if indicator in msg.lower()
    )
    
    formality = "formal" if formal_count > casual_count else "casual"
    
    # Question vs statement ratio
    questions = sum(1 for msg in user_messages if '?' in msg)
    question_ratio = questions / len(user_messages)
    
    # Preferred response length (based on positive feedback)
    positive_interactions = [
        i for i in data["interactions"]
        if i.get("feedback") == "good"
    ]
    
    preferred_response_length = (
        sum(i["response_length"] for i in positive_interactions) / len(positive_interactions)
        if positive_interactions else 500
    )
    
    # Save to patterns
    patterns["communication_style"] = {
        "formality": formality,
        "avg_message_length": round(avg_message_length),
        "question_ratio": round(question_ratio, 2),
        "preferred_response_length": round(preferred_response_length),
        "last_updated": time.time()
    }
    
    _save_patterns(patterns)
    
    return {
        "ok": True,
        "style": {
            "formality": formality,
            "message_length": "short" if avg_message_length < 50 else "medium" if avg_message_length < 150 else "long",
            "interaction_type": "question-driven" if question_ratio > 0.6 else "conversational",
            "preferred_response_length": round(preferred_response_length)
        },
        "recommendations": [
            f"User prefers {formality} communication",
            f"User asks questions {round(question_ratio * 100)}% of the time",
            f"Optimal response length: {round(preferred_response_length)} characters"
        ]
    }


# ============================================================================
# STATISTICS & REPORTING
# ============================================================================

def get_learning_stats(**params) -> Dict[str, Any]:
    """
    Tool: Get comprehensive learning statistics
    
    Returns all learning metrics and trends
    """
    require_user()
    
    data = _load_learning_data()
    patterns = _load_patterns()
    
    # Calculate trends (last 7 days vs previous 7 days)
    now = time.time()
    week_ago = now - (7 * 24 * 3600)
    two_weeks_ago = now - (14 * 24 * 3600)
    
    recent_interactions = [
        i for i in data["interactions"]
        if i["timestamp"] >= week_ago
    ]
    previous_interactions = [
        i for i in data["interactions"]
        if two_weeks_ago <= i["timestamp"] < week_ago
    ]
    
    recent_positive = sum(
        1 for i in recent_interactions
        if i.get("feedback") == "good"
    )
    previous_positive = sum(
        1 for i in previous_interactions
        if i.get("feedback") == "good"
    )
    
    # Calculate trend
    recent_rate = recent_positive / max(len(recent_interactions), 1)
    previous_rate = previous_positive / max(len(previous_interactions), 1)
    
    trend = "improving" if recent_rate > previous_rate else "declining" if recent_rate < previous_rate else "stable"
    
    return {
        "ok": True,
        "overall": {
            "total_interactions": len(data["interactions"]),
            "total_topics": len(data["topics"]),
            "positive_feedback_rate": round(
                data["feedback_summary"]["positive"] / max(sum(data["feedback_summary"].values()), 1), 2
            ),
            "learning_since": datetime.fromtimestamp(data["created_at"]).isoformat()
        },
        "recent_performance": {
            "last_7_days": len(recent_interactions),
            "positive_rate": round(recent_rate, 2),
            "trend": trend
        },
        "patterns": {
            "successful": len(patterns["successful_patterns"]),
            "failed": len(patterns["failed_patterns"])
        }
    }


# ============================================================================
# TOOL REGISTRATION
# ============================================================================

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "record_interaction",
        "description": "Record a conversation interaction for learning. Tracks user input, Joi's response, feedback, and context to continuously improve performance.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_input": {"type": "string", "description": "What the user said/asked"},
                "joi_response": {"type": "string", "description": "What Joi responded"},
                "feedback": {"type": "string", "description": "Feedback: 'good', 'bad', 'improve', or custom text"},
                "context": {"type": "array", "items": {"type": "string"}, "description": "Context tags like ['coding', 'debugging']"},
                "response_time": {"type": "number", "description": "Time taken to respond (seconds)"}
            },
            "required": ["user_input", "joi_response"]
        }
    }},
    record_interaction
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "analyze_learning_patterns",
        "description": "Analyze learned patterns from interactions. Identifies successful approaches, weak areas, and generates insights for improvement.",
        "parameters": {"type": "object", "properties": {}}
    }},
    analyze_learning_patterns
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "suggest_improvements",
        "description": "Generate self-improvement suggestions based on learning data. Returns actionable improvements Joi can make to enhance performance.",
        "parameters": {"type": "object", "properties": {}}
    }},
    suggest_improvements
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "learn_communication_style",
        "description": "Analyze user's communication style and preferences. Learns formality level, message length preferences, and optimal response style.",
        "parameters": {"type": "object", "properties": {}}
    }},
    learn_communication_style
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "get_learning_stats",
        "description": "Get comprehensive learning statistics including trends, performance metrics, and pattern analysis.",
        "parameters": {"type": "object", "properties": {}}
    }},
    get_learning_stats
)


# ============================================================================
# FLASK ROUTES
# ============================================================================

def learning_route():
    """Learning system endpoint"""
    require_user()
    
    if flask_req.method == "GET":
        return jsonify(get_learning_stats())
    
    data = flask_req.get_json(silent=True) or {}
    action = data.get("action")
    
    if action == "record":
        return jsonify(record_interaction(**data))
    elif action == "analyze":
        return jsonify(analyze_learning_patterns(**data))
    elif action == "suggest":
        return jsonify(suggest_improvements(**data))
    elif action == "style":
        return jsonify(learn_communication_style(**data))
    else:
        return jsonify({"ok": False, "error": "Unknown action"})


joi_companion.register_route("/learning", ["GET", "POST"], learning_route, "learning_route")


# ============================================================================
# LEARNING-TO-BEHAVIOR LOOP -- System Prompt Injection
# ============================================================================

def compile_learning_block(max_chars: int = 500) -> str:
    """
    Build a concise system prompt block from learned patterns.

    Reads learning data + patterns -> returns text showing:
      - STRONG AREAS (top 3 successful topic patterns)
      - WEAK AREAS (topics with more negative than positive feedback)
      - Communication preferences (formality, response length)

    Injected as step 15 in /chat context assembly chain.
    """
    try:
        data = _load_learning_data()
        patterns = _load_patterns()
    except Exception:
        return ""

    lines: List[str] = []

    # ── Strong areas (topics with highest positive feedback) ──────────
    strong = []
    for topic, stats in data.get("topics", {}).items():
        pos = stats.get("positive_feedback", 0)
        neg = stats.get("negative_feedback", 0)
        if pos > 0 and pos > neg:
            strong.append((topic, pos, pos / max(pos + neg, 1)))
    strong.sort(key=lambda x: x[1], reverse=True)

    if strong:
        top3 = strong[:3]
        lines.append("[LEARNED -- strong areas]: " +
                      ", ".join(f"{t} ({int(r*100)}% positive)" for t, _, r in top3))

    # ── Weak areas (more negative than positive) ─────────────────────
    weak = []
    for topic, stats in data.get("topics", {}).items():
        pos = stats.get("positive_feedback", 0)
        neg = stats.get("negative_feedback", 0)
        if neg > pos and stats.get("count", 0) >= 2:
            weak.append(topic)

    if weak:
        lines.append("[LEARNED -- weak areas (improve here)]: " + ", ".join(weak[:5]))

    # ── Communication style preferences ──────────────────────────────
    comm = patterns.get("communication_style", {})
    if comm:
        parts = []
        if comm.get("formality"):
            parts.append(f"tone={comm['formality']}")
        prl = comm.get("preferred_response_length")
        if prl and prl > 0:
            label = "short" if prl < 200 else "medium" if prl < 600 else "long"
            parts.append(f"preferred_reply={label}")
        if parts:
            lines.append("[LEARNED -- communication style]: " + ", ".join(parts))

    # ── Successful pattern hints ─────────────────────────────────────
    sp = patterns.get("successful_patterns", {})
    if sp:
        top_pattern = max(sp.items(), key=lambda x: x[1].get("count", 0))
        if top_pattern[1].get("count", 0) >= 3:
            topics_str = ", ".join(top_pattern[1].get("topics", [])[:3])
            lines.append(f"[LEARNED -- best pattern]: topics [{topics_str}] worked {top_pattern[1]['count']} times")

    # ── Tool + model learning (from tool_usage_log.json) ──────────
    try:
        tool_block = compile_tool_learning_block(max_chars=300)
        if tool_block.strip():
            lines.append(tool_block.strip())
    except Exception:
        pass

    if not lines:
        return ""

    block = "\n[LEARNING CONTEXT -- patterns from past interactions]:\n" + "\n".join(lines) + "\n"

    # Truncate to max_chars
    if len(block) > max_chars:
        block = block[:max_chars - 3] + "...\n"

    return block


# ============================================================================
# AUTO-RECORD INTERACTION (background, no LLM tool call needed)
# ============================================================================

def auto_record_interaction(user_message: str, joi_reply: str):
    """
    Automatically record each chat turn for learning without requiring
    the LLM to invoke the record_interaction tool.

    Runs in a background thread -- never blocks /chat.
    Extracts topics, saves to learning_data.json with no feedback field
    (auto-records are neutral observations).
    Truncates inputs to 500 chars to keep storage lean.
    """
    import threading

    def _record():
        try:
            user_trunc = (user_message or "")[:500]
            reply_trunc = (joi_reply or "")[:500]

            if not user_trunc.strip():
                return

            data = _load_learning_data()
            topics = _extract_topics(user_trunc)

            interaction = {
                "id": f"auto_{int(time.time() * 1000)}",
                "timestamp": time.time(),
                "datetime": datetime.now().isoformat(),
                "user_input": user_trunc,
                "joi_response": reply_trunc,
                "feedback": None,
                "context": ["auto_recorded"],
                "topics": topics,
                "response_time": None,
                "input_length": len(user_trunc),
                "response_length": len(reply_trunc),
            }

            data["interactions"].append(interaction)

            # Update topic counts (no feedback to tally)
            for topic in topics:
                if topic not in data["topics"]:
                    data["topics"][topic] = {
                        "count": 0,
                        "positive_feedback": 0,
                        "negative_feedback": 0,
                    }
                data["topics"][topic]["count"] += 1

            _save_learning_data(data)
        except Exception as e:
            print(f"  [WARN] auto_record_interaction: {e}")

    threading.Thread(target=_record, daemon=True).start()


# ============================================================================
# TOOL USAGE LOGGING -- Track what tools Joi uses and outcomes
# ============================================================================

TOOL_LOG_FILE = Path("tool_usage_log.json")


def _load_tool_log() -> Dict[str, Any]:
    """Load tool usage log."""
    try:
        if TOOL_LOG_FILE.exists():
            return json.loads(TOOL_LOG_FILE.read_text())
    except Exception:
        pass
    return {
        "entries": [],
        "tool_stats": {},  # tool_name -> {calls, successes, failures}
        "model_stats": {},  # model -> {calls, task_types: {type: count}}
    }


def _save_tool_log(data: Dict[str, Any]):
    """Save tool usage log (keep last 2000 entries)."""
    if len(data.get("entries", [])) > 2000:
        data["entries"] = data["entries"][-2000:]
    TOOL_LOG_FILE.write_text(json.dumps(data, indent=2, default=str))


def log_tool_usage(
    tool_name: str,
    success: bool,
    context: Optional[Dict[str, Any]] = None,
    outcome: str = "",
):
    """
    Log a tool call and its outcome for learning.

    Called after every tool execution in the /chat tool loop.
    This is what closes the feedback gap -- Joi learns which tools
    work well for which situations.
    """
    try:
        data = _load_tool_log()

        entry = {
            "ts": time.time(),
            "tool": tool_name,
            "success": success,
            "outcome": outcome[:200],
            "context": context or {},
        }
        data["entries"].append(entry)

        # Update tool stats
        if tool_name not in data["tool_stats"]:
            data["tool_stats"][tool_name] = {"calls": 0, "successes": 0, "failures": 0}
        data["tool_stats"][tool_name]["calls"] += 1
        if success:
            data["tool_stats"][tool_name]["successes"] += 1
        else:
            data["tool_stats"][tool_name]["failures"] += 1

        _save_tool_log(data)
    except Exception as e:
        print(f"  [WARN] log_tool_usage: {e}")


def log_model_usage(
    model: str,
    task_type: str = "unknown",
    response_time_ms: int = 0,
    verified: Optional[bool] = None,
    tier: Optional[int] = None,
):
    """
    Log which model handled a task and how it performed.

    Called by the router after each /chat response.
    Builds a map of model -> task_type effectiveness.
    """
    try:
        data = _load_tool_log()

        if model not in data["model_stats"]:
            data["model_stats"][model] = {"calls": 0, "task_types": {}, "avg_response_ms": 0}
        stats = data["model_stats"][model]
        stats["calls"] += 1

        # Store tier info if provided
        if tier is not None:
            stats["tier"] = tier

        # Auto-detect tier from Brain's MODELS registry
        if "tier" not in stats:
            try:
                from modules.joi_brain import MODELS as _brain_models
                # Try to find model key from the model string (e.g., "openai:gpt-4o" -> "gpt-4o")
                model_lower = model.lower()
                for key, info in _brain_models.items():
                    if key in model_lower or info.get("display_name", "").lower() in model_lower:
                        stats["tier"] = info.get("tier", 0)
                        break
            except Exception:
                pass

        if task_type not in stats["task_types"]:
            stats["task_types"][task_type] = {"count": 0, "verified_ok": 0, "verified_fail": 0}
        stats["task_types"][task_type]["count"] += 1

        if verified is True:
            stats["task_types"][task_type]["verified_ok"] += 1
        elif verified is False:
            stats["task_types"][task_type]["verified_fail"] += 1

        # Running average of response time
        if response_time_ms > 0:
            old_avg = stats.get("avg_response_ms", 0)
            n = stats["calls"]
            stats["avg_response_ms"] = int((old_avg * (n - 1) + response_time_ms) / n)

        _save_tool_log(data)
    except Exception as e:
        print(f"  [WARN] log_model_usage: {e}")


def auto_infer_feedback(user_message: str, joi_reply: str, tool_calls: List[Dict[str, Any]]):
    """
    Automatically infer feedback from the interaction context.

    Heuristics:
      - User says "thanks", "perfect", "nice", "great" -> positive
      - User says "wrong", "no that's not", "fix this", "try again" -> negative
      - Tool calls succeeded -> positive signal for those tools
      - Tool calls failed -> negative signal

    This closes the gap where auto_record always has feedback=None.
    Runs in background thread.
    """
    import threading

    def _infer():
        try:
            msg_lower = (user_message or "").lower()

            # ── Infer from user sentiment ─────────────────────────────
            positive_signals = [
                "thanks", "thank you", "perfect", "nice", "great", "awesome",
                "good job", "that works", "love it", "exactly", "yes",
                "slay", "ate that", "iconic", "fire",
            ]
            negative_signals = [
                "wrong", "no that's not", "fix this", "try again",
                "that's incorrect", "doesn't work", "broken", "not what i",
                "undo", "rollback", "revert",
            ]

            feedback = None
            if any(sig in msg_lower for sig in positive_signals):
                feedback = "good"
            elif any(sig in msg_lower for sig in negative_signals):
                feedback = "bad"

            if feedback:
                data = _load_learning_data()
                # Find the most recent auto_recorded interaction and add feedback
                for interaction in reversed(data.get("interactions", [])):
                    if interaction.get("feedback") is None and interaction.get("context") == ["auto_recorded"]:
                        interaction["feedback"] = feedback

                        # Update topic feedback counts
                        for topic in interaction.get("topics", []):
                            if topic in data.get("topics", {}):
                                if feedback == "good":
                                    data["topics"][topic]["positive_feedback"] += 1
                                elif feedback == "bad":
                                    data["topics"][topic]["negative_feedback"] += 1

                        # Also update patterns
                        _update_patterns(interaction, feedback)
                        break

                _save_learning_data(data)

            # ── Infer from tool outcomes ──────────────────────────────
            for tc in (tool_calls or []):
                tool_name = tc.get("name", "")
                result_ok = tc.get("result_ok", True)
                if tool_name:
                    log_tool_usage(
                        tool_name=tool_name,
                        success=result_ok,
                        context={"source": "auto_infer"},
                        outcome="auto-detected " + ("success" if result_ok else "failure"),
                    )
        except Exception as e:
            print(f"  [WARN] auto_infer_feedback: {e}")

    threading.Thread(target=_infer, daemon=True).start()


# ============================================================================
# ENHANCED LEARNING BLOCK -- includes tool + model effectiveness
# ============================================================================

def compile_tool_learning_block(max_chars: int = 300) -> str:
    """
    Build a learning block from tool usage data.
    Shows which tools work well, which fail, and model performance.
    """
    try:
        data = _load_tool_log()
    except Exception:
        return ""

    lines = []

    # Tool effectiveness
    tool_stats = data.get("tool_stats", {})
    if tool_stats:
        # Find tools with high failure rates
        problem_tools = []
        strong_tools = []
        for tool, stats in tool_stats.items():
            calls = stats.get("calls", 0)
            if calls < 3:
                continue
            fail_rate = stats.get("failures", 0) / calls
            if fail_rate > 0.3:
                problem_tools.append(f"{tool} ({int(fail_rate*100)}% fail)")
            elif fail_rate < 0.1 and calls >= 5:
                strong_tools.append(tool)

        if strong_tools:
            lines.append(f"[TOOL LEARNING -- reliable]: {', '.join(strong_tools[:5])}")
        if problem_tools:
            lines.append(f"[TOOL LEARNING -- unreliable]: {', '.join(problem_tools[:3])}")

    # Model effectiveness (tier-aware)
    model_stats = data.get("model_stats", {})
    if model_stats:
        parts = []
        tier_calls = {1: 0, 2: 0, 3: 0}
        for model, stats in model_stats.items():
            calls = stats.get("calls", 0)
            avg_ms = stats.get("avg_response_ms", 0)
            tier = stats.get("tier", 0)
            if tier in tier_calls:
                tier_calls[tier] += calls
            if calls >= 3:
                tier_label = f"T{tier}" if tier else ""
                parts.append(f"{model}{(' '+tier_label) if tier_label else ''}: {calls} calls, {avg_ms}ms avg")
        if parts:
            lines.append(f"[MODEL LEARNING]: {'; '.join(parts[:4])}")
        # Tier distribution
        active_tiers = {k: v for k, v in tier_calls.items() if v > 0}
        if active_tiers:
            tier_parts = [f"T{t}={c}" for t, c in sorted(active_tiers.items())]
            lines.append(f"[TIER USAGE]: {', '.join(tier_parts)}")

    if not lines:
        return ""

    block = "\n" + "\n".join(lines) + "\n"
    return block[:max_chars]
