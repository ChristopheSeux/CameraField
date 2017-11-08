import bpy


class CameraFrustumPanel(bpy.types.Panel):
    bl_label = "Camera Frustum"
    bl_category = "CAMMAP"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        layout = self.layout

        layout.prop(bpy.context.scene.camera_frustum_settings, "only_active")

        row = layout.row(align=True)
        row.operator("camerafield.view_field", icon='RENDER_ANIMATION')
        row.prop(bpy.context.scene.camera_frustum_settings, "density")



class CameraFrustumCameraPanel(bpy.types.Panel):
    bl_label = "Camera Frustum"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    def draw(self, context):
        layout = self.layout

        ob = context.object
        cam = ob.data

        layout.prop(cam.camera_frustum_settings, "active")
        layout.prop(cam.camera_frustum_settings, "color")
