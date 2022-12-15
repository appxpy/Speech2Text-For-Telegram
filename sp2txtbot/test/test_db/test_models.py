import pytest
from db.models import User, Recognition


@pytest.mark.filterwarnings("ignore:There is no current event loop")
@pytest.mark.asyncio
async def test_user_str_repr(initialize_db):
    user = await User.create(
        id=1,
        tag='test',
        username='test',
    )
    assert str(user) == 'test'
    assert repr(user) == f'<User: {user.id}>'


@pytest.mark.filterwarnings("ignore:There is no current event loop")
@pytest.mark.asyncio
async def test_recognition_str_repr(initialize_db):
    user = await User.create(
        id=1,
        tag='test',
        username='test',
    )
    recognition = await Recognition.create(
        user=user,
        file_id='test',
        recognized_text='test',
    )
    assert str(recognition) == f'Recognition {recognition.id}'
    assert repr(recognition) == f'<Recognition: {user.id}>'
