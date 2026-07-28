from src.auth.models import create_user, get_user_by_email

# Create a test user
create_user(
    "Raj",
    "raj@example.com",
    "123456"
)

user = get_user_by_email("raj@example.com")

print(dict(user))