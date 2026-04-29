from jinja2 import Template
from production.sentence_mapping import intensity_map, phase_map, activity_map
from production.menstrual_phase import MenstrualPhaseConverter

# Template used to generate a natural-language movement recommendation
template_text = """
Today, we recommend a {{ intensity }} session of {{ activity }}.

{{ activity_msg }}

This session should last {{ duration }} minutes.
{% if phase %}
Your {{ phase }} phase supports this kind of movement — {{ phase_msg }}. 🌿
{% endif %}
"""

# Create Jinja2 template object
template = Template(template_text)


def generate_sentence(user_json, prediction):
    """
    Builds a personalised recommendation sentence using:
    - model prediction (activity)
    - user inputs
    - menstrual phase (optional)
    - sentence templates
    """

    # Retrieve mapped intensity description
    intensity_raw = user_json.get("intensity")
    intensity_desc = intensity_map.get(intensity_raw, "").lower()

    # Retrieve activity description
    activity_desc = activity_map.get(prediction, "")

    # Menstrual phase calculation (optional)
    day = user_json.get("days_since_last_period")
    gender = user_json.get("gender")

    # Default values when no menstrual data is provided
    phase = None
    phase_desc = None

    # Compute menstrual phase only if cycle day is provided
    if day is not None:
        conv = MenstrualPhaseConverter(day=day, gender=gender)
        phase = conv.get_phase()
        phase_desc = phase_map.get(phase)

    # Build template context
    context = {
        "duration": user_json.get("duration_minutes"),
        "intensity": intensity_desc,
        "activity": prediction,
        "activity_msg": activity_desc,
        "phase": phase,
        "phase_msg": phase_desc,
    }

    return template.render(context)
