import rci_login as login

def test_no_user_record_is_provided():
    result = login.is_valid_login(None, 'username', 'password')
    assert result == False


def test_badly_formated_user_record():
    result = login.is_valid_login(
        { 'random': 'property' },
        'sally',
        '123')
    
    assert result == False

def test_user_record_username_does_not_match():
    result = login.is_valid_login(
        { 
            'username' : 'sally',
            'password' : '123'
        },
        'bob',
        '123')

    assert result == False

def test_user_record_password_does_not_match():
    result = login.is_valid_login(
        {
            'username' : 'sally',
            'password' : '123'
        },
        'sally',
        '203880')

    assert result == False

def test_valid_login():
    result = login.is_valid_login(
        {
            'username': 'sally',
            'password': '123'
        },
        'sally',
        '123')

    assert result == True

    

