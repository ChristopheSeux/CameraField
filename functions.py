import bpy
import bgl

def remap(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def draw_callback_3d(self,context):
    #bgl.glDisable(bgl.GL_DEPTH_TEST)
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glPointSize(4)
    bgl.glLineWidth(3)


    count =0
    for index, value in self.frames.items() :
        if count != 0 and count != len(self.frames)-1 :
            bgl.glColor4f(1, 1, 0.0, 0.5)
        elif  count != len(self.frames)-1 :
            bgl.glColor4f(1, 1, 1, 0.5)
        else :
            bgl.glColor4f(1, 1, 0.0, 0.5)

        bgl.glBegin(bgl.GL_POINTS)
        for point in value['plain'] :
            bgl.glVertex3f(*point)

        bgl.glEnd()

        count +=1


    # restore opengl defaults
    bgl.glPointSize(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)

    #bgl.glEnable(bgl.GL_DEPTH_TEST)
