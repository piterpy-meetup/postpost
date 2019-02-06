from api.models import Workspace


class GlobalWorkspaceMiddleware(object):
    """
    Add request-relevant workspace object to request object.

    Because most of requests to our API tied to specific workspace (e.g.
    work with publications), the middleware saves us from a lot of repeated
    code for extracting workspace by request data.
    """

    def __init__(self, get_response):
        """
        Standard interface of django middleware.

        See more:
        https://docs.djangoproject.com/en/2.1/topics/http/middleware/#init-get-response
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Executed before view and other middlewares are called.

        And this method does nothing.
        """
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        One of the django middleware hook.

        Uses here for inject relevant workspace to request objects.
        Search Workspace instance by url params that a router usually
        generates.

        See more about this middleware hook:
        https://docs.djangoproject.com/en/2.1/topics/http/middleware/#process-view
        """
        workspace_name = view_kwargs.get('workspace_pk') or view_kwargs.get('workspace_name')
        if workspace_name:
            workspace = Workspace.objects.filter(name=workspace_name).first()
            if workspace:
                request.workspace = workspace
