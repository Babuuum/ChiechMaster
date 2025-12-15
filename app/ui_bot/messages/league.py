from app.ui_bot.utils.progress_bars import create_progress_bar


def format_league_message_markdown(league, league_goals, league_big_goals) -> str:
    """
    Форматирует сообщение для команды chiech_master в Markdown.

    Args:
        league: Объект лиги
        league_goals: Список целей лиги
        league_big_goals: Список больших целей лиги

    Returns:
        Отформатированное сообщение в Markdown
    """
    lines = []

    # Заголовок лиги
    lines.append(f"*🏆 {league.name}*")
    lines.append("")  # Пустая строка

    # Создаем словари для быстрого доступа
    big_goals_dict = {bg.id: bg for bg in league_big_goals}
    goals_by_big_goal = {}

    # Группируем цели по big_goal_id
    for goal in league_goals:
        if goal.big_goal_id not in goals_by_big_goal:
            goals_by_big_goal[goal.big_goal_id] = []
        goals_by_big_goal[goal.big_goal_id].append(goal)

    # Сначала добавляем big_goals с их целями
    for big_goal in league_big_goals:
        # Заголовок big_goal
        status_icon = "✅" if big_goal.completed else "⏳"
        lines.append(f"**{status_icon} {big_goal.name}**")

        # Если есть описание
        if big_goal.description:
            lines.append(f"_{big_goal.description}_")

        # Цели для этого big_goal
        if big_goal.id in goals_by_big_goal:
            big_goal_goals = goals_by_big_goal[big_goal.id]
            completed_goals = sum(1 for g in big_goal_goals if g.completed)

            # Прогресс бар для целей в big_goal
            progress_bar = create_progress_bar(completed_goals, len(big_goal_goals))
            lines.append(f"`{progress_bar}` {completed_goals}/{len(big_goal_goals)}")

            # Список целей
            for goal in big_goal_goals:
                goal_status = "✓" if goal.completed else "○"
                difficult_icon = ""

                if hasattr(goal, 'difficult'):
                    if goal.difficult.name == "HARD":
                        difficult_icon = "🔥"
                    elif goal.difficult.name == "EASY":
                        difficult_icon = "🌱"
                    elif goal.difficult.name == "NORMAL":
                        difficult_icon = "⭐"

                goal_text = f"{goal_status} {difficult_icon} {goal.name}"
                if goal.completed:
                    goal_text = f"~~{goal_text}~~"  # Зачеркиваем выполненные цели

                lines.append(f"  • {goal_text}")

        lines.append("")  # Пустая строка для отступа

    # Теперь добавляем цели без big_goal (если такие есть)
    goals_without_big_goal = [g for g in league_goals if g.big_goal_id is None or g.big_goal_id not in big_goals_dict]

    if goals_without_big_goal:
        lines.append("**📌 Прочие цели:**")

        # Прогресс бар для всех целей без big_goal
        completed_without_big = sum(1 for g in goals_without_big_goal if g.completed)
        progress_bar = create_progress_bar(completed_without_big, len(goals_without_big_goal))
        lines.append(f"`{progress_bar}` {completed_without_big}/{len(goals_without_big_goal)}")

        # Список целей без big_goal
        for goal in goals_without_big_goal:
            goal_status = "✓" if goal.completed else "○"
            difficult_icon = ""

            if hasattr(goal, 'difficult'):
                if goal.difficult.name == "HARD":
                    difficult_icon = "🔥"
                elif goal.difficult.name == "EASY":
                    difficult_icon = "🌱"
                elif goal.difficult.name == "NORMAL":
                    difficult_icon = "⭐"

            goal_text = f"{goal_status} {difficult_icon} {goal.name}"
            if goal.completed:
                goal_text = f"~~{goal_text}~~"

            lines.append(f"  • {goal_text}")

        lines.append("")  # Пустая строка

    # Общая статистика
    total_goals = len(league_goals)
    completed_goals = sum(1 for g in league_goals if g.completed)

    if total_goals > 0:
        lines.append("=" * 20)
        lines.append("**📊 Общий прогресс:**")

        # Большой прогресс бар для общей статистики
        overall_progress = create_progress_bar(completed_goals, total_goals, width=15)
        lines.append(f"`{overall_progress}`")

        percentage = (completed_goals / total_goals * 100) if total_goals > 0 else 0
        lines.append(f"**Выполнено:** {completed_goals}/{total_goals} ({percentage:.1f}%)")

        # Дополнительная информация о лиге
        if hasattr(league, 'format'):
            lines.append(f"**Формат:** {league.format.value if hasattr(league.format, 'value') else league.format}")

        if hasattr(league, 'start_league_date'):
            lines.append(f"**Начало:** {league.start_league_date.strftime('%d.%m.%Y')}")

    return "\n".join(lines)