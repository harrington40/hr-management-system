from helperFuns import imagePath
from assets import RemoveOverPadding, SildeFromTop, SlideFromBottom, Wave_AnimationCSS, ZoomIn
from components.authencation.authHelper import generate_magic_link
import asyncio

from nicegui import ui, html, app
from datetime import datetime

def Login_Page():
    ZoomIn()
    RemoveOverPadding()
    with ui.grid(columns=12).style('height: 100dvh; width: 100dvw').classes('gap-0 overflow-hidden'):
        with ui.element('div').classes('flex items-center justify-center col-span-12 md:col-span-3 lg:col-span-4 bg-gradient-to-t from-blue-200 to-blue-50'):
            Wave_AnimationCSS()
            with ui.element('div').classes('waves-block'):
                    html.div().classes('waves wave-1')
                    html.div().classes('waves wave-2')
                    html.div().classes('waves wave-3')
                    html.div().classes('waves wave-4')
            with ui.card().tight().classes('zoom-in pb-12 w-full mx-24 px-10 rounded-xl pt-6'):
                ui.image(imagePath('holder.gif')).classes('flex justify-center mx-auto w-20 h-20')
                html.p('Sign In').classes('text-2xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-blue-800 to-blue-900 pb-6')
                html.span('Email*').classes('text-sm font-medium pl-1')
                email = ui.input(placeholder='Enter your email', validation=lambda value: 'Email is required!' if not value else None).props('dense outlined type="email" bg-color="blue-1" input-class="text-sm"').classes('pb-8 w-full') #.on("blur", lambda e: e.sender.validate())
                html.span('Password*').classes('text-sm font-medium pl-1')
                password = ui.input(password=True, password_toggle_button=True, placeholder='Enter your password', validation=validate_name).props('dense outlined bg-color="blue-1" input-class="text-sm"').classes('w-full') #.on("blur", lambda e: e.sender.validate())
                with ui.row().classes('grid grid-flow-col justify-items-end -mt-4 mb-4 w-full'):
                    ui.label('Forgot').classes('font-medium text-blue-600 hover:text-blue-800 -mr-16')
                    ui.label('Password?').classes('font-semibold text-blue-600 hover:text-blue-800 cursor-pointer -ml-[5rem]')
                submit_btn = ui.button('Login', on_click=lambda: handleSubmit([email, password], submit_btn, email.value)).props(f'rounded').classes('mt-6 w-full font-bold') #.bind_enabled_from(checker, 'no_errors')
                # Development bypass button for testing
                ui.button('Dev Login (Testing)', on_click=dev_login).props('outlined color=orange').classes('mt-2 w-full text-xs')
                # ui.label(f'{progress['isLoading']}').classes('text-red-200')
        with ui.image(f'{imagePath('bg.jpg')}').classes('lg:block bg-fixed md:col-span-9 lg:col-span-8'):
            SlideFromBottom()
            SildeFromTop()
            with ui.element('div').classes('mx-10 mt-14 bg-transparent flex flex-col h-full'):
                html.span('HR MANAGEMENT Kit').classes('fadeIn-top text-4xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-blue-800 to-blue-900')
                html.span('Seamlessly handle all HR related functions and actionable insights from time and attendance management to employee performance, turnover and relevant data trends for facilitating effective decision-makings, all from one place').classes('fadeIn-bottom w-3/5 text-lg bg-clip-text text-transparent bg-gradient-to-l from-blue-500 to-blue-600 my-2')
                with html.span(f' © 2011 - {datetime.now().year} Copyright:').classes('flex text-sm font-medium absolute bottom-20 left-6 text-blue-100'):
                    ui.html('<a href="https://kwarecominc.com/" target="_blank" rel="noreferrer" class="pl-2 text-blue-300"> <strong className="font-semibold"> KWARECOM Inc.</strong></a>', sanitize=False)

async def handleSubmit(inputField: list[ui.input], subminBtn: ui.button, email: str):
    isValid = True
    subminBtn.props('loading').disable()
    subminBtn.add_slot('loading', r'''
            <q-spinner-facebook /> Please Wait...
        ''')
    for field in inputField:
        if not field.validate():
            isValid = False
            ui.notify('Please correct the errors in the form!', color='negative')
            break
    if isValid:
        try:
            await generate_magic_link(email)
            ui.notify(f'Magic link sent to {email}! Please check your email.', color='positive')
        except Exception as e:
            ui.notify('Failed to send email. Please try again.', color='negative')
    await asyncio.sleep(5)
    subminBtn.props(remove='loading')
    subminBtn.enable()

async def dev_login():
    """Development login bypass for testing"""
    try:
        from .authHelper import create_dev_auth_token
        token = create_dev_auth_token("dev@hrmkit.com")
        app.storage.user.update({'token': token, 'authenticated': True})
        ui.notify('Development login successful!', color='positive')
        ui.navigate.to('/dashboard')
    except Exception as e:
        ui.notify(f'Development login failed: {str(e)}', color='negative')

def validate_name(value):
    if not value:
        return 'Password is required!'
    elif len(value) < 3:
        return 'Name must be at least 3 characters long.'
    return None