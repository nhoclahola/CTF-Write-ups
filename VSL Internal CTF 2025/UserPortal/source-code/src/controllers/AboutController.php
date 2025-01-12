<?php
require_once 'BaseController.php';

class AboutController extends BaseController
{
    public function index()
    {
        $this->render('about');
    }
}
?>