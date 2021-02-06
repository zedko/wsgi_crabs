from os import path, getcwd

CONTENT_TYPES_MAP = {
        ".3gp": "video/3gpp",
        ".3gpp": "video/3gpp",
        ".7z": "application/x-7z-compressed",
        ".ai": "application/postscript",
        ".asf": "video/x-ms-asf",
        ".asx": "video/x-ms-asf",
        ".atom": "application/atom+xml",
        ".avi": "video/x-msvideo",
        ".bmp": "image/x-ms-bmp",
        ".cco": "application/x-cocoa",
        ".crt": "application/x-x509-ca-cert",
        ".css": "text/css",
        ".der": "application/x-x509-ca-cert",
        ".doc": "application/msword",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".ear": "application/java-archive",
        ".eot": "application/vnd.ms-fontobject",
        ".eps": "application/postscript",
        ".flv": "video/x-flv",
        ".gif": "image/gif",
        ".hqx": "application/mac-binhex40",
        ".htc": "text/x-component",
        ".htm": "text/html",
        ".html": "text/html",
        ".ico": "image/x-icon",
        ".jad": "text/vnd.sun.j2me.app-descriptor",
        ".jar": "application/java-archive",
        ".jardiff": "application/x-java-archive-diff",
        ".jng": "image/x-jng",
        ".jnlp": "application/x-java-jnlp-file",
        ".jpeg": "image/jpeg",
        ".jpg": "image/jpeg",
        ".js": "text/javascript",
        ".json": "application/json",
        ".kar": "audio/midi",
        ".kml": "application/vnd.google-earth.kml+xml",
        ".kmz": "application/vnd.google-earth.kmz",
        ".m3u8": "application/vnd.apple.mpegurl",
        ".m4a": "audio/x-m4a",
        ".m4v": "video/x-m4v",
        ".mid": "audio/midi",
        ".midi": "audio/midi",
        ".mjs": "text/javascript",
        ".mml": "text/mathml",
        ".mng": "video/x-mng",
        ".mov": "video/quicktime",
        ".mp3": "audio/mpeg",
        ".mp4": "video/mp4",
        ".mpeg": "video/mpeg",
        ".mpg": "video/mpeg",
        ".ogg": "audio/ogg",
        ".pdb": "application/x-pilot",
        ".pdf": "application/pdf",
        ".pem": "application/x-x509-ca-cert",
        ".pl": "application/x-perl",
        ".pm": "application/x-perl",
        ".png": "image/png",
        ".ppt": "application/vnd.ms-powerpoint",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".prc": "application/x-pilot",
        ".ps": "application/postscript",
        ".ra": "audio/x-realaudio",
        ".rar": "application/x-rar-compressed",
        ".rpm": "application/x-redhat-package-manager",
        ".rss": "application/rss+xml",
        ".rtf": "application/rtf",
        ".run": "application/x-makeself",
        ".sea": "application/x-sea",
        ".shtml": "text/html",
        ".sit": "application/x-stuffit",
        ".svg": "image/svg+xml",
        ".svgz": "image/svg+xml",
        ".swf": "application/x-shockwave-flash",
        ".tcl": "application/x-tcl",
        ".tif": "image/tiff",
        ".tiff": "image/tiff",
        ".tk": "application/x-tcl",
        ".ts": "video/mp2t",
        ".txt": "text/plain",
        ".wasm": "application/wasm",
        ".war": "application/java-archive",
        ".wbmp": "image/vnd.wap.wbmp",
        ".webm": "video/webm",
        ".webp": "image/webp",
        ".wml": "text/vnd.wap.wml",
        ".wmlc": "application/vnd.wap.wmlc",
        ".wmv": "video/x-ms-wmv",
        ".woff": "application/font-woff",
        ".woff2": "font/woff2",
        ".xhtml": "application/xhtml+xml",
        ".xls": "application/vnd.ms-excel",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".xml": "text/xml",
        ".xpi": "application/x-xpinstall",
        ".xspf": "application/xspf+xml",
        ".zip": "application/zip",
        "apple-app-site-association": "application/pkc7-mime",
        # Adobe Products - see:
        # https://www.adobe.com/devnet-docs/acrobatetk/tools/AppSec/xdomain.html#policy-file-host-basics
        "crossdomain.xml": "text/x-cross-domain-policy",
    }


class App:
    def __init__(self, settings, routes=None, middleware=None):
        self.settings = settings
        self.router = routes if routes else self.settings.ROUTES
        self.middleware = middleware if middleware else self.settings.MIDDLEWARE

    def __call__(self, environ, start_response):
        print('=' * 10)
        for (key, value) in environ.items():
            print(key, value)
        print('+' * 10)

        url_path: str = environ['PATH_INFO']
        content_type: str = "text/html"

        request = {}
        for ware in self.middleware:
            ware(request)

        # make sure that both URL (in environ['PATH_info'] and in routes dict) have slashes as last symbol
        if self.fix_url_slash(url_path) in (self.fix_url_slash(key) for key in self.router.keys()):
            data, status = self.router[url_path](request)
            binary_data = data.encode(encoding='utf-8')
        # static delivery
        elif url_path.startswith(self.settings.STATIC_URL):
            file_path = url_path[len(self.settings.STATIC_URL):]
            content_type = self.get_content_type(file_path)
            binary_data, status = self.get_static(self.settings.STATIC_FILES_DIR, file_path)
        else:
            data, status = response_404(request)
            binary_data = data.encode(encoding='utf-8')

        start_response(status, [
            ("Content-Type", content_type),
            # ("Content-Length", str(len(data))),
            ("CUSTOM_HEADER", request.get("header"))  # добавляем значение из middleware
        ])

        return [binary_data]

    @staticmethod
    def fix_url_slash(path: str):
        """
        Adds slash at the end of path
        """
        if path[-1] != '/':
            path += '/'
        return path

    @staticmethod
    def get_static(static_dir, file_path):
        # TODO define root dir in settings
        path_to_file = path.join(static_dir, file_path)
        print(path_to_file, getcwd())
        with open(path_to_file, 'rb') as f:
            file_content = f.read()
        status_code = '200 OK'
        return file_content, status_code

    @staticmethod
    def get_content_type(file_path, content_types_map=CONTENT_TYPES_MAP):
        file_name = path.basename(file_path).lower()
        media_type = content_types_map.get(file_name, None)
        if media_type is not None:
            return media_type
        extension = path.splitext(file_name)[1]
        return content_types_map.get(extension, "text/plain")


def response_404(request):
    content_text = 'Gunicorn cannot find the page you looking for'
    status_code = '404 NOT FOUNDED'
    return content_text, status_code


if __name__ == '__main__':
    import crabs_project.settings as settings
    from crabs_project.urls import router
    from crabs_project.middleware import middleware_list
    app = App(settings, routes=router, middleware=middleware_list)

