# app.py

from flask import Flask, request, render_template, jsonify, make_response, session
import uuid
import random
from flask_session import Session
import io
import contextlib
from multiprocessing import Process, Queue
import ast
import hashlib
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-very-secure-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

FLAG_PATH = 'flag.txt'

ALLOWED_MODULES = {
    'abc',
    'aifc',
    'argparse',
    'array',
    'ast',
    'audioop',
    'base64',
    'calendar',
    'cmath',
    'code',
    'codecs',
    'copy',
    'copyreg',
    'dataclasses',
    'datetime',
    'decimal',
    'difflib',
    'email',
    'email.mime',
    'email.message',
    'email.utils',
    'enum',
    'fractions',
    'functools',
    'gettext',
    'glob',
    'gzip',
    'hashlib',
    'heapq',
    'hmac',
    'html',
    'html.parser',
    'http',
    'http.client',
    'http.server',
    'imghdr',
    'inspect',
    'io',
    'ipaddress',
    'itertools',
    'json',
    'json.decoder',
    'json.encoder',
    'keyword',
    'linecache',
    'locale',
    'logging',
    'logging.handlers',
    'math',
    'mimetypes',
    'pathlib',
    'pprint',
    'profile',
    'pstats',
    'py_compile',
    'pydoc',
    'pydoc_data',
    'queue',
    'quopri',
    'random',
    're',
    'reprlib',
    'sched',
    'secrets',
    'shelve',
    'shlex',
    'sre_compile',
    'sre_constants',
    'sre_parse',
    'stat',
    'statistics',
    'string',
    'stringprep',
    'struct',
    'tarfile',
    'textwrap',
    'timeit',
    'tokenize',
    'traceback',
    'tracemalloc',
    'turtle',
    'types',
    'typing',
    'unicodedata',
    'unittest',
    'unittest.mock',
    'urllib',
    'urllib.parse',
    'urllib.request',
    'uu',
    'uuid',
    'venv',
    'warnings',
    'wave',
    'weakref',
    'webbrowser',
    'xml',
    'xml.etree.ElementTree',
    'xml.dom',
    'xml.sax',
    'xmlrpc',
    'xmlrpc.client',
    'xmlrpc.server',
    'zipapp',
    'zipfile',
    'zipimport',
    'zlib',
    'xml.sax.handler',
    'xml.sax.expatreader',
    'xml.dom.minidom',
    'xml.dom.pulldom',
    'json.tool',
    'email.mime.text',
    'email.mime.multipart',
    'email.mime.base',
    'email.mime.image',
    'email.mime.audio',
    'email.mime.application',
    'http.server.SimpleHTTPRequestHandler',
    'http.server.HTTPServer',
    'http.client.HTTPConnection',
    'http.client.HTTPSConnection',
    'urllib.error',
    'urllib.parse.urlparse',
    'urllib.parse.urljoin',
    'urllib.request.urlopen',
}

FORBIDDEN_FUNCTIONS = {'exec', 'eval', 'compile', 'open', 'input'}


def hash_captcha(value):
    return hashlib.sha256((value + app.config['SECRET_KEY']).encode()).hexdigest()


def generate_execution_id():
    return str(uuid.uuid4())


def limited_import(name, globals=None, locals=None, fromlist=(), level=0):
    if level != 0:
        raise ImportError("Relative imports are not allowed.")

    if name not in ALLOWED_MODULES:
        raise ImportError(f"Import of module '{name}' is not allowed.")

    return __import__(name, globals, locals, fromlist, level)


def is_code_safe(user_code):
    try:
        tree = ast.parse(user_code, mode='exec')
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                if alias.name not in ALLOWED_MODULES:
                    return False, f"Import of module '{alias.name}' is not allowed."
        elif isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                func_name = func.id
                if func_name in FORBIDDEN_FUNCTIONS:
                    return False, f"Use of '{func_name}' is not allowed."
            elif isinstance(func, ast.Attribute):
                attr_name = func.attr
                if attr_name in FORBIDDEN_FUNCTIONS:
                    return False, f"Use of '{attr_name}' is not allowed."
        elif isinstance(node, ast.Attribute):
            if node.attr.startswith('__') and node.attr.endswith('__'):
                return False, "Access to special attributes is forbidden."

    return True, "Code is safe"


def execute_code(user_code, queue):
    is_safe, message = is_code_safe(user_code)
    if not is_safe:
        queue.put({'output': f"Security Error: {message}"})
        return

    try:
        buffer = io.StringIO()
        allowed_builtins = {
            'abs': abs,
            'all': all,
            'any': any,
            'bool': bool,
            'chr': chr,
            'divmod': divmod,
            'float': float,
            'int': int,
            'len': len,
            'max': max,
            'min': min,
            'pow': pow,
            'range': range,
            'str': str,
            'sum': sum,
            'print': lambda *args, **kwargs: print(*args, **kwargs, file=buffer),
            '__import__': limited_import
        }
        exec_globals = {
            '__builtins__': allowed_builtins,
        }
        exec_locals = {}
        with contextlib.redirect_stdout(buffer):
            exec(user_code, exec_globals, exec_locals)
        output = buffer.getvalue()
        queue.put({'output': output})
    except Exception as e:
        queue.put({'output': f"Runtime Error: {e}"})


def run_with_timeout(user_code, timeout=5):
    queue = Queue()
    p = Process(target=execute_code, args=(user_code, queue))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        return "Error: Execution timed out."
    if not queue.empty():
        return queue.get()['output']
    return "Error: No output."


def generate_captcha():
    operators = ['+', '-']
    num_operands = random.randint(5, 10)
    expression = "What is "
    operands = [str(random.randint(100, 999)) for _ in range(num_operands)]
    ops = [random.choice(operators) for _ in range(num_operands - 1)]
    expression += ' '.join([val for pair in zip(operands, ops + [''])
                           for val in pair if val])
    try:
        answer = str(eval(expression.replace("What is ", "").replace("?", "")))
    except Exception:
        return generate_captcha()
    return expression, answer


@app.route('/', methods=['GET'])
def index():
    question, answer = generate_captcha()
    hashed_captcha = hash_captcha(answer)
    response = make_response(render_template(
        'index.html', captcha_question=question))
    response.set_cookie('captcha_hash', hashed_captcha,
                        httponly=True, samesite='Strict')
    return response


@app.route('/get_captcha', methods=['GET'])
def get_captcha():
    question, answer = generate_captcha()
    hashed_captcha = hash_captcha(answer)
    response = jsonify({'question': question})
    response.set_cookie('captcha_hash', hashed_captcha,
                        httponly=True, samesite='Strict')
    return response


@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    user_code = data.get('code', '')
    user_captcha = data.get('captcha', '').strip()
    hashed_captcha = request.cookies.get('captcha_hash')
    if not user_captcha:
        return jsonify({'success': False, 'error': 'CAPTCHA is required.'}), 400

    if hash_captcha(user_captcha) != hashed_captcha:
        question, answer = generate_captcha()
        new_hashed_captcha = hash_captcha(answer)
        response = jsonify(
            {'success': False, 'error': 'Incorrect CAPTCHA. Please try again.'})
        response.set_cookie('captcha_hash', new_hashed_captcha,
                            httponly=True, samesite='Strict')
        return response, 400
    execution_id = generate_execution_id()
    output = run_with_timeout(user_code)
    question, answer = generate_captcha()
    new_hashed_captcha = hash_captcha(answer)
    response = jsonify({'success': True, 'id': execution_id, 'output': output})
    response.set_cookie('captcha_hash', new_hashed_captcha,
                        httponly=True, samesite='Strict')
    return response, 200


@app.route("/snippets", methods=["GET"])
def get_snippets():
    snippets = [
        {"name": "Print 'Hello, World!'", "code": "print('Hello, World!')"},
        {"name": "For Loop", "code": "for i in range(5):\n    print(i)"},
        {"name": "Function: Add Numbers",
            "code": "def add(a, b):\n    return a + b"},
        {"name": "Sum of List",
            "code": "numbers = [1, 2, 3, 4, 5]\nprint(sum(numbers))"},
        {"name": "Try-Except Block",
            "code": "try:\n    x = 1 / 0\nexcept ZeroDivisionError:\n    print('Cannot divide by zero!')"},
        {"name": "Class Definition",
            "code": "class Animal:\n    def __init__(self, name):\n        self.name = name"},
        {"name": "Math Library", "code": "import math\nprint(math.sqrt(16))"},
        {"name": "File Handling",
            "code": "with open('file.txt', 'r') as file:\n    print(file.read())"},
        {"name": "String Uppercase",
            "code": "text = 'hello world'\nprint(text.upper())"},
        {"name": "Generate Random Number",
            "code": "import random\nprint(random.randint(1, 100))"},
        {"name": "Current Date and Time",
            "code": "import datetime\nprint(datetime.datetime.now())"},
        {"name": "Matrix Print",
            "code": "matrix = [[1, 2], [3, 4]]\nfor row in matrix:\n    print(row)"},
        {"name": "Character Count",
            "code": "from collections import Counter\nprint(Counter('banana'))"},
        {"name": "List Comprehension",
            "code": "nums = [1, 2, 3, 4]\ndoubled = [x * 2 for x in nums]\nprint(doubled)"},
        {"name": "Get Current Directory",
            "code": "import os\nprint(os.getcwd())"},
        {"name": "Recursive Function",
            "code": "def factorial(n):\n    return 1 if n == 0 else n * factorial(n-1)\nprint(factorial(5))"},
        {"name": "Generate Permutations",
            "code": "from itertools import permutations\nprint(list(permutations([1, 2, 3])))"},
        {"name": "Dictionary Access",
            "code": "data = {'name': 'Alice', 'age': 25}\nprint(data.get('name'))"},
        {"name": "Sort List",
            "code": "numbers = [5, 3, 8, 6]\nprint(sorted(numbers))"},
        {"name": "Regex Search",
            "code": "import re\nmatch = re.search(r'\\d+', 'Order 66')\nprint(match.group())"},
    ]
    return jsonify(snippets)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1003, debug=False)
