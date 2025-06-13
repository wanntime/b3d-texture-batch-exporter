# アドオンのメタ情報
bl_info = {
    "name": "Texture Swapper",
    "author": "wanntime",
    "version": (0, 0, 1),
    "blender": (4, 3, 2),
    "location": "View3D > Sidebar > Texture Swapper",
    "description": "Swaps texture of the active material and exports the model.",
    "warning": "This is a beta version.",
    "doc_url": "",
    "category": "Material",
}

# Pythonの再読み込みに対応するための処理
if "bpy" in locals():
    import importlib
    importlib.reload(properties)
    importlib.reload(operator)
    importlib.reload(panel)

import bpy

# 他のファイルからクラスをインポート
from .properties import TextureSwapperProperties
from .operator import MESH_OT_texture_swapper
from .panel import VIEW3D_PT_texture_swapper

# アドオンに含めるクラスのリスト
classes = (
    TextureSwapperProperties,
    MESH_OT_texture_swapper,
    VIEW3D_PT_texture_swapper,
)

# アドオンの登録処理
def register():
    bpy.utils.register_class(TextureSwapperProperties)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=TextureSwapperProperties)
    bpy.utils.register_class(MESH_OT_texture_swapper)
    bpy.utils.register_class(VIEW3D_PT_texture_swapper)

# アドオンの登録解除処理
def unregister():
    del bpy.types.Scene.my_tool
    bpy.utils.unregister_class(VIEW3D_PT_texture_swapper)
    bpy.utils.unregister_class(MESH_OT_texture_swapper)
    bpy.utils.unregister_class(TextureSwapperProperties)
