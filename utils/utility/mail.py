from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import send_mail


class MailAuthenticateUser:
    pass

    def mail(
        self,
        subject: str = "",
        html_template_data: tuple[str, dict] = None,
        from_email=None,
        to: list = None
    ):
        html_message = render_to_string(
            html_template_data[0], html_template_data[1])
        plain_message = strip_tags(html_message)

        send_mail(subject, plain_message, from_email,
                  to, html_message=html_message)
