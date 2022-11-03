import pyglet
from pyglet.gl import glBlendFunc, glDisable, glEnable, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA

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
        return pyglet.gl.current_context.frost_default_shader
    except AttributeError:
        _default_vert_shader = pyglet.graphics.shader.Shader(vertex_source, 'vertex')
        _default_frag_shader = pyglet.graphics.shader.Shader(fragment_source, 'fragment')
        default_shader_program = pyglet.graphics.shader.ShaderProgram(_default_vert_shader, _default_frag_shader)
        pyglet.gl.current_context.frost_default_shader = default_shader_program
        return default_shader_program


class FrostGroup(pyglet.graphics.Group):
    """Shared Widget rendering Group.

    The group is automatically coalesced with other widget groups
    sharing the same parent group and blend parameters.
    """

    def __init__(self, program, order=0, parent=None):
        """Create a Shape group.

        The group is created internally. Usually you do not
        need to explicitly create it.

        :Parameters:
            `program` : `~pyglet.graphics.shader.ShaderProgram`
                The ShaderProgram to use.
            `parent` : `~pyglet.graphics.Group`
                Optional parent group.
        """
        super().__init__(order=order, parent=parent)
        self.program = program
        self.blend_src = GL_SRC_ALPHA
        self.blend_dest = GL_ONE_MINUS_SRC_ALPHA

    def set_state(self):
        self.program.bind()
        glEnable(GL_BLEND)
        glBlendFunc(self.blend_src, self.blend_dest)

    def unset_state(self):
        glDisable(GL_BLEND)
        self.program.unbind()

    def __eq__(self, other):
        return (other.__class__ is self.__class__ and
                self.parent == other.parent and
                self.order == other.order and
                self.blend_src == other.blend_src and
                self.blend_dest == other.blend_dest and
                self.program == other.program)

    def __hash__(self):
        return hash((id(self.parent), self.blend_src, self.blend_dest, self.order, self.program))

