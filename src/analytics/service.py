def get_analytics_overview(db, organization_id: str) -> dict:
    """Gets an overview of analytics for an organization."""
    tasks_ref = db.collection(f"organizations/{organization_id}/tasks")
    llm_usages_ref = db.collection(f"organizations/{organization_id}/llm_usages")
    workflows_ref = db.collection(f"organizations/{organization_id}/workflows")

    workflows = {w.id: w.to_dict() for w in workflows_ref.stream()}

    total_runs = 0
    successful_runs = 0
    total_time_saved = 0
    for task in tasks_ref.stream():
        total_runs += 1
        task_data = task.to_dict()
        if task_data.get("status") == "success":
            successful_runs += 1
            workflow_id = task_data.get("workflow_id")
            if workflow_id in workflows:
                total_time_saved += workflows[workflow_id].get("estimated_time_saved", 5)

    failed_runs = total_runs - successful_runs
    success_rate = (successful_runs / total_runs) * 100 if total_runs > 0 else 0

    total_tokens = 0
    for usage in llm_usages_ref.stream():
        total_tokens += usage.to_dict().get("total_tokens", 0)

    return {
        "total_runs": total_runs,
        "successful_runs": successful_runs,
        "failed_runs": failed_runs,
        "success_rate": success_rate,
        "total_tokens": total_tokens,
        "total_time_saved_minutes": total_time_saved,
    }
