from app.core.db.models import User


def test_create_user(db_session):
    user = User(tg_id=123, tg_nickname="tester")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    fetched = db_session.get(User, user.id)
    assert fetched.tg_nickname == "tester"
    assert fetched.tg_id == 123
