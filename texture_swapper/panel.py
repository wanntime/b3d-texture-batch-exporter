import bpy
from .operator import MESH_OT_texture_swapper

class VIEW3D_PT_texture_swapper(bpy.types.Panel):
    """テクスチャスワッパーのUIパネル"""
    
    bl_label = "Texture Swapper"
    bl_idname = "VIEW3D_PT_texture_swapper"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Texture Swapper'

    def draw(self, context):
        """パネルの描画
        
        Args:
            context: Blenderのコンテキスト
        """
        layout = self.layout
        props = context.scene.my_tool

        # マテリアル選択セクション
        box = layout.box()
        box.label(text="マテリアル設定", icon='MATERIAL')
        box.prop(props, "target_material")
        
        if props.target_material:
            box.prop(props, "target_node_index")
        
        # フォルダ設定セクション
        box = layout.box()
        box.label(text="フォルダ設定", icon='FILE_FOLDER')
        box.prop(props, "textures_folder")
        box.prop(props, "export_path")
        
        # ファイル名設定セクション
        box = layout.box()
        box.label(text="ファイル名設定", icon='FILE')
        box.prop(props, "export_file_name_base")
        
        # 実行ボタン
        layout.separator()
        layout.operator(
            MESH_OT_texture_swapper.bl_idname,
            text="実行",
            icon='PLAY'
        )
