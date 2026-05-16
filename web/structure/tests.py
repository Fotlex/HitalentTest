import pytest
from rest_framework.test import APIClient
from web.structure.models import Department

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_create_department(api_client):
    response = api_client.post('/departments/', {'name': 'Backend'}, format='json')
    assert response.status_code == 201, response.data

@pytest.mark.django_db
def test_prevent_cyclic_tree(api_client):
    parent = Department.objects.create(name='A')
    child = Department.objects.create(name='B', parent=parent)
    
    response = api_client.patch(f'/departments/{parent.id}/', {'parent_id': child.id}, format='json')
    assert response.status_code == 409, response.data

@pytest.mark.django_db
def test_cascade_delete(api_client):
    dept = Department.objects.create(name='Main')
    Department.objects.create(name='Sub', parent=dept)
    
    response = api_client.delete(f'/departments/{dept.id}/?mode=cascade')
    assert response.status_code == 204
    assert Department.objects.count() == 0