from flask_restx import Namespace, fields

class AuthNamespace(Namespace):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.email_field = fields.String(default="jane.smith@example.com", format="email", required=True)
        self.password_field = fields.String(default="password123", format="password", required=True)
        self.updated_password_field = fields.String(default="newpassword123", required=True)

    def get_auth_fields(self):
        return self.model('UserAuthentication', {
            "email": self.email_field,
            "password": self.password_field
        })

    def get_send_code_fields(self):
        return self.model("UserSendCode", {
            "email": self.email_field
        })

    def get_reset_pw_fields(self):
        return self.model("UserResetPassword", {
            "email": self.email_field,
            "reset_code": fields.String(default="XXXXXXXX", required=True),
            "updated_password": self.updated_password_field
        })

    def get_change_pw_fields(self):
        return self.model("UserChangePassword", {
            "email": self.email_field,
            "password": self.password_field,
            "updated_password": self.updated_password_field
        })
