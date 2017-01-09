"""Helper forms which make handling common operations simpler."""


from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms.fields import BooleanField, HiddenField, PasswordField, StringField
from wtforms.validators import Email, EqualTo, InputRequired, ValidationError


class RegistrationForm(FlaskForm):
    """
    Register a new user.

    This class is used to provide safe user registration.  The only required
    fields are `email` and `password` -- everything else is optional (and can
    be configured by the developer to be used or not).

    .. note::
        This form only includes the fields that are available to register
        users with Stormpath directly -- this doesn't include support for
        Stormpath's social login stuff.

        Since social login stuff is handled separately (registration happens
        through Javascript) we don't need to have a form for registering users
        that way.
    """
    username = StringField('Username')
    given_name = StringField('First Name')
    middle_name = StringField('Middle Name')
    surname = StringField('Last Name')
    email = StringField('Email', validators=[
        InputRequired('You must provide an email address.'),
        Email('You must provide a valid email address.')
    ])
    password = PasswordField('Password', validators=[InputRequired('You must supply a password.')])

    def __init__(self, formdata=_Auto, config=None **kwargs):
        super(RegistrationForm, self).__init__(formdata=formdata, **kwargs)

        if config:
            if config['STORMPATH_ENABLE_USERNAME'] and config['STORMPATH_REQUIRE_USERNAME']:
                self.username.validators.append(InputRequired('Username is required.'))

            if config['STORMPATH_ENABLE_GIVEN_NAME'] and config['STORMPATH_REQUIRE_GIVEN_NAME']:
                self.given_name.validators.append(InputRequired('First name is required.'))

            if config['STORMPATH_ENABLE_MIDDLE_NAME'] and config['STORMPATH_REQUIRE_MIDDLE_NAME']:
                self.middle_name.validators.append(InputRequired('Middle name is required.'))

            if config['STORMPATH_ENABLE_SURNAME'] and config['STORMPATH_REQUIRE_SURNAME']:
                self.surname.validators.append(InputRequired('Surname is required.'))


class AcceptTermsRegistrationForm(RegistrationForm):
    accept = BooleanField(validators=[InputRequired('You have to accept the terms and conditions in order to use the bulletin board.')])


class LoginForm(FlaskForm):
    """
    Log in an existing user.

    This class is used to provide safe user login.  A user can log in using
    a login identifier (either email or username) and password.  Stormpath
    handles the username / email abstractions itself, so we don't need any
    special logic to handle those cases.

    .. note::
        This form only includes the fields that are available to log users in
        with Stormpath directly -- this doesn't include support for Stormpath's
        social login stuff.

        Since social login stuff is handled separately (login happens through
        Javascript) we don't need to have a form for logging in users that way.
    """
    login = StringField('Login', validators=[InputRequired('Login identifier required.')])
    password = PasswordField('Password', validators=[InputRequired('Password required.')])


class ForgotPasswordForm(FlaskForm):
    """
    Retrieve a user's email address for initializing the password reset
    workflow.

    This class is used to retrieve a user's email address.
    """
    email = StringField('Email', validators=[
        InputRequired('Email address required.'),
        Email('You must provide a valid email address.')
    ])


class ChangePasswordForm(FlaskForm):
    """
    Change a user's password.

    This class is used to retrieve a user's password twice to ensure it's valid
    before making a change.
    """
    password = PasswordField('Password', validators=[InputRequired('Password required.')])
    password_again = PasswordField('Password (again)', validators=[
        InputRequired('Please verify the password.'),
        EqualTo('password', 'Passwords do not match.')
    ])

class ChangePasswordFormHref(ChangePasswordForm):
    href = HiddenField('Href')

class ResendVerificationForm(FlaskForm):
    username = HiddenField('Username')
