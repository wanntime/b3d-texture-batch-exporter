import bpy
from typing import List, Tuple, Optional

# ドロップダウンメニューの項目を動的に生成する関数
def get_image_nodes(self, context) -> List[Tuple[str, str, str]]:
    """選択されたマテリアル内の画像テクスチャノードをリストアップする
    
    Args:
        context: Blenderのコンテキスト
        
    Returns:
        List[Tuple[str, str, str]]: (識別子, 表示名, 説明)のリスト
    """
    items: List[Tuple[str, str, str]] = []
    # プロパティが所属するシーンからmy_toolプロパティグループを取得
    props = context.scene.my_tool
    
    if props.target_material:
        mat = props.target_material
        if mat.use_nodes and mat.node_tree:
            # ノード名とノードのラベルをリストに追加
            tex_nodes = [node for node in mat.node_tree.nodes if node.type == 'TEX_IMAGE']
            for i, node in enumerate(tex_nodes):
                # 識別子として、ノード名ではなくインデックス番号の文字列を格納する
                item = (str(i), node.label or node.name, f"Image: {node.image.name if node.image else 'None'}")
                items.append(item)
    
    if not items:
        items.append(("NONE", "No Image Texture Node Found", "Select a material with image textures"))
        
    return items

class TextureSwapperProperties(bpy.types.PropertyGroup):
    target_material: bpy.props.PointerProperty(  # type: ignore
        name="マテリアル選択", 
        type=bpy.types.Material,
        description="テクスチャを差し替えたいマテリアルを選択してください"
    )
    
    target_node_index: bpy.props.EnumProperty(  # type: ignore
        name="ターゲット画像ノード",
        description="差し替えたいテクスチャノードを選択してください",
        items=get_image_nodes
    )
    
    textures_folder: bpy.props.StringProperty(  # type: ignore
        name="テクスチャフォルダ選択",
        description="入れ替えたいテクスチャ群が格納されたフォルダを指定してください", 
        subtype='DIR_PATH'
    )
    
    export_path: bpy.props.StringProperty(  # type: ignore
        name="エクスポート先フォルダ選択",
        description="モデルエクスポート先のフォルダを指定してください",
        subtype='DIR_PATH'
    )
    
    export_file_name_base: bpy.props.StringProperty(  # type: ignore
        name="ファイル名",
        description="エクスポートするモデルのベースファイル名（末尾が_{画像ファイル名}になります）",
        default="model"
    )
