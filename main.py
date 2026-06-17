import sys
import tkinter as tk
from pynput import keyboard


popup_open = False
popup = None


def copy(face):
    root.clipboard_clear()
    root.clipboard_append(face)
    root.update()


def popup_manager(action):
    global popup

    if action == 'open':
        popup = tk.Toplevel(root)
        popup.title('Lenny Face Copy + Paste')
        popup.geometry('350x300')

        container = tk.Frame(popup)
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container)
        canvas.pack(side='left', fill='both', expand=True)

        def scroll(event):
            if sys.platform.startswith('linux'):
                if event.num == 4:
                    canvas.yview_scroll(-1, 'units')
                elif event.num == 5:
                    canvas.yview_scroll(1, 'units')
            elif sys.platform == "darwin":  # why is this the mac name
                canvas.yview_scroll(-event.delta, 'units')
            else:
                canvas.yview_scroll(int(-event.delta / 120), 'units')

        canvas.bind_all('<MouseWheel>', scroll)
        canvas.bind_all('<Button-4>', scroll)
        canvas.bind_all('<Button-5>', scroll)

        scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')

        canvas.configure(yscrollcommand=scrollbar.set)

        scroll_frame = tk.Frame(canvas)
        window_id = canvas.create_window((0, 0), window=scroll_frame, anchor='nw')

        def update_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox('all'))
            canvas.itemconfigure(window_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', update_scroll_region)
        scroll_frame.bind('<Configure>', update_scroll_region)

        # WHY WON'T SCROLLING WORK ASD;LKJ

        # im typing on US international keyboard rn whoops

        def copied():
            message = tk.Label(popup, text='copied lenny!', fg='green', font=('Arial', 14))
            message.pack(pady=5)

            popup.after(1200, message.destroy)

        lenny_list = ['( ͡° ͜ʖ ͡°)', 'ʘ‿ʘ', '(◑‿◐)',
                      '( ͡~ ͜ʖ ͡°)', '( ° ͜ʖ °)', '( ͠° ͟ʖ ͡°)',
                      '(͠≖ ͜ʖ͠≖)', 'ʕ ͡° ʖ̯ ͡°ʔ', '(｢•-•)｢ ʷʱʸ?',
                      '( ͡ʘ ͜ʖ ͡ʘ)', '( ͡° ᴥ ͡°)', '( ͡♥ ͜ʖ ͡♥)',
                      '(☭ ͜ʖ ☭)', '(╬ಠ益ಠ)', '(-‿◦☀))',
                      '¯\_(ツ)_/¯', '¯\_( ͡° ͜ʖ ͡°)_/¯', '( ͡° ل͜ ͡°)',
                      '(͡• ͜໒ ͡• )', '(☞ ͡° ͜ʖ ͡°)☞', '( ͝° ͜ʖ͡°)',
                      '┏(-_-)┛', '( ಠ ͜ʖಠ)', '( ͡ಥ ͜ʖ ͡ಥ)',
                      'ᕙ(▀̿ĺ̯▀̿ ̿)ᕗ', '( ͡°👅 ͡°)', '╲⎝⧹ ( ͡° ͜ʖ ͡°) ⎠╱',
                      '[̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅)̲̅$̲̅]', '( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)', '( ཀ ʖ̯ ཀ)']

        for i in range(30):
            lenny_button = tk.Button(scroll_frame, text=lenny_list[i], width=12, command=lambda face=lenny_list[i]: (copy(face), copied()))
            row = i // 2
            col = i % 2
            lenny_button.grid(row=row, column=col, padx=10, pady=5)

        close_button = tk.Button(popup, text='close', command=popup.destroy)
        close_button.pack(pady=10)

    elif action == 'close':
        popup.destroy()


def on_press(key):
    global popup_open

    try:
        if key == keyboard.KeyCode.from_char('l') and ctrl and shift and alt:
            if not popup_open:
                popup_open = True
                popup_manager('open')
            elif popup_open:
                popup_open = False
                popup_manager('close')
    except:
        pass


def on_release(key):
    global ctrl, shift, alt
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl = False
    if key == keyboard.Key.shift:
        shift = False
    if key == keyboard.Key.alt:
        alt = False


def on_press_wrapper(key):
    global ctrl, shift, alt
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl = True
    if key == keyboard.Key.shift:
        shift = True
    if key == keyboard.Key.alt:
        alt = True
    on_press(key)


ctrl = False
shift = False
alt = False


listener = keyboard.Listener(on_press=on_press_wrapper, on_release=on_release)
listener.start()


root = tk.Tk()
root.title('Lenny Face-er Main Window')

title = tk.Label(text='Lenny Face-er', font=('Arial', 30, 'bold'))
title.pack(pady=10)

subtitle = tk.Label(text='created by ImmatureGoat', font=('Arial', 10))
subtitle.pack()

text = tk.Label(text='press ctrl+shift+alt+L for Lenny Faces', font=('Arial', 20))
text.pack(pady=10)

button = tk.Button(text='close', command=root.destroy)
button.pack(pady=(0, 10))

root.mainloop()