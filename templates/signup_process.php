<?php
// Establish a database connection
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "chatbotx";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Process the sign-up form submission
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST["email"];
    $password = $_POST["password"];
    $confirm_password = $_POST["confirm_password"];

    // Check if the passwords match
    if ($password != $confirm_password) {
        echo "Passwords do not match.";
        exit;
    }

    // Check if the email is already registered
    $sql = "SELECT * FROM user_info WHERE email=?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("s", $email);
    $stmt->execute();
    $result = $stmt->get_result();
    if ($result->num_rows > 0) {
        echo "Email already registered.";
        exit;
    }

    // Hash the password
    $Password = password_hash($password, PASSWORD_DEFAULT);

    // Insert the user into the database
    $sql = "INSERT INTO user_info (email, password) VALUES (?, ?)";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ss", $email, $Password);
    if ($stmt->execute()) {
        echo "<script>alert('Sign up successful!'); window.location.href = 'login.html';</script>";
        exit;
    } else {
        echo "Error: " . $stmt->error;
    }
}

$conn->close();
?>