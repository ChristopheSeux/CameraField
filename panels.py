import bpy

class cameraFrustumPanel(bpy.types.Panel):
    bl_label = "Camera Frustum"
    bl_category = "CAMMAP"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'


    def draw(self,context):
        layout = self.layout
        row = layout.row(align= True)

        row.operator("camerafield.view_field",icon = 'RENDER_ANIMATION')
        row.prop(bpy.context.scene.CameraFrustumSettings,"density")
        #row = layout.row(align= True)
        #row.label('Look throw cam Proj and select render Cam')
