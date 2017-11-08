import bpy
import bgl


# def remap(value, leftMin, leftMax, rightMin, rightMax):
#     # Figure out how 'wide' each range is
#     leftSpan = leftMax - leftMin
#     rightSpan = rightMax - rightMin
#
#     # Convert the left range into a 0-1 range (float)
#     valueScaled = (value - leftMin) / leftSpan
#
#     # Convert the 0-1 range into a value in the right range.
#     return rightMin + valueScaled * rightSpan


def draw_callback_3d(self, context):
    # bgl.glDisable(bgl.GL_DEPTH_TEST)
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glPointSize(4)
    bgl.glLineWidth(3)

    # for f_i, frame in enumerate(self.frames.values()):
    for co, color in zip(self.points['co'], self.points['colors']):
        bgl.glColor4f(*color, 0.5)
        # if f_i == 0:  # and f_i != len(self.frames)-1:
        #     bgl.glColor4f(1, 1, 1, 0.5)
        # elif f_i != len(self.frames) - 1:
        #     bgl.glColor4f(1, 1, 0.0, 0.5)

        bgl.glBegin(bgl.GL_POINTS)
        # for point in frame:
        bgl.glVertex3f(*co)

        bgl.glEnd()

    # Restore opengl defaults
    bgl.glPointSize(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)

    # bgl.glEnable(bgl.GL_DEPTH_TEST)
