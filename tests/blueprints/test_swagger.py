def test_swagger(client):
    rv = client.get('/swagger.json')
    assert rv.json['info']['title'] == 'Content'
