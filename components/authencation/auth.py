import asyncio
import time
from nicegui import ui, html, app, context
from datetime import datetime

from helperFuns import imagePath
from assets import RemoveOverPadding, SildeFromTop, SlideFromBottom, Wave_AnimationCSS, ZoomIn
from .authHelper import create_dev_auth_token, generate_magic_link

def Login_Page():
    # Check if user is already authenticated, redirect to dashboard
    try:
        if context.client.storage.user.get('authenticated', False):
            ui.navigate.to('/hrmkit/reporting/dashboard')
            return
    except:
        pass
    
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
                password = ui.input(password=True, password_toggle_button=True, placeholder='Enter your password', validation=validate_password).props('dense outlined bg-color="blue-1" input-class="text-sm"').classes('w-full') #.on("blur", lambda e: e.sender.validate())
                with ui.row().classes('grid grid-flow-col justify-items-end -mt-4 mb-4 w-full'):
                    ui.label('Forgot').classes('font-medium text-blue-600 hover:text-blue-800 -mr-16')
                    ui.label('Password?').classes('font-semibold text-blue-600 hover:text-blue-800 cursor-pointer -ml-[5rem]')
                submit_btn = ui.button('Login', on_click=lambda: handleSubmit([email, password], submit_btn, email.value, password.value)).props(f'rounded').classes('mt-6 w-full font-bold') #.bind_enabled_from(checker, 'no_errors')
               
                ui.button('Send Magic Link', on_click=lambda: send_magic_link(email.value)).props('outlined color=purple').classes('mt-2 w-full')
                ui.button('Dev Login (Testing)', on_click=dev_login).props('outlined color=orange').classes('mt-2 w-full text-xs')
        with ui.image(f'{imagePath('bg.jpg')}').classes('lg:block bg-fixed md:col-span-9 lg:col-span-8'):
            SlideFromBottom()
            SildeFromTop()
            with ui.element('div').classes('mx-10 mt-14 bg-transparent flex flex-col h-full'):
                html.span('HR MANAGEMENT Kit').classes('fadeIn-top text-4xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-blue-800 to-blue-900')
                html.span('Seamlessly handle all HR related functions and actionable insights from time and attendance management to employee performance, turnover and relevant data trends for facilitating effective decision-makings, all from one place').classes('fadeIn-bottom w-3/5 text-lg bg-clip-text text-transparent bg-gradient-to-l from-blue-500 to-blue-600 my-2')
                with html.span(f' © 2011 - {datetime.now().year} Copyright:').classes('flex text-sm font-medium absolute bottom-20 left-6 text-blue-100'):
                    ui.html('<a href="https://kwarecominc.com/" target="_blank" rel="noreferrer" class="pl-2 text-blue-300"> <strong className="font-semibold"> KWARECOM Inc.</strong></a>')

async def handleSubmit(inputField: list[ui.input], subminBtn: ui.button, email: str, password: str):
    isValid = True
    subminBtn.props('loading').disable()
    subminBtn.add_slot('loading', r'''
            <q-spinner-facebook /> Please Wait...
        ''')

    # Validate email
    if not email or '@' not in email:
        ui.notify('Please enter a valid email address!', color='negative')
        isValid = False

    # Validate password
    if not password or len(password) < 3:
        ui.notify('Password must be at least 3 characters!', color='negative')
        isValid = False

    if isValid:
        try:
            # For now, just send magic link if email/password are provided
            # In production, you'd validate against database here
            response = await generate_magic_link(email)
            if response.status_code == 200:
                ui.notify(f'Magic link sent to {email}! Please check your email.', color='positive')
            else:
                ui.notify('Failed to send email. Please try again.', color='negative')
        except Exception as e:
            ui.notify('Failed to send email. Please try again.', color='negative')
    else:
        # Re-enable button if validation failed
        subminBtn.props(remove='loading')
        subminBtn.enable()
        return

    await asyncio.sleep(3)
    subminBtn.props(remove='loading')
    subminBtn.enable()

async def dev_login():
    """Development login bypass for testing"""
    try:
        from .authHelper import create_jwt_token
        
        # Create a dev user token
        user_data = {
            "email": "dev@hrmkit.com",
            "username": "Developer",
            "timestamp": str(int(time.time()))
        }
        
        token = create_jwt_token(user_data)
        
        # Store authentication in context
        context.client.storage.user.update({
            'token': token, 
            'authenticated': True,
            'username': user_data['username'],
            'email': user_data['email']
        })
        
        ui.notify('Development login successful!', color='positive')
        ui.navigate.to('/hrmkit/reporting/dashboard')
    except Exception as e:
        ui.notify(f'Development login failed: {str(e)}', color='negative')

def validate_password(value):
    if not value:
        return 'Password is required!'
    elif len(value) < 3:
        return 'Password must be at least 3 characters!'

async def send_magic_link(email: str):
    if not email:
        ui.notify('Please enter your email address', color='negative')
        return
    try:
        print(f"Attempting to send magic link to: {email}")
        response = await generate_magic_link(email)
        print(f"Response: {response}")

        # Check if response indicates success
        if hasattr(response, 'status_code') and response.status_code == 200:
            ui.notify('Magic link sent! Check your email.', color='positive')
        elif isinstance(response, dict) and response.get('status_code') == 200:
            ui.notify('Magic link sent! Check your email.', color='positive')
        else:
            ui.notify('Failed to send magic link. Please try again.', color='negative')
    except Exception as e:
        print(f"Exception in send_magic_link: {e}")
        import traceback
        traceback.print_exc()
        ui.notify(f'Error sending magic link: {str(e)}', color='negative')