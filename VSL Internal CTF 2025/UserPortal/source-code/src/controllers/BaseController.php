<?php
class BaseController
{
    protected function render($view, $data = [])
    {
        extract($data);
        require_once __DIR__ . '/../includes/header.php';
        require_once __DIR__ . '/../views/' . $view . '.php';
        require_once __DIR__ . '/../includes/footer.php';
    }
}
?>