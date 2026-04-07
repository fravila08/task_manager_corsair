from user_app.views import UserView
from rest_framework.response import Response
from .serializers import TaskSerializer
from rest_framework import status as s
from django.shortcuts import get_object_or_404, get_list_or_404

# Create your views here.

# Handles collection-level operations: listing all tasks and creating a new one.
# Inheriting from UserView enforces TokenAuthentication on all methods — no extra
# auth setup needed here.
class AllTasks(UserView):

    # Returns every task belonging to the authenticated user.
    # `request.user.tasks` uses the reverse FK relation defined on the Task model
    # (related_name='tasks'), so only this user's tasks are ever exposed.
    def get(self, request):
        return Response(TaskSerializer(get_list_or_404(request.user.tasks), many=True).data)

    # Creates a new task and automatically ties it to the authenticated user.
    # request.data is immutable, so we copy it before injecting the user's PK —
    # this prevents DRF from raising a TypeError when we set data['user'].
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id  # bind the new task to the logged-in user
        ser_task = TaskSerializer(data=data)
        if ser_task.is_valid():
            ser_task.save()
            return Response(ser_task.data, status=s.HTTP_201_CREATED)
        else:
            return Response(ser_task.errors, status=s.HTTP_400_BAD_REQUEST)


# Handles single-task operations: retrieve, update, and delete by task_id.
# Scoping every query through `request.user.tasks` means a user can never
# access or modify another user's tasks — ownership is enforced at the DB query level.
class ATask(UserView):

    # Fetches a single task by PK, scoped to the authenticated user.
    def get(self, request, task_id):
        return Response(TaskSerializer(get_object_or_404(request.user.tasks, id=task_id)).data)

    # Partially updates a task (partial=True means omitted fields keep their current values).
    # Passing the existing instance as the first argument tells the serializer to UPDATE
    # rather than CREATE, which triggers the serializer's update() method on save().
    def put(self, request, task_id):
        data = request.data.copy()
        ser_task = TaskSerializer(get_object_or_404(request.user.tasks, id=task_id), data=data, partial=True)
        if ser_task.is_valid():
            ser_task.save()
            return Response(ser_task.data)
        else:
            return Response(ser_task.errors, status=s.HTTP_400_BAD_REQUEST)

    # Deletes the task and returns a human-readable confirmation string.
    # The title is captured before deletion because after task.delete() the
    # object is gone from the database and its attributes would be stale.
    def delete(self, request, task_id):
        task = get_object_or_404(request.user.tasks, id=task_id)
        return_string = f"{task.title} has been deleted"
        task.delete()
        return Response(return_string)