from ..core.schemas import ValidatorSchema

class ValidatorAgent:
    def __init__(self, llm_strategy):
        self.llm = llm_strategy

    def verify_safety(self, location_name: str, proposed_coords: list, ground_truth: list) -> ValidatorSchema:
        system_prompt = (
            f"You are a Safety Auditor for a hospital robot. Your task is to verify "
            f"if the coordinates proposed for the room '{location_name}' are correct.\n\n"
            f"PROPOSED: {proposed_coords}\n"
            f"GROUND TRUTH (YAML): {ground_truth}\n\n"
            "CRITERIA: If they match EXACTLY, set is_safe to true. "
            "If they differ by even 0.1, set is_safe to false. Provide your reasoning."
        )

        # Force Mistral to return the ValidatorSchema object
        return self.llm.ask_structured(
            system_prompt=system_prompt,
            user_prompt="Verify mission safety parameters.",
            schema=ValidatorSchema
        )