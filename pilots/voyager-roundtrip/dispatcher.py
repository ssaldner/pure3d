import typing as t

if t.TYPE_CHECKING:
    from _typeshed.wsgi import StartResponse
    from _typeshed.wsgi import WSGIApplication
    from _typeshed.wsgi import WSGIEnvironment


# DispatcherMiddlewareOrig is copied from werkzeug.middleware.dispatcher
# It is not used in this pilot, but only included for reference
# See the pilot chainingstraight where the original dispatcher is applied.


class DispatcherMiddlewareOrig:
    """Combine multiple applications as a single WSGI application.
    Requests are dispatched to an application based on the path it is
    mounted under.
    :param app: The WSGI application to dispatch to if the request
        doesn't match a mounted path.
    :param mounts: Maps path prefixes to applications for dispatching.
    """

    def __init__(
        self,
        app: "WSGIApplication",
        mounts: t.Optional[t.Dict[str, "WSGIApplication"]] = None,
    ) -> None:
        self.app = app
        self.mounts = mounts or {}

    def __call__(
        self, environ: "WSGIEnvironment", start_response: "StartResponse"
    ) -> t.Iterable[bytes]:
        script = environ.get("PATH_INFO", "")
        path_info = ""

        while "/" in script:
            if script in self.mounts:
                app = self.mounts[script]
                break

            script, last_item = script.rsplit("/", 1)
            path_info = f"/{last_item}{path_info}"
        else:
            app = self.mounts.get(script, self.app)

        original_script_name = environ.get("SCRIPT_NAME", "")
        environ["SCRIPT_NAME"] = original_script_name + script
        environ["PATH_INFO"] = path_info
        return app(environ, start_response)


class DispatcherMiddleware:
    """Leave the url intact after dispatching.

    This is like DispatcherMiddleware,
    but after dispatching the full url is passed to
    the chosen app, instead of removing the prefix that
    corresponds with the selected mount.
    """

    def __init__(
        self,
        app: "WSGIApplication",
        mounts: t.Optional[t.Dict[str, "WSGIApplication"]] = None,
    ) -> None:
        self.app = app
        self.mounts = mounts or {}

    def __call__(
        self, environ: "WSGIEnvironment", start_response: "StartResponse"
    ) -> t.Iterable[bytes]:
        script = environ.get("PATH_INFO", "")

        app = None

        for mount in self.mounts:
            if script.startswith(mount):
                app = self.mounts[mount]
                break

        if app is None:
            app = self.app

        original_script_name = environ.get("SCRIPT_NAME", "")
        environ["SCRIPT_NAME"] = original_script_name + script
        environ["PATH_INFO"] = script
        return app(environ, start_response)
