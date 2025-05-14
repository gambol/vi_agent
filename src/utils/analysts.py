"""Constants and utilities related to analysts configuration."""

from src.agents.aswath_damodaran import aswath_damodaran_agent
from src.agents.ben_graham import ben_graham_agent
from src.agents.bill_ackman import bill_ackman_agent
from src.agents.cathie_wood import cathie_wood_agent
from src.agents.charlie_munger import charlie_munger_agent
from src.agents.fundamentals import fundamentals_agent
from src.agents.michael_burry import michael_burry_agent
from src.agents.phil_fisher import phil_fisher_agent
from src.agents.peter_lynch import peter_lynch_agent
from src.agents.sentiment import sentiment_agent
from src.agents.stanley_druckenmiller import stanley_druckenmiller_agent
from src.agents.technicals import technical_analyst_agent
from src.agents.valuation import valuation_agent
from src.agents.warren_buffett import warren_buffett_agent

from src.utils.display_names import ANALYST_DISPLAY_NAMES

# Define analyst configuration - single source of truth
ANALYST_CONFIG = {
    "aswath_damodaran": {
        "display_name": ANALYST_DISPLAY_NAMES["aswath_damodaran"],
        "agent_func": aswath_damodaran_agent,
        "order": 0,
    },
    "ben_graham": {
        "display_name": ANALYST_DISPLAY_NAMES["ben_graham"],
        "agent_func": ben_graham_agent,
        "order": 1,
    },
    "bill_ackman": {
        "display_name": ANALYST_DISPLAY_NAMES["bill_ackman"],
        "agent_func": bill_ackman_agent,
        "order": 2,
    },
    "cathie_wood": {
        "display_name": ANALYST_DISPLAY_NAMES["cathie_wood"],
        "agent_func": cathie_wood_agent,
        "order": 3,
    },
    "charlie_munger": {
        "display_name": ANALYST_DISPLAY_NAMES["charlie_munger"],
        "agent_func": charlie_munger_agent,
        "order": 4,
    },
    "michael_burry": {
        "display_name": ANALYST_DISPLAY_NAMES["michael_burry"],
        "agent_func": michael_burry_agent,
        "order": 5,
    },
    "peter_lynch": {
        "display_name": ANALYST_DISPLAY_NAMES["peter_lynch"],
        "agent_func": peter_lynch_agent,
        "order": 6,
    },
    "phil_fisher": {
        "display_name": ANALYST_DISPLAY_NAMES["phil_fisher"],
        "agent_func": phil_fisher_agent,
        "order": 7,
    },
    "stanley_druckenmiller": {
        "display_name": ANALYST_DISPLAY_NAMES["stanley_druckenmiller"],
        "agent_func": stanley_druckenmiller_agent,
        "order": 8,
    },
    "warren_buffett": {
        "display_name": ANALYST_DISPLAY_NAMES["warren_buffett"],
        "agent_func": warren_buffett_agent,
        "order": 9,
    },
    "technical_analyst": {
        "display_name": ANALYST_DISPLAY_NAMES["technical_analyst"],
        "agent_func": technical_analyst_agent,
        "order": 10,
    },
    "fundamentals_analyst": {
        "display_name": ANALYST_DISPLAY_NAMES["fundamentals_analyst"],
        "agent_func": fundamentals_agent,
        "order": 11,
    },
    "sentiment_analyst": {
        "display_name": ANALYST_DISPLAY_NAMES["sentiment_analyst"],
        "agent_func": sentiment_agent,
        "order": 12,
    },
    "valuation_analyst": {
        "display_name": ANALYST_DISPLAY_NAMES["valuation_analyst"],
        "agent_func": valuation_agent,
        "order": 13,
    },
}

# 默认选中的分析师
DEFAULT_ANALYSTS = [
    "warren_buffett",
    "charlie_munger",
    # "peter_lynch",
    # "michael_burry",
    # "phil_fisher",
    # "stanley_druckenmiller",
    "sentiment_analyst",
    "fundamentals_analyst",
    "technical_analyst",
]

# Derive ANALYST_ORDER from ANALYST_CONFIG for backwards compatibility
ANALYST_ORDER = [(config["display_name"], key) for key, config in sorted(ANALYST_CONFIG.items(), key=lambda x: x[1]["order"])]


def get_analyst_nodes():
    """Get the mapping of analyst keys to their (node_name, agent_func) tuples."""
    return {key: (f"{key}_agent", config["agent_func"]) for key, config in ANALYST_CONFIG.items()}
