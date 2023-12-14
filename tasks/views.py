from rest_framework import generics, permissions
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwner

class TaskListCreateView(generics.ListCreateAPIView):
    """
    List all tasks or create a new task.

    Authentication:
    - Requires token-based authentication.

    Permissions:
    - Authenticated users are allowed.

    Create:
    - Provide the task details in the request body (title, description, due_date, status).

    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a task by ID.

    Authentication:
    - Requires token-based authentication.

    Permissions:
    - Authenticated users are allowed.
    - Users can only update or delete tasks that they own.

    Retrieve:
    - Returns the details of a specific task.

    Update:
    - Provide the updated task details in the request body.

    Delete:
    - Deletes the specified task.

    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
