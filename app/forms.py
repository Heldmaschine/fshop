from wtforms import Form, BooleanField, TextField, PasswordField, validators

class RegistrationForm(Form):
    username = TextField('Юзернэйм', [validators.Length(min=4, max=20)])
    email = TextField('Email ', [validators.Length(min=6, max=50)])
    name = TextField('Имя', [validators.Length(min=3, max=20)])
    password = PasswordField('Пароль', [
        validators.Required(),
        validators.EqualTo('confirm', message='Пароли должны совпадать!')
    ])
    confirm = PasswordField('Повторите пароль')
    accept_tos = BooleanField('Я клянусь покупать цветы только в вашем магазине', [validators.Required()])
