from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape, Template


if __name__ == '__main__':
    """ Data streams have a lot of common functionality, but it involves
    property and function names that depend upon the name of the data
    stream. e.g. XData *has* to methods on_xdata and
    on_xdata_preprocess. My solution was to do some meta-programming:
    This script generates all of the classes in data_streams.py.

    """
    env = Environment(
        loader=PackageLoader('rvit', 'core/vis/templates'),
        autoescape=select_autoescape(default=False, default_for_string=False)
    )
    class_template = template = env.get_template('data_stream_class.py')

    def generate_data_stream_class(substitutions):
        """ A factory for generating data-view components.

        property_name: what is specified in the rvit.kv file e.g. color_data
        variable_name: how to reference the view from inside the vis e.g. colors
        """

        s = class_template.render(substitutions)
        return(s)

    classes = ''
    classes += generate_data_stream_class({
        'property_name' : 'x_data',
        'variable_name' : 'xs',
        'docstring' : 'vector containing the x-values of data to be plotted.',
        'attribute_defn' : 'attribute float x;',
        'fmt' : (b'x', 1, 'float')
    })
    classes += generate_data_stream_class({
        'property_name' : 'y_data',
        'variable_name' : 'ys',
        'docstring' : 'vector containing the y-values of data to be plotted.',
        'attribute_defn' : 'attribute float y;',
        'fmt' : (b'y', 1, 'float'),
    })

    classes += generate_data_stream_class({
        'property_name' : 'color1d_data',
        'variable_name' : 'colors',
        'docstring' : 'vector containing the colors of each plotted item.',
        'attribute_defn' : 'attribute float color1D;',
        'fmt' : (b'color1D', 1, 'float'),
        'vertex_shader_functions' : '''"""
// testing
"""''',
        'on_set' : 'self.color_dim = np.shape(np.shape((self.colors)[1]))'
    })
    
    classes += generate_data_stream_class({
        'property_name' : 'size_data',
        'variable_name' : 'sizes',
        'docstring' : 'vector containing the sizes of each plotted item.',
        'attribute_defn' : 'attribute float size;',
        'fmt' : (b'size', 1, 'float'),
    })



    s = Template('''
## DO NOT EDIT THIS FILE. It is automatically generated by {{this_file}}
## and any edits will be overwritten the next time that it is run.  

from rvit.core.vis.rvi_element import RVIElement
from kivy.properties import *
from kivy.app import App
import numpy as np

{{classes}}

'''
    )
    filetext = s.render(this_file=__file__,
                        classes=classes)
    #print(filetext)
    with open('data_streams.py', 'tw') as f:
        f.write(filetext)
