#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''Gtk 对话框
@author: U{Jiahua Huang <jhuangjiahua@gmail.com>}
@license: LGPLv3+
'''

import os

import gtk
import gobject

__all__ = ['error', 'info', 'inputbox', 'messagedialog', 'open', 'save', 'warning',
        'yesno']

try: import i18n
except: from gettext import gettext as _

def colorbox(title="Changing color", previous_color='', current_color=''):
    '''
    '''
    dialog = gtk.ColorSelectionDialog("Changing color")
    colorsel = dialog.colorsel

    if current_color:
        colorsel.set_previous_color(previous_color)
    if current_color:
        colorsel.set_current_color(current_color)
    colorsel.set_has_palette(True)

    response = dialog.run()
    htmlcolor = ''
    if response == gtk.RESPONSE_OK:
        color = colorsel.get_current_color()
        rgb = (color.red, color.green, color.blue)
        htmlcolor = '#' + ''.join((str(hex(i/257))[2:].rjust(2, '0') for i in rgb))
    dialog.destroy()
    return htmlcolor

def textbox(title='Text Box', label='Text',
        parent=None, text=''):
    """display a text edit dialog
    
    return the text , or None
    """
    dlg = gtk.Dialog(title, parent, gtk.DIALOG_DESTROY_WITH_PARENT,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_OK, gtk.RESPONSE_OK    ))
    dlg.set_default_size(500,500)
    #lbl = gtk.Label(label)
    #lbl.set_alignment(0, 0.5)
    #lbl.show()
    #dlg.vbox.pack_start(lbl,  False)
    gscw = gtk.ScrolledWindow()
    gscw.set_shadow_type(gtk.SHADOW_IN)    
    #gscw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
    gscw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    textview=gtk.TextView(buffer=None)
    buffer = textview.get_buffer()
    
    if text:buffer.set_text(text)    
    
    #textview.show()
    gscw.add(textview)
    #gscw.show()
    dlg.vbox.pack_start(gscw)
    dlg.show_all()
    resp = dlg.run()
    
    text=buffer.get_text(buffer.get_start_iter(),buffer.get_end_iter())
    dlg.destroy()
    if resp == gtk.RESPONSE_OK:
        return text
    return None

def combobox(title='ComboBox', label='ComboBox', parent=None, texts=['']):
    '''dialog with combobox
    '''
    dlg = gtk.Dialog(title, parent, gtk.DIALOG_DESTROY_WITH_PARENT,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_OK, gtk.RESPONSE_OK    ))

    label1 = gtk.Label(label)
    label1.set_alignment(0, 0.5)
    label1.set_padding(5, 5)
    label1.set_line_wrap(True)
    label1.show()
    dlg.vbox.pack_start(label1, False, False, 0)

    combobox1_List = gtk.ListStore(gobject.TYPE_STRING)
    combobox1 = gtk.ComboBox()
    combobox1.show()
    #combobox1_List.append(["1122"])

    combobox1.set_model(combobox1_List)

    cell = gtk.CellRendererText()
    combobox1.pack_start(cell, True)
    combobox1.add_attribute(cell, 'text', 0)
    dlg.vbox.pack_start(combobox1, True, True, 0)

    for i in texts:
        combobox1.append_text(i)
    combobox1.set_active(0)

    resp = dlg.run()
    t = combobox1.get_active()
    text = texts[t]
    dlg.destroy()
    if resp == gtk.RESPONSE_CANCEL:
        return None        
    return text


def spinbox2(title='2 Spin Box', label1='value1:', label2='value2:',
        parent=None, value1=3, value2=3):
    """dialog with 2 spin buttons
    
    return (value1,value2) , or ()
    """
    dlg = gtk.Dialog(title, parent, gtk.DIALOG_DESTROY_WITH_PARENT,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_OK, gtk.RESPONSE_OK    ))

    lbl = gtk.Label(title)
    lbl.set_alignment(0, 0.5)
    dlg.vbox.pack_start(lbl,  False)
    
    #vbox1 = gtk.VBox(False, 0)
    #vbox1.show()
    #vbox1.set_spacing(0)

    table2 = gtk.Table()
    table2.show()
    table2.set_row_spacings(0)
    table2.set_col_spacings(0)
    
    label1 = gtk.Label(label1)
    label1.set_alignment(0, 0.5)
    label1.set_padding(0, 0)
    label1.set_line_wrap(False)
    label1.show()
    table2.attach(label1, 0, 1, 0, 1, gtk.FILL, 0, 0, 0)
    
    label2 = gtk.Label(label2)
    label2.set_alignment(0, 0.5)
    label2.set_padding(0, 0)
    label2.set_line_wrap(False)
    label2.show()
    table2.attach(label2, 0, 1, 1, 2, gtk.FILL, 0, 0, 0)
            
    adj = gtk.Adjustment(1.0, 1.0, 512.0, 1.0, 5.0, 0.0)
    spin1=gtk.SpinButton(adj,0,0)
    if value1: spin1.set_value(value1)    
    table2.attach(spin1, 1, 2, 0, 1, gtk.EXPAND|gtk.FILL, 0, 0, 0)

    adj2 = gtk.Adjustment(1.0, 1.0, 512.0, 1.0, 5.0, 0.0)
    spin2=gtk.SpinButton(adj2,0,0)
    if value2: spin2.set_value(value2)
    table2.attach(spin2, 1, 2, 1, 2, gtk.EXPAND|gtk.FILL, 0, 0, 0)
    
    #vbox1.pack_start(table2, True, True, 0)
    dlg.vbox.pack_start(table2)
    dlg.show_all()
    
    resp = dlg.run()    
    value1=spin1.get_value()
    value2=spin2.get_value()
    dlg.hide()    
    if resp == gtk.RESPONSE_CANCEL:
        return ()    
    return (value1,value2)
        
def inputbox(title='Input Box', label='Please input the value',
        parent=None, text=''):
    """dialog with a input entry
    
    return text , or None
    """
    #@TODO: 要直接回车确定
    dlg = gtk.Dialog(title, parent, gtk.DIALOG_DESTROY_WITH_PARENT,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_OK, gtk.RESPONSE_OK    ))
    lbl = gtk.Label(label)
    lbl.set_alignment(0, 0.5)
    lbl.show()
    dlg.vbox.pack_start(lbl)
    entry = gtk.Entry()
    if text: entry.set_text(text)
    entry.show()
    dlg.vbox.pack_start(entry, False)
    dlg.set_default_response(gtk.RESPONSE_OK)
    resp = dlg.run()
    text = entry.get_text()
    dlg.hide()
    if resp == gtk.RESPONSE_CANCEL:
        return None
    return text

def inputbox2(title='2 Input Box', label1='value1:', label2='value2:',
        parent=None, text1='', text2=''):
    """dialog with 2 input buttons
    
    return (text1,text2) , or ()
    """
    strlabel2 = label2
    dlg = gtk.Dialog(title, parent, gtk.DIALOG_DESTROY_WITH_PARENT,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_OK, gtk.RESPONSE_OK    ))
    
    lbl = gtk.Label(title)
    lbl.set_alignment(0, 0.5)
    dlg.vbox.pack_start(lbl,  False)
    
    table1 = gtk.Table()
    table1.show()
    table1.set_row_spacings(0)
    table1.set_col_spacings(0)
    
    label2 = gtk.Label(label1)
    label2.set_alignment(0.5, 0.5)
    label2.set_padding(0, 0)
    label2.set_line_wrap(False)
    label2.show()
    table1.attach(label2, 0, 1, 0, 1, gtk.FILL, 0, 0, 0)
    
    entry2 = gtk.Entry()
    entry2.set_text("")
    entry2.set_editable(True)
    entry2.show()
    entry2.set_visibility(True)
    table1.attach(entry2, 1, 2, 0, 1, gtk.EXPAND|gtk.FILL, 0, 0, 0)
    
    label3 = gtk.Label(strlabel2)
    label3.set_alignment(0, 0.5)
    label3.set_padding(0, 0)
    label3.set_line_wrap(False)
    label3.show()
    table1.attach(label3, 0, 1, 1, 2, gtk.FILL, 0, 0, 0)

    entry3 = gtk.Entry()
    entry3.set_text("")
    entry3.set_editable(True)
    entry3.show()
    entry3.set_visibility(True)
    table1.attach(entry3, 1, 2, 1, 2, gtk.EXPAND|gtk.FILL, 0, 0, 0)
    
    if text1: entry2.set_text(text1)
    if text2: entry3.set_text(text2)

    dlg.vbox.pack_start(table1)
    dlg.set_default_response(gtk.RESPONSE_OK)
    dlg.show_all()
    
    resp = dlg.run()
    text1 = entry2.get_text()
    text2 = entry3.get_text()
    dlg.hide()
    if resp == gtk.RESPONSE_CANCEL:
        return ()
    return (text1,text2)    

def savechanges(text=_("Save Changes?"), parent=None):
    '''Save Changes?
    return 1, -1, 0 => yes, no, cancel
    '''
    d = gtk.MessageDialog(parent=parent, flags=gtk.DIALOG_MODAL,
            type=gtk.MESSAGE_INFO,)
    d.add_buttons(gtk.STOCK_YES, 1, gtk.STOCK_NO, -1, gtk.STOCK_CANCEL, 0)
    d.set_markup(text)
    d.show_all()
    response = d.run()
    d.destroy()
    return response

def infotablebox(title=_("Info"), short=_("Info"), info=[[_("Key:"), _("Value")]], parent=None):
    '''show info table box
    '''
    dlg = gtk.Dialog(title, parent, gtk.DIALOG_DESTROY_WITH_PARENT,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_OK, gtk.RESPONSE_OK    ))
    label = gtk.Label()
    label.set_markup(short)
    label.set_padding(20, 10)
    label.set_alignment(0, 0)
    label.show()
    dlg.vbox.pack_start(label, False, False, 0)
    ##
    table = gtk.Table()
    table.show()
    # table
    y = 0
    for line in info:
        x = 0
        left = 0
        for text in line:
            label = gtk.Label()
            #label.set_selectable(1) # 会干扰编辑区选中状态
            label.set_padding(10, 3)
            label.set_alignment(left, 0)
            label.set_markup("%s" % text)
            label.show()
            table.attach(label, x, x+1, y, y+1,)
            x += 1
            left = 1
            pass
        y += 1
        pass
    dlg.vbox.pack_start(table, False, False, 5)
    response = dlg.run()
    dlg.destroy()
    return response


def messagedialog(dialog_type, short, long=None, parent=None,
                buttons=gtk.BUTTONS_OK, additional_buttons=None):
    d = gtk.MessageDialog(parent=parent, flags=gtk.DIALOG_MODAL,
                        type=dialog_type, buttons=buttons)
    
    if additional_buttons:
        d.add_buttons(*additional_buttons)
    
    d.set_markup(short)
    
    if long:
        if isinstance(long, gtk.Widget):
            widget = long
        elif isinstance(long, basestring):
            widget = gtk.Label()
            widget.set_markup(long)
        else:
            raise TypeError("long must be a gtk.Widget or a string")
        
        expander = gtk.Expander(_("Click here for details"))
        expander.set_border_width(6)
        expander.add(widget)
        d.vbox.pack_end(expander)
        
    d.show_all()
    response = d.run()
    d.destroy()
    return response
    
def error(short, long=None, parent=None):
    """Displays an error message."""
    return messagedialog(gtk.MESSAGE_ERROR, short, long, parent)

def info(short, long=None, parent=None):
    """Displays an info message."""
    return messagedialog(gtk.MESSAGE_INFO, short, long, parent)

def warning(short, long=None, parent=None):
    """Displays a warning message."""
    return messagedialog(gtk.MESSAGE_WARNING, short, long, parent)

def yesno(text="OK ?", parent=None):
    """
    
    return 1 or 0 . ( yes/no )
    """
##    return messagedialog(gtk.MESSAGE_WARNING, text, None, parent,
##        buttons=gtk.BUTTONS_YES_NO)
    i = messagedialog(gtk.MESSAGE_INFO, text, None, parent,
        buttons=gtk.BUTTONS_YES_NO)
    if i == -8:
        return 1
    return 0

def open(title='', parent=None, 
        patterns=[], mimes=[], name_mimes=[], name_patterns=[], folder=None):
    """Displays an open dialog.
    
    return the  full path , or None"""
    filechooser = gtk.FileChooserDialog(title or _('Open'),
                    parent,
                    gtk.FILE_CHOOSER_ACTION_OPEN,
                    (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                    gtk.STOCK_OPEN, gtk.RESPONSE_OK))

    if patterns:
        file_filter = gtk.FileFilter()
        for pattern in patterns:
            file_filter.add_pattern(pattern)
        filechooser.set_filter(file_filter)
        pass
    if mimes:
        file_filter = gtk.FileFilter()
        for mime in mimes:
            file_filter.add_mime_type(mime)
        filechooser.add_filter(file_filter)
        pass
    if name_mimes:
        for name, mime in name_mimes:
            file_filter = gtk.FileFilter()
            file_filter.set_name(name)
            file_filter.add_mime_type(mime)
            filechooser.add_filter(file_filter)
    if not "*" in [ i[1] for i in name_patterns]:
        name_patterns += [[_("All Files"), "*"]]
        pass
    for name, pattern in name_patterns:
            file_filter = gtk.FileFilter()
            file_filter.set_name(name)
            file_filter.add_pattern(pattern)
            filechooser.add_filter(file_filter)

    filechooser.set_default_response(gtk.RESPONSE_OK)

    if folder:
        filechooser.set_current_folder(folder)
        
    response = filechooser.run()
    if response != gtk.RESPONSE_OK:
        filechooser.destroy()
        return
    
    path = filechooser.get_filename()
    if path and os.access(path, os.R_OK):
        filechooser.destroy()
        return path
        
    abspath = os.path.abspath(path)

    error(_('Could not open file "%s"') % abspath,
        _('The file "%s" could not be opened. '
        'Permission denied.') %  abspath)

    filechooser.destroy()
    return path

def save(title='', parent=None, current_name='', 
        patterns=[], mimes=[], name_mimes=[], name_patterns=[], folder=None):
    """Displays a save dialog.
    
    return the  full path , or None
    """
    filechooser = gtk.FileChooserDialog(title or _('Save'),
                parent,
                gtk.FILE_CHOOSER_ACTION_SAVE,
                (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                gtk.STOCK_SAVE, gtk.RESPONSE_OK))

    if patterns:
        file_filter = gtk.FileFilter()
        for pattern in patterns:
            file_filter.add_pattern(pattern)
        filechooser.set_filter(file_filter)
        pass
    if mimes:
        file_filter = gtk.FileFilter()
        for mime in mimes:
            file_filter.add_mime_type(mime)
        filechooser.add_filter(file_filter)
        pass
    if name_mimes:
        for name, mime in name_mimes:
            file_filter = gtk.FileFilter()
            file_filter.set_name(name)
            file_filter.add_mime_type(mime)
            filechooser.add_filter(file_filter)
    if not "*" in [ i[1] for i in name_patterns]:
        name_patterns += [[_("All Files"), "*"]]
        pass
    for name, pattern in name_patterns:
            file_filter = gtk.FileFilter()
            file_filter.set_name(name)
            file_filter.add_pattern(pattern)
            filechooser.add_filter(file_filter)
                
    if current_name:
        filechooser.set_current_name(current_name)       
    filechooser.set_default_response(gtk.RESPONSE_OK)
    
    if folder:
        filechooser.set_current_folder(folder)
        
    path = None
    while True:
        response = filechooser.run()
        if response != gtk.RESPONSE_OK:
            path = None
            break
        
        path = filechooser.get_filename()
        if not os.path.exists(path):
            break

        submsg1 = _('A file named "%s" already exists') % os.path.abspath(path)
        submsg2 = _('Do you which to replace it with the current project?')
        text = '<span weight="bold" size="larger">%s</span>\n\n%s\n' % \
            (submsg1, submsg2)
        result = messagedialog(gtk.MESSAGE_ERROR,
                    text,
                    parent=parent,
                    buttons=gtk.BUTTONS_NONE,
                    additional_buttons=(gtk.STOCK_CANCEL,
                            gtk.RESPONSE_CANCEL,
                            _("Replace"),
                            gtk.RESPONSE_YES))
        # the user want to overwrite the file
        if result == gtk.RESPONSE_YES:
            break

    filechooser.destroy()
    return path
    
def test():
    #globals()['_'] = lambda s: s
    #-print combobox(title='ComboBox', label='Combo', texts=['11','22','33'])
    #-print spinbox2(title='Select the values',label1='cows:',value1=4, label2='rows:',value2=4)
    #-print textbox(title='Edit The Text',label='Text',text='test text in textbox')
    #-print inputbox(title='Input a Value',label='Input a value')
    #-print inputbox2(title='Name and Host',label1='name:',text1='vgh', label2='host:',text2='/')
    #print open(title='Open a file', patterns=['*.py'])
    #-print open(title='Open a file', name_mimes={"Python Script":"text/x-python"})
    #print save(title='Save a file', current_name='foobar.py')
    #-print save(title='Save a file', current_name='foobar.py', name_mimes={"Python Script":"text/x-python"})
    #-print info(short='This is a InfoBox', long='the long message')
    #-print yesno(text='Are you OK?')
    #-print savechanges()
    error('An error occurred', gtk.Button('Woho'))
    error('An error occurred',
        'Long description bla bla bla bla bla bla bla bla bla\n'
        'bla bla bla bla bla lblabl lablab bla bla bla bla bla\n'
        'lbalbalbl alabl l blablalb lalba bla bla bla bla lbal\n')
    
if __name__ == '__main__':
    test()
