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

def _load_learning_data() -> Dict[str, Any]:
    """Load main learning data"""
    try:
        return json.loads(LEARNING_DATA_FILE.read_text())
    except:
        return {
            "interactions": [],
            "feedback_summary": {"positive": 0, "negative": 0, "improvement_requests": 0},
            "topics": {},
            "response_times": [],
            "created_at": time.time()
        }


def _save_learning_data(data: Dict[str, Any]):
    """Save main learning data"""
    # Limit interactions stored
    if len(data.get("interactions", [])) > MAX_INTERACTIONS_STORED:
        data["interactions"] = data["interactions"][-MAX_INTERACTIONS_STORED:]
    
    LEARNING_DATA_FILE.write_text(json.dumps(data, indent=2))


def _load_patterns() -> Dict[str, Any]:
    """Load learned patterns"""
    try:
        return json.loads(PATTERNS_FILE.read_text())
    except:
        return {
            "successful_patterns": {},
            "failed_patterns": {},
            "user_preferences": {},
            "communication_style": {}
        }


def _save_patterns(patterns: Dict[str, Any]):
    """Save learned patterns"""
    PATTERNS_FILE.write_text(json.dumps(patterns, indent=2))


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
