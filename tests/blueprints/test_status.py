def test_status(client):
    rv = client.get('/status')
    assert rv.json == {'message': 'Let the Content Flow!'}
