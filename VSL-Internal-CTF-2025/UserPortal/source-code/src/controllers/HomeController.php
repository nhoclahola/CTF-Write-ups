<?php
require_once 'BaseController.php';

class HomeController extends BaseController
{
    public function index()
    {
        $this->render('home');
    }
}
?>