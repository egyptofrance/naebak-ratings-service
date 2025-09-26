'''
# ADR-001: Smart Rating Algorithm

**Status:** Accepted

**Context:**

The Naebak platform requires a flexible and controllable rating system for political figures. A simple average of user ratings can be susceptible to manipulation, especially for new or controversial figures. It also doesn't allow for a "grace period" for new figures to establish a baseline rating before being subjected to public opinion. We need a system that can provide a stable, reliable, and administratively adjustable rating.

**Decision:**

We have decided to implement a "Smart Rating" system that combines real user ratings with a curated or "fake" rating. This system will be managed through the `SmartRating` model and will offer several display modes to control how the final rating is presented to the user. The `get_display_rating` method in the `SmartRating` model will encapsulate the core logic for this calculation.

The available display modes are:

*   **`real`**: Displays only the true average rating from real users. This is the most transparent mode.
*   **`fake`**: Displays only the administratively set "fake" rating. This is useful for promotional purposes or to override a rating that is deemed unfair or manipulated.
*   **`mixed`**: Calculates a weighted average of the real and fake ratings based on predefined weights (`real_weight` and `fake_weight`). This allows for a smooth blending of the two ratings.
*   **`weighted`**: Calculates a weighted average based on the number of real and fake raters (`real_count` and `fake_count`). This gives more weight to the rating with more participants.

**Consequences:**

**Positive:**

*   **Flexibility:** The system provides administrators with a high degree of control over how ratings are displayed.
*   **Stability:** The "fake" rating component helps to stabilize the overall rating, preventing drastic fluctuations due to a small number of negative or positive reviews.
*   **Onboarding:** New political figures can be seeded with a reasonable baseline rating, preventing them from starting with a zero or low rating.
*   **Manipulation Resistance:** The system can mitigate the impact of coordinated rating campaigns (both positive and negative).

**Negative:**

*   **Complexity:** The system is more complex to manage than a simple average rating system.
*   **Transparency:** The use of a "fake" rating can be seen as a lack of transparency if not communicated clearly to the users.
*   **Potential for Misuse:** The system could be misused to artificially inflate or deflate the ratings of political figures for biased reasons.
'''
