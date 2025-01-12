<?php
require_once 'BaseController.php';
require_once __DIR__ . '/../includes/functions.php';
class FeedbackController extends BaseController
{
    private $functions;
    public function __construct()
    {
        $this->functions = new Functions();
    }
    public function index()
    {
        if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] !== true) {
            header("Location: index.php?page=home");
            exit();
        }

        $feedback = "";
        $success = "";
        $error = "";

        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $feedback = trim($_POST['feedback']);

            if (strlen($feedback) > 500) {
                $error = "Feedback is too long.";
            } elseif (!empty($feedback)) {
                try {
                    $output = $this->functions->render_template("User Feedback: $feedback", $variables = []);
                    $success = $output;
                } catch (Exception $e) {
                    $error = "An error occurred while processing your feedback.";
                }
            } else {
                $error = "Feedback cannot be empty.";
            }
        }

        $data = [
            'feedback' => $feedback,
            'success' => $success,
            'error' => $error
        ];

        $this->render('feedback', $data);
    }
}
?>