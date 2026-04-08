from src.graph import build_parallel_travel_agent


def main():
    agent = build_parallel_travel_agent()
    result = agent.invoke({
        "user_query": """
                      Plan a 5-day trip to London and find me flights and hotels from JFK to LHR
                      for 1 adult only from 21 Apr 2026 to 26 Apr 2026 (one way trip)
                      """,
        "messages": []
    })
    print("=" * 60)
    print("USER QUERY:")
    print(result["user_query"])

    print("\n" + "=" * 60)
    print("TASKS DISPATCHED:")
    for task in result.get("tasks", []):
        print(f"  • {task.source}: {task.user_query}")

    print("\n" + "=" * 60)
    print("AGENT RESULTS:")
    for r in result.get("agent_results", []):
        print(f"\n[{r['agent'].upper()}]")
        print("-" * 40)
        print(r["result"][:50000] + "..." if len(r["result"]) > 500 else r["result"])

    print("\n" + "=" * 60)
    print("FINAL SYNTHESIZED RESPONSE:")
    print("=" * 60)
    print(result["final_answer"])

if __name__ == "__main__":
    main()