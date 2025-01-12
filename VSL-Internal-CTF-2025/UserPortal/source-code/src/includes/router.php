<?php
require_once __DIR__ . '/../includes/init.php';
function routeRequest($page)
{
    $routes = [
        'home' => ['controller' => 'HomeController', 'action' => 'index'],
        'about' => ['controller' => 'AboutController', 'action' => 'index'],
        'feedback' => ['controller' => 'FeedbackController', 'action' => 'index'],
        'login' => ['controller' => 'AuthController', 'action' => 'login'],
        'logout' => ['controller' => 'AuthController', 'action' => 'logout'],
        'profile' => ['controller' => 'ProfileController', 'action' => 'index'],
    ];
    $isAjax = !empty($_SERVER['HTTP_X_REQUESTED_WITH']) &&
        strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) == 'xmlhttprequest';
    if ($isAjax && isset($_POST['action']) && in_array($_POST['action'], ['login', 'logout'])) {
        $action = $_POST['action'];
        if ($action === 'login' || $action === 'logout') {
            $controllerName = $routes[$action]['controller'];
            $actionName = $routes[$action]['action'];
            $controllerFile = __DIR__ . '/../controllers/' . $controllerName . '.php';
            if (file_exists($controllerFile)) {
                require_once $controllerFile;
            } else {
                header("HTTP/1.0 404 Not Found");
                echo json_encode(['success' => false, 'message' => 'Controller not found.']);
                exit();
            }
            if (class_exists($controllerName)) {
                $controller = new $controllerName();
                if (method_exists($controller, $actionName)) {
                    $controller->$actionName();
                } else {
                    header("HTTP/1.0 404 Not Found");
                    echo json_encode(['success' => false, 'message' => 'Action not found.']);
                    exit();
                }
            } else {
                header("HTTP/1.0 404 Not Found");
                echo json_encode(['success' => false, 'message' => 'Controller class does not exist.']);
                exit();
            }
        }
    }
    if (isset($_GET['page'])) {
        $page = $_GET['page'];
    } else {
        $page = 'home';
    }
    if (!array_key_exists($page, $routes)) {
        $page = 'home';
    }

    $controllerName = $routes[$page]['controller'];
    $actionName = $routes[$page]['action'];
    $controllerFile = __DIR__ . '/../controllers/' . $controllerName . '.php';
    if (file_exists($controllerFile)) {
        require_once $controllerFile;
    } else {
        header("HTTP/1.0 404 Not Found");
        echo "404 Not Found - Controller does not exist.";
        exit();
    }
    if (class_exists($controllerName)) {
        $controller = new $controllerName();
        if (method_exists($controller, $actionName)) {
            $controller->$actionName();
        } else {
            header("HTTP/1.0 404 Not Found");
            echo "404 Not Found - Action does not exist.";
            exit();
        }
    } else {
        header("HTTP/1.0 404 Not Found");
        echo "404 Not Found - Controller class does not exist.";
        exit();
    }
}
?>