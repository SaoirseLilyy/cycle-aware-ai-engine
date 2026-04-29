class MenstrualPhaseConverter:
    """
    Convert menstrual cycle day + gender into:
    - a menstrual phase name ("Menstrual", "Follicular", "Ovulatory", "Luteal")
    - an encoded intensity score (0–3)

    Behaviour:
    - If gender is "F" and day is valid (1–35), get_phase() returns the phase
      name and get_intensity() returns an integer 0–3.
    - If gender is not "F" or day is missing/invalid, both methods return -1.
    """

    # Map menstrual phase → numerical intensity
    _PHASE_TO_INTENSITY = {
        "Menstrual": 0,
        "Follicular": 2,
        "Ovulatory": 3,
        "Luteal": 1,
    }

    def __init__(self, day=None, gender=None):
        self.day = day
        self.gender = gender
        self.phase = None
        self.intensity = None

    def get_phase(self):
        """
        Determine menstrual phase based on cycle day.

        Returns:
            str: Phase name if day is in a valid range.
            int: -1 if day is missing or out of range.
        """
        if self.day is None:
            return -1
        if 1 <= self.day <= 5:
            self.phase = "Menstrual"
        elif 6 <= self.day <= 13:
            self.phase = "Follicular"
        elif 14 <= self.day <= 16:
            self.phase = "Ovulatory"
        elif 17 <= self.day <= 35:
            self.phase = "Luteal"
        else:
            return -1

        return self.phase

    def get_intensity(self):
        """
        Convert menstrual phase into a numerical intensity score.

        Returns:
            int: 0–3 if gender is "F" and day is valid, otherwise -1.
        """
        if self.gender != "F" or self.day is None:
            return -1

        phase = self.get_phase()
        if phase == -1:
            return -1

        return self._PHASE_TO_INTENSITY[self.phase]
