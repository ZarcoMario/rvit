import numpy as np
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, OptionProperty, BooleanProperty
from kivy.core.window import Window
from kivy.graphics.transformation import Matrix
from functools import partial
import os
from kivy.graphics.context_instructions import *
from kivy.graphics import RenderContext
from kivy.clock import Clock

import rvit.core
from ..configurable_property import ConfigurableProperty

class RvitWidget(FloatLayout):
    unique_name = StringProperty('')
    target_object = ObjectProperty(None)
    target_varname = StringProperty('')
    show_controls = BooleanProperty(True)
    auto_update = BooleanProperty(True)
    update_interval = NumericProperty(1.0 / 60.0)
    preprocess = StringProperty('')
    secondary_preprocess = StringProperty('')

    def __init__(self, *args, **kwargs):
        self.render_context = RenderContext()
        super(RvitWidget, self).__init__(**kwargs)
        self.configurable_properties = {}
        self.addControlBar()

        self.render_context['modelview_mat'] = Matrix().identity()
        self.render_context['projection_mat'] = Matrix().identity()
        self.render_context['window_size'] = [float(Window.width), float(Window.height)]
        self.canvas.before.add(self.render_context)

        self.update_event = None

        prop = self.property('update_interval')
        # dispatch this property on the button instance
        prop.dispatch(self)

    def addControlBar(self):
        """ Adds bar to top of widget with various controls for that widget. """
        self.top_buttons = BoxLayout(orientation='horizontal',
                                     size_hint=(1.0, None),
                                     size=(0, 20),
                                     pos_hint={'right': 1.0,
                                               'top': 1.0},)

        ## create title label
        self.title_label = Label()
        self.top_buttons.add_widget(self.title_label)


        ## create inspection button
        if 'inspect' in dir(self):
            self.inspect_button = Button(text='inspect',
                                         on_press=lambda x: self.inspect(),
                                         background_color=rvit.core.WHITE,
                                         pos_hint={'x': 0.0, 'top': 1.0})

            self.top_buttons.add_widget(self.inspect_button)

        ## create disable button 
        self.disable_button = ToggleButton(size_hint=(None, None),
                                           background_color=rvit.core.RED,
                                           size=(20, 20),
                                           state='down',
                                           )

        def enabled_state_changed(inst, value):
            self.enabled = value == 'down'
        self.enabled = True
        self.disable_button.bind(state=enabled_state_changed)
        self.top_buttons.add_widget(self.disable_button)

        ## add all created buttons to layout (i.e. display them all)
        self.add_widget(self.top_buttons)
        
    def addConfigurableProperty(self, prop):
        self.configurable_properties[prop.name] = ConfigurableProperty(prop, self)

    def removeConfigurableProperty(self, prop):
        self.configurable_properties.pop(prop.name)

    def registerConfigurableProperties(self):
        pass

    def on_unique_name(self, obj, unique_name):
        """Once the widget is given a non-empty unique name, set up its
        configuration panel UI (i.e the panel that comes up when you hit
        the 'configure' button.

        """

        if unique_name != '':
            self.title_label.text = unique_name
            self.registerConfigurableProperties()
            if len(self.configurable_properties) > 0:
                def test(value):
                    content = StackLayout()
                    for k in self.configurable_properties.keys():
                        content.add_widget(
                            self.configurable_properties[k].getConfigurationSubpanel())
                    popup = Popup(title='Configure', content=content)
                    popup.open()

                self.configure_button = Button(text='configure',
                                               on_press=test,
                                               background_color=rvit.core.BLUE,
                                               pos_hint={'x': 0.0, 'top': 1.0})

                self.top_buttons.add_widget(self.configure_button, index=2)

                
    def on_show_controls(self, inst, value):
        if value == True:
            self.add_widget(self.top_buttons)
        else:
            if self.top_buttons in self.children:
                self.remove_widget(self.top_buttons)

    def createInspectionDumpFile(self):
        try:
            os.makedirs(skivy.inspection_path)
        except os.error:
            pass

        datafile_name = filter(str.isalnum, self.unique_name)
        return os.path.join(skivy.inspection_path, datafile_name)

    def launchInspector(self, datafile_name):
        from subprocess import call

        inspection_script_name = 'inspect_%s.py' % (filter(str.isalnum, self.unique_name))
        inspection_script_path = os.path.join(skivy.inspection_path, inspection_script_name)
        with open(inspection_script_path, "w") as text_file:
            text_file.write('from pylab import *\n')
            text_file.write('a = np.load("%s")\n' % (datafile_name))
            text_file.write("print('%s is loaded in the variable called `a`')\n" % (datafile_name))

        instructions = ['gnome-terminal', '-e',
                        """ bash -c "cd """ + skivy.inspection_path +
                        """ ; ipython -i """ + inspection_script_name + """ " """]
        call(instructions)

    def on_target_object(self, inst, value):
        self.target_object = value
        # self.setTarget()

    # def on_target_varname(self, inst, value):
    #     self.target_varname = value
    #     self.setTarget()

    def on_preprocess(self, obj, value):
        self.preprocess = value
        s = 'self.preprocess_fn = %s' % (self.preprocess)
        exec(s)

    def on_secondary_preprocess(self, obj, value):
        self.secondary_preprocess = value
        s = 'self.secondary_preprocess_fn = %s' % (self.secondary_preprocess)
        exec(s)

    def apply_preprocessing(self, data):
        if self.preprocess != '':
            return self.preprocess_fn(data)
        else:
            return data

    def apply_secondary_preprocessing(self, data):
        if self.secondary_preprocess != '':
            return self.secondary_preprocess_fn(data)
        else:
            return data

    def on_update_interval(self, obj, value):
        if self.update_event is not None:
            self.update_event.cancel()

        if self.auto_update:
            def iterate(a):
                self.update()
            self.update_event = Clock.schedule_interval(iterate, self.update_interval)




# ### Local Variables: ###
# ### mode: python ###
# ### python-main-file: "main.py" ###
# ### python-working-dir: "../minimal_project/" ###
# ### End: ###