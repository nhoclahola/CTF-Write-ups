<?php
require_once __DIR__ . '/../includes/init.php';

class Database
{
    private $pdo;

    public function __construct()
    {
        $host = getenv('DB_HOST');
        $dbname = getenv('DB_NAME');
        $username = getenv('DB_USER');
        $password = getenv('DB_PASSWORD');

        try {
            $this->pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
            $this->pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        } catch (PDOException $e) {
            die("Database connection failed: " . $e->getMessage());
        }
    }

    public function getConnection()
    {
        return $this->pdo;
    }
}

class AuthController
{
    private $db;

    public function __construct()
    {
        $this->db = (new Database())->getConnection();
    }

    public function login()
    {
        header('Content-Type: application/json');
        $response = ['success' => false, 'message' => ''];

        $username = isset($_POST['username']) ? trim($_POST['username']) : '';
        $password = isset($_POST['password']) ? $_POST['password'] : '';
        $username = htmlspecialchars(strip_tags($username));
        $password = htmlspecialchars(strip_tags($password));
        $sql = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";

        try {
            $stmt = $this->db->query($sql);
            $user = $stmt->fetch(PDO::FETCH_ASSOC);

            if ($user) {
                $_SESSION['loggedin'] = true;
                $_SESSION['username'] = $user['username'];
                $response['success'] = true;
                $response['message'] = 'Login successful.';
            } else {
                $response['message'] = 'Invalid username or password.';
            }
        } catch (PDOException $e) {
            $response['message'] = 'An error occurred: ' . $e->getMessage();
        }

        echo json_encode($response);
        exit();
    }

    public function logout()
    {
        header('Content-Type: application/json');
        $response = ['success' => false, 'message' => ''];

        if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true) {
            $_SESSION = [];
            session_destroy();
            $response['success'] = true;
            $response['message'] = 'Logged out successfully.';
        } else {
            $response['message'] = 'You are not logged in.';
        }

        echo json_encode($response);
        exit();
    }
}
?>