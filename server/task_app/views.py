from user_app.views import UserView
from rest_framework.response import Response
from .serializers import TaskSerializer
from rest_framework import status as s
from django.shortcuts import get_object_or_404, get_list_or_404
from task_proj.utilies import handle_exceptions

# Create your views here.
class AllTasks(UserView):

    @handle_exceptions
    def get(self, request):
        return Response(TaskSerializer(get_list_or_404(request.user.tasks), many=True).data)

    @handle_exceptions
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id  # bind the new task to the logged-in user
        ser_task = TaskSerializer(data=data)
        if ser_task.is_valid():
            ser_task.save()
            return Response(ser_task.data, status=s.HTTP_201_CREATED)
        else:
            return Response(ser_task.errors, status=s.HTTP_400_BAD_REQUEST)


class ATask(UserView):

    @handle_exceptions
    def get(self, request, task_id):
        return Response(TaskSerializer(get_object_or_404(request.user.tasks, id=task_id)).data)

    @handle_exceptions
    def put(self, request, task_id):
        data = request.data.copy()
        ser_task = TaskSerializer(get_object_or_404(request.user.tasks, id=task_id), data=data, partial=True)
        if ser_task.is_valid():
            ser_task.save()
            return Response(ser_task.data)
        else:
            return Response(ser_task.errors, status=s.HTTP_400_BAD_REQUEST)

    @handle_exceptions
    def delete(self, request, task_id):
        task = get_object_or_404(request.user.tasks, id=task_id)
        return_string = f"{task.title} has been deleted"
        task.delete()
        return Response(return_string)