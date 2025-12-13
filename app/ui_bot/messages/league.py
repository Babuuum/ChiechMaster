from app.ui_bot.utils.progress_bars import create_progress_bar


def format_chiech_master_message(league, league_goals, league_big_goals) -> str:
    """
    Форматирует сообщение для команды chiech_master.

    Args:
        league: Объект лиги
        league_goals: Список целей лиги
        league_big_goals: Список больших целей лиги

    Returns:
        Отформатированное сообщение в Markdown
    """
    lines = []

    # Заголовок лиги
    lines.append(f"<b>🏆 {league.name}</b>\n")

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
        big_goal_color = "#3498db"  # Синий цвет для big_goals
        status_icon = "✅" if big_goal.completed else "⏳"
        lines.append(f'<b><span style="color: {big_goal_color};">{status_icon} {big_goal.name}</span></b>')

        # Если есть описание
        if big_goal.description:
            lines.append(f'<i><span style="color: {big_goal_color};">{big_goal.description}</span></i>')

        # Цели для этого big_goal
        if big_goal.id in goals_by_big_goal:
            big_goal_goals = goals_by_big_goal[big_goal.id]
            completed_goals = sum(1 for g in big_goal_goals if g.completed)

            # Прогресс бар для целей в big_goal
            progress_bar = create_progress_bar(completed_goals, len(big_goal_goals))
            lines.append(f'    <code>{progress_bar}</code> {completed_goals}/{len(big_goal_goals)}')

            # Список целей
            for goal in big_goal_goals:
                goal_color = "#2ecc71"  # Зеленый цвет для целей
                goal_status = "✓" if goal.completed else "○"
                difficult_icon = ""

                if hasattr(goal, 'difficult'):
                    if goal.difficult.name == "HARD":
                        difficult_icon = "🔥"
                    elif goal.difficult.name == "EASY":
                        difficult_icon = "🌱"

                lines.append(
                    f'    <span style="color: {goal_color};">{goal_status} {difficult_icon} {goal.name}</span>')

        lines.append("")  # Пустая строка для отступа

    # Теперь добавляем цели без big_goal (если такие есть)
    goals_without_big_goal = [g for g in league_goals if g.big_goal_id is None or g.big_goal_id not in big_goals_dict]

    if goals_without_big_goal:
        lines.append("<b>📌 Прочие цели:</b>")

        # Прогресс бар для всех целей без big_goal
        completed_without_big = sum(1 for g in goals_without_big_goal if g.completed)
        progress_bar = create_progress_bar(completed_without_big, len(goals_without_big_goal))
        lines.append(f'<code>{progress_bar}</code> {completed_without_big}/{len(goals_without_big_goal)}')

        # Список целей без big_goal
        goal_color = "#2ecc71"  # Зеленый цвет для целей
        for goal in goals_without_big_goal:
            goal_status = "✓" if goal.completed else "○"
            difficult_icon = ""

            if hasattr(goal, 'difficult'):
                if goal.difficult.name == "HARD":
                    difficult_icon = "🔥"
                elif goal.difficult.name == "EASY":
                    difficult_icon = "🌱"

            lines.append(f'<span style="color: {goal_color};">{goal_status} {difficult_icon} {goal.name}</span>')

    # Общая статистика
    total_goals = len(league_goals)
    completed_goals = sum(1 for g in league_goals if g.completed)

    if total_goals > 0:
        lines.append("\n" + "=" * 30)
        lines.append(f"<b>📊 Общий прогресс:</b>")
        overall_progress = create_progress_bar(completed_goals, total_goals, length=15)
        lines.append(f'<code>{overall_progress}</code>')
        lines.append(f"<b>Выполнено:</b> {completed_goals}/{total_goals} ({completed_goals / total_goals * 100:.1f}%)")

    return "\n".join(lines)