import pyglet
from pyglet.graphics.api.gl import glBlendFunc, glDisable, glEnable, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA

from pyglet.graphics import shader


vertex_source = """#version 150 core
    in vec2 vertices;
    in vec2 translation;
    in vec3 colors;

    out vec4 vertex_colors;

    uniform WindowBlock
    {
        mat4 projection;
        mat4 view;
    } window;

    mat4 m_translate = mat4(1.0);

    void main()
    {
        m_translate[3][0] = translation.x;
        m_translate[3][1] = translation.y;

        gl_Position = window.projection * window.view * m_translate * vec4(vertices, 0.0, 1.0);
        vertex_colors = vec4(colors, 1);
    }
"""

fragment_source = """#version 150 core
    in vec4 vertex_colors;
    out vec4 final_color;

    void main()
    {
        final_color = vertex_colors;
    }
"""


def get_default_shader():
    try:
        return pyglet.graphics.frost_default_shader
    except AttributeError:
        _default_vert_shader = pyglet.graphics.Shader(vertex_source, 'vertex')
        _default_frag_shader = pyglet.graphics.Shader(fragment_source, 'fragment')
        default_shader_program = pyglet.graphics.ShaderProgram(_default_vert_shader, _default_frag_shader)
        pyglet.graphics.frost_default_shader = default_shader_program
        return default_shader_program
