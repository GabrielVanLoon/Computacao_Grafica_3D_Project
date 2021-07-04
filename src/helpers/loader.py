
def load_model_from_file(filename):
    """Loads a Wavefront OBJ file (Versão Ricardo Marcacini)"""

    objects  = {}
    vertices = []
    normals  = []
    texture_coords = []
    faces = []

    material = None

    # Open wavefront file and read line by line
    for line in open(filename, "r"): 

        # Comentario
        if line.startswith('#'): continue ## ignora comentarios

        # Quebra da linha em espaços
        values = line.split()

        # Se a linha estiver fazia ignora
        if not values: 
            continue

        # Recuperando Vertices de Posição (3 coords)
        if values[0] == 'v':
            vertices.append(values[1:4])

        # Recuperando Vetores Normais (3 coords)
        elif values[0] == 'vn':
            normals.append(values[1:4])

        # Recuperando Coordenadas de textura (2 coords)
        elif values[0] == 'vt':
            texture_coords.append(values[1:3])

        # Defininto o meterial do objeto (O que é mesmo)?
        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]

        # Definindo as faces
        elif values[0] == 'f':
            face = []
            face_texture = []
            face_normals = []

            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                face_normals.append(int(w[2]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)

            faces.append((face, face_texture, face_normals, material))

    model = {}
    model['vertices'] = vertices
    model['texture'] = texture_coords
    model['faces'] = faces
    model['normals'] = normals

    return model

def load_materials_from_file(filename):
    """Helper function to load .mtl files and illumination configs :P"""

    materials = {}
    default_values = {
        "Ns": 225.0, 
        "Ka": [1.0, 1.0, 1.0],
        "Kd": [0.8, 0.8, 0.8],
        "Ks": [0.5, 0.5, 0.5],
        "Ke": [0.0, 0.0, 0.0],
        "Ni": 1.55,
        "d":  1.0,
        "illum": 2,
        "map_Kd": None
    }

    material_name = "Start_Material"
    current_material = dict(default_values) # Copy without reference (!important)

    for line in open(filename, "r"):
        
        # If is comment or empty line
        if line.startswith("#") or (not line.split()):
            continue
        
        # If is a new material, save current and create another
        if line.startswith("newmtl"):
            materials[material_name] = current_material    
            material_name = line.split()[-1]
            current_material = dict(default_values)

        # If is Ka, Kd, Ks or Ke (3 float values)
        elif line.split()[0] in ["Ka", "Kd", "Ks", "Ke"]:
            Kvalues = line.split()
            current_material[Kvalues[0]] = [float(Kvalues[1]), float(Kvalues[2]), float(Kvalues[3])]

        # If is Ns, Ni or d (1 float value)
        elif line.split()[0] in ["Ns", "Ni", "d"]:
            Nvalue = line.split()
            current_material[Nvalue[0]] = float(Nvalue[1])

        # If is Ns, Ni or d (1 float value)
        elif line.split()[0] in ["Ns", "Ni", "d"]:
            Nvalue = line.split()
            current_material[Nvalue[0]] = float(Nvalue[1])

        # If is texture path
        elif line.startswith("map_Kd"):
            current_material["map_Kd"] =  line.split("/")[-1].rstrip()

    # Add last declared material
    materials[material_name] = current_material
    return materials


def get_textures_from_materials(materials, preffix_path=""):
    """Return a list of materials textures"""
    textures = []
    for mat in materials.values():
        if mat["map_Kd"] != None: textures.append(preffix_path+mat["map_Kd"])
    return textures


def load_model_from_file_and_mtl(filename, materials):
    """Loads a Wavefront OBJ file and materials (Versão Original)"""

    # Declarations of Positions, Normals and Textures Vertexes
    declares         = { "v": [], "vn": [], "vt": []}
    current_material = "Start_Material"
    faces            = []

    # Draw informations :)
    textures = get_textures_from_materials(materials)
    draws = [{"txt_index": None, "offset": 0, "qtd": 0}] # {"txt_index": None, "offset": 0, "qtd": 0}

    # Open wavefront file and read line by line
    for line in open(filename, "r"): 

        # If comment or empty line
        if line.startswith("#") or (not line.split()):
            continue
        
        # If is Position, Normal or Texture Vertex Declare
        elif line.split()[0] in ["v", "vn", "vt"]:
            values = line.split()
            max_coord = 3 if values[0] == "vt" else 4
            declares[values[0]].append([float(v) for v in values[1:max_coord]])

        # Define current active material
        elif line.split()[0] in ("usemtl", "usemat"):
            current_material = line.split()[-1].rstrip()
            draws.append(dict({
                "txt_index": textures.index(materials[current_material]["map_Kd"]),
                "offset": draws[-1]["offset"] + draws[-1]["qtd"], 
                "faces": 0
            }))

        # Defining the faces
        elif line.split()[0].startswith("f"):
            draws[-1]["faces"] += 1 # Add one in face draw counter

            values = line.split()
            face = []
            face_texture = []
            face_normals = []

            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                face_normals.append(int(w[2]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)

            faces.append((face, face_texture, face_normals, current_material))

    model = {
        "vertices": declares["v"],
        "texture": declares["vt"],
        "normals": declares["vn"],
        "faces": faces,
        "draws": draws
    }

    return model


if __name__ == "__main__":
    # print(load_materials_from_file("/home/gabriel/Models/_exports/jiro/jiro.mtl"))
    # print(load_materials_from_file("../../assets/sky/sky.mtl"))
    # print(load_model_from_file("../../assets/objects/cube.obj")['faces'])
    print(load_model_from_file_and_mtl("../../assets/cube/cube.obj", [])['faces'])