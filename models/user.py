from werkzeug.security import generate_password_hash

# In a real application, this data should be stored in a database
users = {
    "user1": generate_password_hash("password1"),
    "user2": generate_password_hash("password2")
}
