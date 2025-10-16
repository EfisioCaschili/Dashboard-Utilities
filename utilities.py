
import os


scripts = {'Create_PDF_Report':'main.py','Overview SlotMeeting':'app.py','WEEKLY REPORT':'gui.py'}

def get_script(script_name):
    return scripts.get(script_name, "Script not found")