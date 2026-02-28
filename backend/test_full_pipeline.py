from service import generate_answer

if __name__ == "__main__":
    result = generate_answer(
        question="How do I check in for my flight?",
        persona="First-time traveler",
        mode="Checklist"
    )

    print(result)