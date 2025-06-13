import bpy
import os
from typing import Optional, List, Tuple
from pathlib import Path


def export_glb(file_path):
    bpy.ops.export_scene.gltf(
        filepath=file_path,
        export_format='GLB',
        use_selection=True,
        export_yup=True,
        export_texcoords=True,
        export_normals=True,
        export_vertex_color='MATERIAL',
        export_all_vertex_colors=True,
        export_materials='EXPORT',
        export_image_format='AUTO',
        export_rest_position_armature=True,
        export_animations=False,
    )

class MESH_OT_texture_swapper(bpy.types.Operator):
    """テクスチャを差し替えてエクスポートするオペレーター"""
    
    bl_idname = "mesh.texture_swapper"
    bl_label = "Batch Swap and Export"
    bl_options = {'REGISTER', 'UNDO'}

    def validate_inputs(self, context) -> Tuple[bool, Optional[str]]:
        """入力値の検証を行う
        
        Args:
            context: Blenderのコンテキスト
            
        Returns:
            Tuple[bool, Optional[str]]: (検証結果, エラーメッセージ)
        """
        props = context.scene.my_tool
        
        if not props.target_material:
            return False, "マテリアルを選択してください"
            
        if not props.target_node_index or props.target_node_index == "NONE":
            return False, "テクスチャノードを選択してください"
            
        if not props.textures_folder:
            return False, "テクスチャフォルダを指定してください"
            
        if not props.export_path:
            return False, "エクスポート先フォルダを指定してください"
            
        # 選択されたオブジェクトのチェック
        selected_objects = context.selected_objects
        if not selected_objects:
            return False, "エクスポートするオブジェクトを選択してください"
            
        self.report({'INFO'}, f"選択されたオブジェクト: {', '.join(obj.name for obj in selected_objects)}")
            
        return True, None

    def get_image_files(self, folder_path: str) -> List[str]:
        """指定フォルダ内の画像ファイルを取得する
        
        Args:
            folder_path: フォルダのパス
            
        Returns:
            List[str]: 画像ファイル名のリスト
        """
        return [f for f in os.listdir(folder_path) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    def execute(self, context):
        """オペレーターの実行
        
        Args:
            context: Blenderのコンテキスト
            
        Returns:
            set: 実行結果
        """
        # 入力値の検証
        is_valid, error_message = self.validate_inputs(context)
        if not is_valid:
            self.report({'WARNING'}, error_message)
            return {'CANCELLED'}
            
        props = context.scene.my_tool
        
        # マテリアルとノードの取得
        mat = props.target_material
        node_index = int(props.target_node_index)
        tex_nodes = [node for node in mat.node_tree.nodes if node.type == 'TEX_IMAGE']
        
        if node_index >= len(tex_nodes):
            self.report({'ERROR'}, "ノードインデックスが範囲外です")
            return {'CANCELLED'}
            
        image_node = tex_nodes[node_index]
        
        # パスの設定
        export_folder = Path(bpy.path.abspath(props.export_path))
        textures_folder = Path(bpy.path.abspath(props.textures_folder))
        base_name = props.export_file_name_base or "model"
        
        # 元の状態のエクスポート
        if not export_folder.exists():
            self.report({'ERROR'}, f"エクスポート先フォルダが存在しません: {export_folder}")
            return {'CANCELLED'}

        if not textures_folder.exists():
            self.report({'ERROR'}, f"テクスチャフォルダが存在しません: {textures_folder}")
            return {'CANCELLED'}
            
        original_path = export_folder / f"{base_name}.glb"
        self.report({'INFO'}, f"元の状態をエクスポート: {original_path.name}")
        export_glb(str(original_path))
        
        # 画像ファイルの取得
        image_files = self.get_image_files(str(textures_folder))
        if not image_files:
            self.report({'WARNING'}, "指定フォルダに画像ファイルが見つかりません")
            return {'CANCELLED'}
            
        # テクスチャの差し替えとエクスポート
        total_files = len(image_files)
        self.report({'INFO'}, f"{total_files}個の画像を処理します...")
        
        for i, texture_file in enumerate(image_files, 1):
            # テクスチャの差し替え
            new_image_path = textures_folder / texture_file
            new_image = bpy.data.images.load(str(new_image_path), check_existing=True)
            image_node.image = new_image
            
            # エクスポート
            texture_name = Path(texture_file).stem
            export_path = export_folder / f"{base_name}_{texture_name}.glb"
            self.report({'INFO'}, f"処理中 ({i}/{total_files}): {texture_file}")
            export_glb(str(export_path))
            
        return {'FINISHED'}
