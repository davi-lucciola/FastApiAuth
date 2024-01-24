users: dict[int, dict[str, str]] = {
    1: {
        'username': 'davilucciola',
        'password': '123'
    },
    2: {
        'username': 'not3981',
        'password': '123'
    },
    3: {
        'username': 'ferrabacalfront',
        'password': '123'
    }
}


def get_user_by_username(username: str) -> dict | None:
    id = user = None
    for current_id, current_user in users.items():
        if current_user.get('username') == username:
            id, user = current_id, current_user
            break
    
    return id, user