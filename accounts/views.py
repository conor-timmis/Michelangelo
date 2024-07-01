from allauth.account.views import LoginView, SignupView

class LoginView(LoginView):
    template_name = 'my_login.html'

class SignupView(SignupView):
    template_name = 'my_signup.html'
