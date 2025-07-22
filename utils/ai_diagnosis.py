def diagnose_issues(peaks: list, faults: list):
    suggestions = []

    if "ghost_peaks" in faults:
        suggestions.append("Ghost peaks detected — check for septum bleed or carryover.")
    if "tailing" in faults:
        suggestions.append("Tailing observed — may be inlet liner damage or dirty column.")
    if "fronting" in faults:
        suggestions.append("Fronting detected — possible column overloading.")
    if "baseline_noise" in faults:
        suggestions.append("High baseline noise — check carrier gas purity or grounding.")
    if "inlet_leak" in faults:
        suggestions.append("Inlet leak simulated — verify septum and connections.")
    if "coelution" in faults:
        suggestions.append("Coelution detected — try longer column or slower ramp.")

    if not suggestions:
        suggestions.append("No obvious problems detected in simulated data.")

    return suggestions
