def create_progress_bar(completed: int, total: int, width: int = 10) -> str:
    if total <= 0:
        return "█" * width

    progress = min(completed / total, 1.0)
    filled_length = int(width * progress)
    bar = "█" * filled_length + "░" * (width - filled_length)
    percentage = int(progress * 100)
    return f"{bar} {percentage}%"