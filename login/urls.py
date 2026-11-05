from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("perfil/", views.perfil, name="perfil"),
    path("alterar-senha/", auth_views.PasswordChangeView.as_view(template_name="alterar_senha.html", success_url="/login/perfil/"), name="alterar_senha"),
    path("esqueci-senha/", auth_views.PasswordResetView.as_view(template_name="esqueci_senha.html", email_template_name="esqueci_senha_email.html", subject_template_name="esqueci_senha_assunto.txt", success_url="/login/esqueci-senha-enviada/"), name="password_reset"), 
    path("esqueci-senha-enviada/", auth_views.PasswordResetDoneView.as_view(template_name="esqueci_senha_enviada.html"), name="password_reset_done"), 
    path("redefinir-senha/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="redefinir_senha.html", success_url="/login/senha-redefinida/"), name="password_reset_confirm"), 
    path("senha-redefinida/", auth_views.PasswordResetCompleteView.as_view(template_name="senha_redefinida.html"), name="password_reset_complete"),
    path('cadastro/', views.cadastro, name='cadastro'),
]