from api.models import Workspace


class GlobalWorkspaceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response()

    def process_view(self, request, view_func, view_args, view_kwargs):
        workspace_name = view_kwargs.get('workspace_pk') or view_kwargs.get('workspace_name')
        if workspace_name:
            workspace = Workspace.objects.filter(name=workspace_name).first()
            if workspace:
                request.workspace = workspace
