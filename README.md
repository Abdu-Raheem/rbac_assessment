# Role-Based Access Control (RBAC) System

**Description:**  
This project is an implementation of a Role-Based Access Control (RBAC) system using Django REST Framework (DRF). It includes user authentication, role management, and restricted access to resources based on roles (e.g., Admin and Moderator).
You can access the API through https://rbac-vrv-ten.vercel.app/api/ and test the APIs using POSTMAN. Please check the API Documentation at https://rbac-vrv-ten.vercel.app/ and the superadmin username : admin and password : 123
---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Models](#models)
- [Views](#views)
- [Serializers](#serializers)
- [Swagger API Documentation](#swagger-api-documentation)
- [Permissions](#permissions)
- [Usage](#usage)

---

## Features

- **User Registration**: Users can register with a username, password, and email.
- **JWT Authentication**: Token-based authentication with login, logout, and token refresh endpoints.
- **Role Management**: Assign roles to users to restrict access to specific endpoints.
- **Role-Based Views**: Dedicated views for Admin and Moderator users with access restrictions.
- **API Documentation**: Swagger UI integration for easy API exploration.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Abdu-Raheem/rbac_assessment.git
   cd rbac_assessment
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate   # On Windows: .\env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

---

## API Endpoints

### Authentication

| Endpoint              | Method | Description                     |
|-----------------------|--------|---------------------------------|
| `/api/register/`      | POST   | Register a new user            |
| `/api/login/`         | POST   | Login and obtain JWT tokens    |
| `/api/token/refresh/` | POST   | Refresh JWT tokens             |
| `/api/logout/`        | POST   | Logout and blacklist tokens    |

### Role-Based Endpoints

| Endpoint                  | Method | Description                     |
|---------------------------|--------|---------------------------------|
| `/api/admin/dashboard/`   | GET    | Access Admin Dashboard         |
| `/api/moderator/tools/`   | GET    | Access Moderator Tools         |

---

## Models

### Role Model

```python
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
```

### User Model

```python
class User(AbstractUser):
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
    )
```

---

## Views

### Register View

Handles user registration.  
**URL**: `/api/register/`  
**Method**: POST

```python
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Logout View

Handles user logout and token blacklisting.  
**URL**: `/api/logout/`  
**Method**: POST

```python
class LogoutView(APIView):
    def post(self, request):
        token = RefreshToken(request.data.get("refresh"))
        token.blacklist()
        return Response({"message": "User logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
```

### Admin Dashboard View

Provides restricted access to Admin users.  
**URL**: `/api/admin/dashboard/`  
**Method**: GET

```python
class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        return Response({"message": "Welcome to the Admin Dashboard"}, status=status.HTTP_200_OK)
```

### Moderator Tools View

Provides restricted access to Moderator users.  
**URL**: `/api/moderator/tools/`  
**Method**: GET

```python
class ModeratorToolsView(APIView):
    permission_classes = [IsAuthenticated, IsModeratorUser]

    def get(self, request):
        return Response({"message": "Welcome to the Moderator Tools"}, status=status.HTTP_200_OK)
```

---

## Serializers

### Register Serializer

Used for user registration.

```python
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
```

---

## Swagger API Documentation

Swagger UI is integrated into the project for API exploration.  
Access it at the root URL (`/`).

**Key Features**:
- Interactive API testing
- Auto-generated documentation from DRF views and serializers

---

## Permissions

Custom permissions are defined for role-based access:

- **IsAdminUser**: Grants access to Admin endpoints.
- **IsModeratorUser**: Grants access to Moderator endpoints.

---

## Usage

### Register a New User

**Endpoint**: `/api/register/`  
**Method**: POST  
**Payload**:
```json
{
    "username": "example",
    "password": "password123",
    "email": "example@example.com"
}
```

### Login and Obtain JWT Tokens

**Endpoint**: `/api/login/`  
**Method**: POST  
**Payload**:
```json
{
    "username": "example",
    "password": "password123"
}
```

**Response**:
```json
{
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}
```
