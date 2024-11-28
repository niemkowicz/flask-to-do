import unittest
from unittest.mock import patch, MagicMock
from app import app, db, Task

class TaskAppTests(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()


    def test_add_task(self):
        task = Task(content='New task')
        db.session.add(task)
        db.session.commit()

        response = self.app.post('/add', data={'content': 'New task'})
        self.assertEqual(response.status_code, 302)

    def test_get_all_tasks(self):
        mock_task = MagicMock()
        mock_task.content = 'New task'

        with patch('app.Task.query') as mock_query:
            mock_query.all.return_value = [mock_task]

            response = self.app.get('/')
            self.assertIn('New task', str(response.data))
            mock_query.all.assert_called_once()

    def test_update_task(self):
        task = Task(content='Old task')
        db.session.add(task)
        db.session.commit()

        response = self.app.post(f'/update/{task.id}', data={'content': 'Updated task'})
        self.assertEqual(response.status_code, 302)

        updated_task = db.session.get(Task, task.id)
        self.assertEqual(updated_task.content, 'Updated task')

    def test_delete_task(self):
        task = Task(content='Task to be deleted')
        db.session.add(task)
        db.session.commit()

        response = self.app.post(f'/delete/{task.id}')
        self.assertEqual(response.status_code, 302)

        deleted_task = db.session.get(Task, task.id)
        self.assertIsNone(deleted_task)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


if __name__ == '__main__':
    unittest.main()
