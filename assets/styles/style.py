# import helperFuns.helperFuns

from nicegui import ui

def Wave_AnimationCSS():
    return ui.add_head_html('''
        <style type="text/css">
            .waves-block {
            position: absolute;
            width: 720px;
            height: 720px;
            top: 50%;
            -webkit-transform: translateY(-50%);
            transform: translateY(-50%);
            }
            .waves-block .waves {
            position: absolute;
            width: 100%;
            height: 100%;
            background: rgba(54, 39, 133, 0.2);
            opacity: 0;
            -ms-filter: 'alpha(opacity=0)';
            border-radius: 50%;
            background-clip: padding-box;
            -webkit-animation: waves 6s ease-in-out infinite;
            animation: waves 6s ease-in-out infinite;
            }
            .waves-block .wave-1 {
            -webkit-animation-delay: 0s;
            animation-delay: 2s;
            }
            .waves-block .wave-2 {
            -webkit-animation-delay: 1s;
            animation-delay: 3s;
            }
            .waves-block .wave-3 {
            -webkit-animation-delay: 2s;
            animation-delay: 4s;
            }
            .waves-block .wave-4 {
            -webkit-animation-delay: 2s;
            animation-delay: 5ms;
            }
            @keyframes waves {
            0% {
                -webkit-transform: scale(0.5, 0.5);
                transform: scale(0.5, 0.5);
                opacity: 0;
                -ms-filter: 'alpha(opacity=0)';
            }
            50% {
                opacity: 0.7;
                -ms-filter: 'alpha(opacity=90)';
            }
            100% {
                -webkit-transform: scale(0.9, 0.9);
                transform: scale(0.9, 0.9);
                opacity: 0;
                -ms-filter: 'alpha(opacity=0)';
            }
            }
        </style>
''')
def RemoveOverPadding():
    return ui.query('.nicegui-content').classes('bg-red-800; p-0')

def ZoomIn():
    return ui.add_css('''
    @keyframes zoomIn {
    0% {
        transform: scale(0.5); /* Start smaller */
        opacity: 0; /* Optional: fade in */
    }
    100% {
        transform: scale(1); /* End at normal size */
        opacity: 1; /* Fully visible */
    }
    }

    .zoom-in {
    display: inline-block; /* Ensure the element respects its size */
    animation: zoomIn 2s ease-in-out; /* Duration and easing */
    transform-origin: center; /* Zoom from the center */
''')

def SildeFromTop():
    return ui.add_css('''
    @keyframes fade-in-up {0% { transform: translateY(-50px); opacity: 0; } 100% { transform: translateY(0); opacity: 1;} }
    .fadeIn-top { 
        animation: fade-in-up 3s ease 0.2s normal none; 
    }
''')

def SlideFromBottom():
    ui.add_css('''
        @keyframes fade-in-bottom {0% { transform: translateY(50px); opacity: 0; } 100% { transform: translateY(0); opacity: 1;} }

        .fadeIn-bottom { 
            animation: fade-in-bottom 3s ease-in 0.4s 1 normal none; 
        }
''')

def FlipCards():
    ui.add_css('''
            h2{font-size:2rem}
            .card { perspective: 800px;}
            .card__content {transform-style: preserve-3d;}
            .flib_card {transform: rotateY(.5turn);} #transition style

            .card__front,
            .card__back { backface-visibility: hidden;}
            .card__back{ transform: rotateY(.5turn);}
     ''')
    
def SearchBox():
    ui.add_css('''
        .btn.disabled .btn:disabled {
        opacity: 0.65;
        }
        .btn:not(:disabled):not(.disabled) {
        cursor: pointer;
        }
        a.btn.disabled fieldset:disabled a.btn {
        pointer-events: none;
        }
        .close {
        float: right;
        font-size: 1.5rem;
        font-weight: 700;
        line-height: 1;
        color: #f6f2f2;
        text-shadow: 0 1px 0 #fff;
        opacity: 0.75;
        }
        .close:hover {
        color: #fff;
        text-decoration: none;
        }
        .close:not(:disabled):not(.disabled) {
        cursor: pointer;
        }
        .close:not(:disabled):not(.disabled):hover,
        .close:not(:disabled):not(.disabled):focus {
        opacity: 1;
        }

        button.close {
        padding: 0;
        background-color: transparent;
        border: 0;
        appearance: none;
        }

        a.close.disabled {
        pointer-events: none;
        }
        .searchWrapper {
        position: relative;
        margin-right: 0.6666666667rem;
        }
        .searchWrapper .inputHolder {
        height: 42px;
        width: 42px;
        overflow: hidden;
        position: relative;
        transition: all 0.3s ease-in-out;
        }
        .searchWrapper .inputHolder .searchInput {
        width: 100%;
        padding: 0 70px 0 20px;
        opacity: 0;
        position: absolute;
        top: 0;
        left: 0;
        background: transparent;
        box-sizing: border-box;
        border: none;
        outline: none;
        transform: translate(0, 60px);
        transition: all 0.3s cubic-bezier(0, 0.105, 0.035, 1.57);
        transition-delay: 0.3s;
        color: #fff;
        font-size: 1rem;
        }
        .searchWrapper .inputHolder .searchIcon {
        width: 42px;
        height: 42px;
        border: none;
        padding: 0;
        outline: none;
        position: relative;
        z-index: 2;
        float: right;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 30px;
        }
        .searchWrapper .inputHolder .searchIcon span {
        width: 24px;
        height: 24px;
        display: inline-block;
        vertical-align: middle;
        position: relative;
        transform: rotate(45deg);
        transition: all 0.4s cubic-bezier(0.65, -0.6, 0.24, 1.65);
        }
        .searchWrapper .inputHolder .searchIcon span::before,
        .searchWrapper .inputHolder .searchIcon span::after {
        position: absolute;
        content: '';
        }
        .searchWrapper .inputHolder .searchIcon span::before {
        width: 4px;
        height: 11px;
        left: 9px;
        top: 13px;
        border-radius: 2px;
        background: rgba(255, 255, 255, 0.8);
        }
        .searchWrapper .inputHolder .searchIcon span::after {
        width: 14px;
        height: 14px;
        left: 4px;
        top: 0;
        border-radius: 16px;
        border: 2px solid rgba(255, 255, 255, 0.9);
        }
        .searchWrapper .close {
        position: absolute;
        z-index: 1;
        top: 50%;
        left: 0;
        width: 20px;
        height: 20px;
        margin-top: -10px;
        cursor: pointer;
        opacity: 0 !important;
        transform: rotate(-180deg);
        transition: all 0.2s cubic-bezier(0.285, -0.45, 0.935, 0.11);
        transition-delay: 0.1s;
        }
        .searchWrapper .close::before,
        .searchWrapper .close::after {
        position: absolute;
        content: '';
        background: rgba(255, 255, 255, 0.9);
        border-radius: 2px;
        }
        .searchWrapper .close::before {
        width: 2px;
        height: 20px;
        left: 9px;
        top: 0;
        }
        .searchWrapper .close::after {
        width: 20px;
        height: 2px;
        left: 0;
        top: 9px;
        }
        .searchWrapper.active {
        width: 330px;
        }
        .activeIcon {
        background-color: transparent !important;
        }
        .searchWrapper.active .inputHolder {
        width: 290px;
        border-radius: 50px;
        background: rgba(255, 255, 255, 0.1);
        transition: all 0.5s cubic-bezier(0, 0.105, 0.035, 1.57);
        }
        .searchWrapper.active .inputHolder .searchInput {
        opacity: 1;
        transform: translate(0, 11px);
        }
        .searchWrapper.active .inputHolder .searchIcon {
        width: 42px;
        height: 42px;
        margin: 0;
        border-radius: 30px;
        }
        .searchWrapper.active .inputHolder .searchIcon span {
        transform: rotate(-45deg);
        }
        .searchWrapper.active .close {
        left: 300px;
        opacity: 0.6 !important;
        transform: rotate(45deg);
        transition: all 0.6s cubic-bezier(0, 0.105, 0.035, 1.57);
        transition-delay: 0.5s;
        }
        .searchWrapper.active .close:hover {
        opacity: 1 !important;
        }
        .searchWrapper.active + .headerMegamenu {
        opacity: 0;
        }
        .searchPlaceholder::placeholder {
        color: #fff !important;
        }
        @media screen and (max-width: 768px) {
        .searchWrapper {
            display: none;
            }
    }
    ''')
    
# <div class="card w-40">
#   <div class="card__content text-center relative p-20 transition-transform duration-1000 text-white font-bold">
    
#     <div class="card__front absolute top-0 bottom-0 right-0 left-0 p-8 bg-pink-600 flex items-center justify-center">
#       <h2>Front</h2>
#     </div>
#     <div class="card__back absolute top-0 bottom-0 right-0 left-0 p-8 bg-teal-500 flex items-center justify-center">
#       <h2>Back</h2>
#     </div>
    
#   </div>
# </div>