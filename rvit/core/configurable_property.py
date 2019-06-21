from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.graphics import Color
from kivy.uix.colorpicker import ColorPicker,ColorWheel
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, OptionProperty, BooleanProperty
from rvit.core.properties import ColorProperty
from functools import partial
from rvit.core import *
import rvit.core

class ConfigurableProperty(object):
    def __init__(self, prop, owner):
        self.prop = prop
        self.owner = owner
        self.key = self.owner.unique_name + '.' + self.prop.name

        # load values from the previous run
        if self.key in rvit.core.pars.keys():
            # print('configurableProperty %s being '+
            #       'loaded from a previous run to be %s' % (self.key,
            #                                                rvit.core.pars[self.key]))
            self.prop.set(self.owner, rvit.core.pars[self.key])
            self.prop.dispatch(self.owner)

    def getConfigurationSubpanel(self):
        subpanel = BoxLayout(size_hint=(1.0, None), height=(40))
        subpanel.add_widget(Label(text=self.prop.name, size_hint=(1.0, 1.0)))
        if isinstance(self.prop, ColorProperty):
            clr_picker = ColorPicker()
            if(self.key in rvit.core.pars.keys()) :
                current_color = rvit.core.pars[self.key]
                clr_picker.color = current_color
            def on_color(instance, value):
                # print("RGBA = ", instance.color)
                # print(type(instance.color))
                # print("HSV = ", str(instance.hsv))
                # print("HEX = ", str(instance.hex_color))
                self.prop.set(self.owner, list(instance.color))
                rvit.core.pars[self.key] = list(instance.color)
            subpanel.add_widget(clr_picker)
            clr_picker.bind(color=on_color)
            subpanel.height = 300
            subpanel.background = [0,0,0,1]
        elif isinstance(self.prop, OptionProperty):
            if len(self.prop.options) < 5:
                for opt in self.prop.options:

                    def setNewValue(_, new_value=''):
                        self.prop.set(self.owner, new_value)
                        rvit.core.pars[self.key] = new_value

                    set_fn = partial(setNewValue, new_value=opt)
                    btn = ToggleButton(text=opt, group=self.prop.name,
                                       on_press=set_fn)
                    if self.prop.get(self.owner) == opt:
                        btn.state = 'down'
                    subpanel.add_widget(btn)
        elif isinstance(self.prop, StringProperty):
            def on_text(instance, value):
                self.prop.set(self.owner, value)
                rvit.core.pars[self.key] = value

            ti = TextInput(text=str(self.prop.get(self.owner)),
                           multiline=False, size_hint=(1.0, 1.0))
            subpanel.add_widget(ti)
            ti.bind(text=on_text)
        elif isinstance(self.prop, NumericProperty):
            def is_number(s):
                try:
                    float(s)
                    return True
                except ValueError:
                    return False

            def on_text(instance, value):
                if(is_number(value)):
                    value = float(value)
                    self.prop.set(self.owner, value)
                    rvit.core.pars[self.key] = value

            ti = TextInput(text=str(self.prop.get(self.owner)),
                           multiline=False, size_hint=(1.0, 1.0))
            subpanel.add_widget(ti)
            ti.bind(text=on_text)        
        else:
            subpanel.add_widget(Label(text=str(self.prop.get(self.owner)),
                                      size_hint=(1.0, 1.0)))
        return subpanel
