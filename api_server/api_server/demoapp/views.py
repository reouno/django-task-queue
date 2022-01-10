from rest_framework.response import Response
from rest_framework.views import APIView

from api_server.celery import debug_task, sleep_task


class CallDebugTask(APIView):
    """Celeryにdebug_taskを登録"""

    def post(self, request):
        """POSTでタスク登録する。実行開始・完了は検知しない。
        - クエリでnum_tasks=N とすると、N回タスク登録する。
        """
        num_tasks = int(request.query_params.get('num_tasks')) if request.query_params.get('num_tasks') else 1
        [debug_task.delay(arg={'i': i + 1, 'args': request.data}) for i in range(num_tasks)]

        return Response(data={'message': 'Task is registered.'})


class CallSleepTask(APIView):
    """Celeryにsleep_taskを登録"""

    def post(self, request):
        """POSTでタスク登録する。実行開始・完了は検知しない。
        - クエリでnum_tasks=N とすると、N回タスク登録する。
        - クエリでsleep_sec=M とすると、M秒スリープするタスクになる。
        """
        num_tasks = int(request.query_params.get('num_tasks')) if request.query_params.get('num_tasks') else 1
        sleep_sec = int(request.query_params.get('sleep_sec')) if request.query_params.get('sleep_sec') else 1
        [sleep_task.delay(sleep_sec, arg={'i': i + 1, 'args': request.data}) for i in range(num_tasks)]

        return Response(data={'message': 'Task is registered.'})
